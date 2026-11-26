title: 5 Google News scrapers on the same queries - full text, direct links, several countries in one run
description: Five Google News Actors from the Apify Store, the same two queries in English and Ukrainian, measured on 26 November 2026: direct publisher links, full article text, run time and what you pay for. On the same pages: 26 of 27 full texts against 18 of 20.
date: 2026-11-27
lang: en
slug: google-news-scrapers-compared
pair: google-news-skrapery-porivniannia
---
Getting headlines out of Google News is easy. Getting **the article itself** - the direct publisher link and the full
text, ready for a summary, a digest or a RAG index - is where Google News tools differ. I ran the three most used
Google News Actors in the Apify Store, plus memo23 and mine, on the same two queries and compared what came back. All numbers are from runs
on 26 November 2026.

> Disclosure: one of the five is mine, [Google News Scraper](https://apify.com/ai_admin/google-news-scraper). Every
> number below comes from a real run with the same settings for every Actor.

## The test

- Two queries: "artificial intelligence" in the US edition (`US:en`) and «штучний інтелект» in the Ukrainian one
  (`UA:uk`).
- 10 articles from the last 7 days per query. Mine with `sortBy: "relevance"`, the others in their default order.
- Direct publisher links and full article text switched on wherever the Actor offers them.

## Short answer

| | ai_admin (mine) | data_xplorer | memo23 | lhotanova | automation-lab |
|---|---|---|---|---|---|
| Direct publisher links | **10 of 10** | 10 of 10 | 10 of 10 | 10 of 10 | 10 of 10 |
| Full text, Ukrainian query | **10 of 10** | 9 of 10 | 9 of 10 | no text option | no text option |
| Full text, US query | **9 of 10** | 9 of 10 | 9 of 10 | no text option | no text option |
| Several editions in one run | **yes** | no | no | no | no |
| Choice of order (newest or relevance) | **yes** | no | no | no | no |
| Run time with full text | **6-7 s** | 5-7 s | 72-97 s | 19-94 s | - |
| Page part charged only when read | **yes** | no (one price, also without text) | yes | - | - |

No duplicates in any output. The one US page nobody could read, on war.gov, is closed to robots for every Actor -
sites that block robots (Reuters is another) are a limit for all Google News tools, mine included.

## Full text on the same pages

The most useful number is what each tool does with **the same pages**. data_xplorer and memo23 returned 27 different
pages between them. On those 27 pages my tool extracted the full text from 26 (the same extraction code as in the
Actor, run on the pages from their output); data_xplorer and memo23 got 18 of their 20 each.

**On two of these pages a competitor came back empty and mine got the full text:** gur.gov.ua (data_xplorer: 0 words,
mine: 250) and dou.ua (memo23: 0 words, mine: 2,140). One of them is the article below - a post from DOU, the
Ukrainian developer community, that memo23 returned without text. This is how it came from my Ukrainian run:

```json
{
  "query": "штучний інтелект",
  "edition": "UA:uk",
  "title": "Монополія на інтелект, або як зробити штучний інтелект персональним і до чого це може призвести",
  "source": "Спільнота програмістів",
  "url": "https://dou.ua/forums/topic/63499/",
  "imageUrl": "https://s.dou.ua/img/announces/image_3_qziV40t.jpg",
  "author": "Andriy Belyaev",
  "publishedAt": "2026-11-20T12:00:05Z",
  "wordCount": 2140,
  "text": "Монополія на інтелект, або як зробити штучний інтелект персональним..."
}
```

The whole Ukrainian run - 10 articles, every one with its direct link, image and full text - took 6.6 seconds.

## Several countries in one run

All four other Actors take one region per run. Mine takes a list: `UA:uk`, `UA:ru`, `US:en`, `DE:de`, `PL:pl` and 40+
more, together with several queries. Comparing how one story is covered in three markets is one run, not three.

## Your order of results

`sortBy: "relevance"` gives Google's own order - the best choice when you want the most complete texts.
`sortBy: "newest"` puts today's articles first - the best choice for monitoring.

## You pay for what you get

| What | Paid plans (Bronze) | Free plan |
|---|---|---|
| Article: headline and direct publisher link | $2.50 per 1,000 | $3 per 1,000 |
| Page read: details and full text | $0.50 per 1,000 | $0.50 per 1,000 |

The page part is charged only when the page was actually read. A site that blocks robots or a paywall costs nothing
beyond the headline. A fully read article costs $3 per 1,000 on Bronze - a fair price, with no hidden extras.

## Try it with the same input

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("ai_admin/google-news-scraper").call(run_input={
    "queries": ["штучний інтелект"],
    "editions": ["UA:uk"],
    "timeframe": "7d",
    "maxArticlesPerQuery": 10,
    "fullText": True,
    "sortBy": "relevance",
})
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item["source"], item["wordCount"], item["url"])
```

More ideas - a morning digest, Ukrainian and Russian coverage side by side, a news dataset for RAG - are in
[the first post about this tool](/google-news-monitoring-ukrainian-russian/). It is also an MCP tool for Claude,
Cursor and other agents - see [MCP server for document and media tools](/mcp-document-tools-for-ai-agents/).

Which news would you monitor - your brand, a market or a topic? Tell me in the comments.

## Try it in two minutes

1. Open [Google News Scraper](https://apify.com/ai_admin/google-news-scraper) and press **Try for free**.
2. The input is already filled with a working example: press **Start**, or put in your own search queries.
3. Apify's free plan includes $5 of usage every month - enough to test it on your own data.
