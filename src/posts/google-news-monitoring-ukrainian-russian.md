title: Monitor Ukrainian and Russian news with Google News - direct links and full article text for $2.50 per 1,000
description: Get Google News articles in Ukrainian, Russian and English as clean JSON in one run - direct publisher links, images and full article text for AI and RAG. A real run, the output, and how the price and features compare with the six most used Google News Actors.
date: 2026-11-16
lang: en
slug: google-news-monitoring-ukrainian-russian
pair: monitorynh-novyn-google-news
---
Media monitoring, brand mentions, a morning digest for a team, a news feed for an AI assistant - all of these start
with the same step: get the articles out of Google News as data. For Ukrainian and Russian sources there is one more
twist: the same story is covered in both languages, so you want both editions at once. This post shows a tool that
does that, with a real run from 16 November 2026.

**In short: the most complete data for the lowest price.** Direct links, full article text and several countries in
one run - all in one price of $2.50 per 1,000 articles, with no add-on fees.

> Disclosure: I built the tool, [Google News Scraper](https://apify.com/ai_admin/google-news-scraper) on Apify. The
> code is open: [AndriyVK/-apify-document-tools](https://github.com/AndriyVK/-apify-document-tools).

## One run, two languages

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("ai_admin/google-news-scraper").call(run_input={
    "queries": ["Укренерго"],
    "editions": ["UA:uk", "UA:ru"],
    "timeframe": "1d",
    "maxArticlesPerQuery": 10,
    "articleDetails": True,
    "fullText": True,
})
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item["edition"], item["source"], item["url"])
```

The run took 9 seconds and returned 19 articles: 10 from the Ukrainian edition and 9 from the Russian one, with no
duplicates. Every one of them came with:

- the **direct link** to the article on the publisher's site (19 of 19), not a Google News redirect;
- the article **image** and **description** (19 of 19);
- the **full article text**, cleaned of menus and ads, with a word count - ready to summarise or to put into a vector
  database. Four of the articles were from Ukr.net, which publishes short summaries of 24-28 words, and they came
  back as such.

One record from that run (text shortened):

```json
{
  "query": "Укренерго",
  "edition": "UA:uk",
  "title": "Борги на балансувальному ринку стримують інвестиції в нову маневрову генерацію - \"Укренерго\"",
  "source": "Гордон",
  "publishedAt": "2026-11-16T17:55:00Z",
  "url": "https://gordonua.com/ukr/section-money/news-borhy-na-balansuvalnomu-rynku-strymuyut-investytsiyi-v-novu-manevrovu-heneratsiyu-ukrenerho-16-11-2026.html",
  "imageUrl": "https://i.gordonua.com/news/2026/11/16/img0196-scaled.jpg?size=1300x975",
  "wordCount": 218,
  "text": "Заборгованість на балансувальному ринку електроенергії перешкоджає залученню інвестицій у нові маневрові потужності, потрібні для стабільної роботи енергосистем..."
}
```

## What else it does

- **Several queries and editions in one run:** `UA:uk`, `UA:ru`, `US:en`, `DE:de`, `PL:pl` and 40+ more. Compare how
  one story is covered in each market without running the tool five times.
- **More than 100 articles per query.** Google News shows at most 100 results per search. Give a date range and the
  tool reads it day by day, up to 5,000 articles per query.
- **Search operators** as on Google News: `"exact phrase"`, `OR`, `-exclude`, `site:`, `intitle:`.
- **Topic headlines** (TOP, WORLD, BUSINESS, TECHNOLOGY and others), often with the other outlets that cover the same
  story.
- **No proxy and no API key needed.**

## Price compared with the six most used Google News Actors

Prices for one article with the direct link, the page details and the text, as the Actors' Store pages showed them on
16 November 2026:

| Actor | Users a month | Price per 1,000 articles | Several queries and editions per run |
|---|---|---|---|
| **ai_admin/google-news-scraper** | new | **$2.50** (paid plans), $3 (free plan) | **yes** |
| data_xplorer/google-news-scraper-fast | 533 | $4 | one keyword, one edition |
| lhotanova/google-news-scraper | 413 | $2 + $1 link + $1 page = $4, plus $5 per 1,000 runs | one query, one edition |
| automation-lab/google-news-scraper | 201 | $2.30, plus $5 per 1,000 runs; no article text option | several queries, one edition |
| easyapi/google-news-scraper | 104 | $5, plus $90 per 1,000 runs | - |
| memo23/google-news-scraper | 42 | $2.50 + $0.50 link + $0.50 text = $3.50, plus $5 per 1,000 runs | - |

All features are included in the article price: the direct link, the details and the text cost nothing extra.

## Ideas for using it

- **Morning digest.** Schedule the run every day at 7:00 with your brand, competitors or a topic, then send the new
  articles to a team channel or let an AI write a summary from the `text` field.
- **Ukrainian and Russian coverage side by side.** One query, editions `UA:uk` and `UA:ru`, and you see who writes what.
- **A news dataset for RAG.** Topic headlines for a month with full text, one record per article, no duplicates.
- **AI agents.** The tool is also an MCP tool for Claude, Cursor and other agents - see
  [MCP server for document and media tools](/mcp-document-tools-for-ai-agents/).

What would you monitor first - your brand, a market, or a topic? Tell me in the comments.
