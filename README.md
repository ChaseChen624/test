# DeepSeek + Futu ETF Demo

This repository contains a minimal Python script that shows how to connect DeepSeek's chat completion API with Futu's OpenAPI to run a toy ETF trading loop.

## Features

- Pulls real-time quotes and recent 1-minute K-line data for a target ETF from Futu OpenAPI.
- Builds a compact market summary and sends it to a DeepSeek model for a buy/sell/hold decision.
- Optionally places a trade through Futu's trading context when the model suggests BUY or SELL.

## Requirements

Install dependencies via pip:

```bash
pip install -r requirements.txt
```

You must have Futu's `OpenD` running locally and expose the host/port to the script. A DeepSeek API key with access to the Chat Completions endpoint is also required.

## Environment Variables

| Variable | Description | Default |
| --- | --- | --- |
| `DEEPSEEK_API_KEY` | DeepSeek API key used for authentication | **required** |
| `DEEPSEEK_API_URL` | Override the base URL for the DeepSeek API | `https://api.deepseek.com/v1/chat/completions` |
| `DEEPSEEK_MODEL` | Model name passed to the DeepSeek API | `deepseek-chat` |
| `ETF_SYMBOL` | ETF ticker understood by Futu OpenAPI | `HK.02800` |
| `FUTU_HOST` | Hostname where Futu OpenD is listening | `127.0.0.1` |
| `FUTU_PORT` | Port exposed by OpenD | `11111` |
| `ORDER_SIZE` | Quantity to trade when a signal is emitted | `100` |
| `FUTU_TRADING_ENV` | `SIMULATE` or `REAL` trading environment | `SIMULATE` |
| `FUTU_TRADE_PWD` | Trade password required by Futu when placing orders | **required if trading** |

## Usage

Run the demo after setting the environment variables:

```bash
export DEEPSEEK_API_KEY="sk-..."
export FUTU_TRADE_PWD="your_trade_pwd"  # only needed when enabling live orders
python demo_deepseek_futu.py
```

The script will print the DeepSeek decision and only submit an order if the action is `BUY` or `SELL`.

> ⚠️ **Disclaimer:** This demo is for educational purposes only. Review and customize risk controls before using it in production or with real funds.
