---
name: iran-situation-monitoring
description: Daily monitoring of Iran situation. Use when the user wants to monitor or track the latest developments about Iran, including geopolitics, military affairs, nuclear program, economy, and domestic politics.
---

# Iran Situation Daily Monitor

Produce a structured daily intelligence briefing on the current Iran situation by searching multiple news sources and synthesizing findings.

## Workflow

Make a todo list for all tasks in this workflow and work through them one by one.

### 1. Set Date Context

Note today's date and use it to focus searches on the most recent developments (last 24–48 hours preferred, last 7 days acceptable if breaking news is sparse).

### 2. Search for Latest Developments

Run the following WebSearch queries **in parallel** to maximize coverage:

- `Iran nuclear program latest news {today's date}`
- `Iran military news {today's date}`
- `Iran US relations latest {today's date}`
- `Iran Israel tensions {today's date}`
- `Iran economy sanctions {today's date}`
- `Iran domestic politics protests {today's date}`
- `Iran proxy forces Middle East {today's date}`

Collect URLs and key headlines from each search result.

### 3. Deep-Read Key Sources

For each search result set, use WebFetch on the 1–2 most authoritative or detailed articles per topic (prefer Reuters, AP, BBC, Al Jazeera, Times of Israel, Iran International, Radio Farda). Extract:
- Specific facts, names, dates, locations
- Quotes from officials
- Any escalation or de-escalation signals

### 4. Analyze and Synthesize

Identify:
- The single most significant development of the day
- Any trend changes compared to recent weeks (escalation, diplomacy, sanctions, protests, etc.)
- Cross-topic linkages (e.g., nuclear talks affecting economic news)

### 5. Assess Risk Level

Rate the overall situation on a simple scale:
- 🟢 **Calm** — No major escalation; routine diplomacy/sanctions activity
- 🟡 **Elevated** — Heightened rhetoric or localized incidents; monitoring warranted
- 🔴 **Critical** — Active military engagement, nuclear threshold event, or regime-stability crisis

### 6. Output Daily Briefing

Present the report in the structured format below.

---

## Daily Briefing Format

```
========================================
🌐 IRAN SITUATION REPORT — {DATE}
========================================

RISK LEVEL: 🟢/🟡/🔴 [CALM / ELEVATED / CRITICAL]

## HEADLINE
[One-sentence summary of the most important development today]

## KEY DEVELOPMENTS

### Nuclear & Military
- [bullet]
- [bullet]

### Geopolitics (US / Israel / Gulf / Europe)
- [bullet]
- [bullet]

### Proxy & Regional Activity
- [bullet]
- [bullet]

### Domestic Affairs (Politics / Economy / Society)
- [bullet]
- [bullet]

## ANALYSIS
[2–4 sentences on what these developments mean together — trends, risks, opportunities]

## SOURCES
- [Source name — URL]
- [Source name — URL]
...

========================================
```

## Wrap Up

After delivering the briefing, offer the user the option to:
1. **Drill down** on any specific topic (e.g., "Tell me more about the nuclear situation")
2. **Save** the briefing to a local file (e.g., `iran-briefing-{date}.md`)
3. **Schedule** recurring monitoring using the `/loop` skill
