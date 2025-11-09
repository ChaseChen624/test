"""Demo script for integrating DeepSeek with Futu OpenAPI to trade ETFs.

This script illustrates the following steps:
1. Fetch latest ETF price data from Futu's OpenAPI.
2. Aggregate data into a structured prompt for DeepSeek.
3. Ask DeepSeek to provide a trading decision.
4. Submit a simulated order through Futu's trading API if instructed.

The script is intentionally simplified and uses blocking I/O for clarity.
"""
import json
import os
import textwrap
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import requests
from futu import (
    KLType,
    OpenQuoteContext,
    OpenTradeContext,
    RET_OK,
    SubType,
)


@dataclass
class Candle:
    time_key: datetime
    open: float
    close: float
    high: float
    low: float
    volume: float


def fetch_realtime_quote(symbol: str, host: str, port: int) -> Dict[str, Any]:
    """Subscribe to realtime quotes and return latest price snapshot."""
    with OpenQuoteContext(host=host, port=port) as quote_ctx:
        ret, _ = quote_ctx.subscribe(symbol, SubType.QUOTE)
        if ret != RET_OK:
            raise RuntimeError(f"Failed to subscribe quote: {ret}")

        ret, data = quote_ctx.get_stock_quote(symbol)
        if ret != RET_OK or data.empty:
            raise RuntimeError("No quote data received")
        return data.iloc[0].to_dict()


def fetch_recent_candles(symbol: str, host: str, port: int, limit: int = 60) -> List[Candle]:
    """Fetch recent 1-minute K-line data and convert into Candle objects."""
    end = datetime.now()
    start = end - timedelta(minutes=limit * 2)
    with OpenQuoteContext(host=host, port=port) as quote_ctx:
        ret, data, _ = quote_ctx.request_history_kline(
            code=symbol,
            start=start.strftime("%Y-%m-%d %H:%M:%S"),
            end=end.strftime("%Y-%m-%d %H:%M:%S"),
            ktype=KLType.K_1M,
            max_count=limit,
        )
        if ret != RET_OK or data.empty:
            raise RuntimeError("Failed to fetch history kline")

        candles = [
            Candle(
                time_key=datetime.strptime(row["time_key"], "%Y-%m-%d %H:%M:%S"),
                open=float(row["open"]),
                close=float(row["close"]),
                high=float(row["high"]),
                low=float(row["low"]),
                volume=float(row["volume"]),
            )
            for _, row in data.iterrows()
        ]
        return candles


def build_deepseek_prompt(symbol: str, quote: Dict[str, Any], candles: List[Candle]) -> str:
    """Build a concise prompt summarizing the latest market context."""
    last_candle = candles[-1]
    summary_lines = [
        f"Symbol: {symbol}",
        f"Last price: {quote['last_price']}",
        f"Open interest: {quote.get('open_interest', 'N/A')}",
        f"Last candle close: {last_candle.close}",
        f"Change %: {quote.get('change_rate', 'N/A')}",
    ]
    history_block = "\n".join(
        f"{c.time_key.strftime('%H:%M')} O:{c.open:.2f} C:{c.close:.2f} H:{c.high:.2f} L:{c.low:.2f} V:{c.volume:.0f}"
        for c in candles[-10:]
    )

    instructions = textwrap.dedent(
        """
        You are a cautious quantitative trading assistant.
        Decide whether to BUY, SELL, or HOLD the ETF based on the intraday trend.
        Reply in JSON with the schema:
        {"action": "BUY|SELL|HOLD", "confidence": 0-1, "reason": "brief explanation"}
        Only buy if momentum is positive and volatility is low.
        Only sell if price is falling sharply or volume spikes negatively.
        Otherwise hold. Never provide orders that exceed normal trading sizes.
        """
    ).strip()

    prompt = "\n".join(summary_lines) + "\n\nRecent candles:\n" + history_block + "\n\n" + instructions
    return prompt


def call_deepseek(prompt: str, model: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.environ["DEEPSEEK_API_KEY"]
    api_url = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
    payload = {
        "model": model or os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        "messages": [
            {"role": "system", "content": "You are an experienced ETF quantitative analyst."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    response = requests.post(
        api_url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return json.loads(data["choices"][0]["message"]["content"])


def place_order(symbol: str, action: str, size: int, price: float, host: str, port: int) -> None:
    trade_password = os.environ.get("FUTU_TRADE_PWD")
    if not trade_password:
        raise RuntimeError("FUTU_TRADE_PWD environment variable is required")

    with OpenTradeContext(host=host, port=port) as trade_ctx:
        order_type = "BUY" if action == "BUY" else "SELL"
        ret, _ = trade_ctx.place_order(
            price=price,
            qty=size,
            code=symbol,
            trd_side=order_type,
            order_type="NORMAL",
            trd_env=os.getenv("FUTU_TRADING_ENV", "SIMULATE"),
            trd_password=trade_password,
        )
        if ret != RET_OK:
            raise RuntimeError("Failed to place order")


def main() -> None:
    symbol = os.getenv("ETF_SYMBOL", "HK.02800")
    futu_host = os.getenv("FUTU_HOST", "127.0.0.1")
    futu_port = int(os.getenv("FUTU_PORT", "11111"))
    order_size = int(os.getenv("ORDER_SIZE", "100"))

    quote = fetch_realtime_quote(symbol, futu_host, futu_port)
    candles = fetch_recent_candles(symbol, futu_host, futu_port)

    prompt = build_deepseek_prompt(symbol, quote, candles)
    decision = call_deepseek(prompt)

    print("DeepSeek decision:", decision)

    action = decision.get("action")
    if action not in {"BUY", "SELL"}:
        print("No trade executed.")
        return

    price = float(quote["last_price"])
    print(f"Submitting {action} order for {symbol} @ {price}")
    place_order(symbol, action, order_size, price, futu_host, futu_port)


if __name__ == "__main__":
    main()
