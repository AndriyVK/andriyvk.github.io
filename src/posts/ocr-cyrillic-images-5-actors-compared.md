title: Ukrainian and Russian text from images - 5 Apify OCR Actors compared, only one read the invoice table
description: Five image-to-text OCR Actors from the Apify Store on the same Ukrainian text, Russian text and a noisy scanned invoice. Latin gibberish, missing languages, invoice tables read column by column - and the one Actor that returned exact text and a correct table at the usual market price.
date: 2026-11-16
lang: en
slug: ocr-cyrillic-images-5-actors-compared
pair: ocr-kyrylytsia-kartynky-porivniannia
---
"Image to text" is one of the most searched tasks in the Apify Store, and most OCR Actors are tuned for English.
If your images are Ukrainian or Russian - screenshots, photos of documents, scanned invoices - the results differ a
lot. I ran five OCR Actors on the same three images and compared every output with the text the images were made
from. All results are from real runs on 16 November 2026.

> Disclosure: one of the five is mine, [Image to Text OCR](https://apify.com/ai_admin/image-to-text-ocr). Every
> number below comes from a real run, the images are public and the raw outputs are kept.

## Short answer

| Actor | Ukrainian text | Russian text | Invoice: numbers exact | Invoice table | Price per image |
|---|---|---|---|---|---|
| **ai_admin/image-to-text-ocr** | **100%** | **100%** | **12 of 12** | **rows, exact** | **$0.004** |
| zen-studio/google-lens-ocr | 100% | 100% | 11 of 12 | read column by column | about $0.007 |
| getascraper/google-lens-ocr | 100% | 100% | 10 of 12 | read column by column | about $0.004 |
| steadydata/image-ocr-text | Latin gibberish | Latin gibberish | 7 of 12 | no | about $0.004 |
| gochujang/image-ocr-extractor | error: no Ukrainian | error | - | - | $0.003 |

## The three images

| Image | What it is |
|---|---|
| `image-uk.png` | Ukrainian heading and two sentences, clean |
| `image-ru.png` | the same in Russian |
| `invoice-noisy-uk.png` | a scanned Ukrainian invoice with noise and a slight tilt: a 5 x 6 table **without lines**, amounts like `40 530,00` and `2 500` |

They are public: `https://api.apify.com/v2/key-value-stores/FloomuI2DrQCJazY8/records/<file name>`.

Settings: my Actor with `languages: ["ukr", "rus"]` - one setting for both languages, as a buyer with mixed
documents would use it; the Google Lens Actors with their language field set to `uk` or `ru`; the others have no
language option or take a Tesseract code (`ukr+rus`).

The Actors are the most used ones for "image to text" and "OCR" in the Store on that day: steadydata has 178 users a
month, the two Google Lens Actors 63 and 57, gochujang 32.

## What each one returned

**Clean Ukrainian and Russian text.** My Actor and both Google Lens Actors returned the text character for character,
including «і», «ї», «ё» and «ы». My Actor does it with a single setting for both languages: it finds out which
language each page is in, reads it with that language first and reports the switch in the `languagesUsed` field.

steadydata returned Cyrillic as Latin look-alikes - the Ukrainian heading «Звіт про постачання» came back as
`3BiTnpOnOCTayaHHA`. gochujang failed on every image with `Failed loading language 'ukr'`: the Ukrainian model is not
installed, but the start of the run is still charged.

**The noisy invoice.** This is where the difference shows. My Actor returned the table as rows, with every number as
printed, in the `markdown` field and as cells in `tables`:

```text
Рахунок-фактура № 47

| № | Товар | Од. | Кількість | Ціна | Сума |
| --- | --- | --- | --- | --- | --- |
| 1 | Цемент М500 | мішок | 420 | 96,50 | 40 530,00 |
| 2 | Арматура 12 мм | шт. | 180 | 412,00 | 74 160,00 |
| 3 | Пісок річковий | т | 12 | 650,00 | 7 800,00 |
| 4 | Цегла рядова | шт. | 2 500 | 9,80 | 24 500,00 |

Разом: 146 990,00 грн
```

The Google Lens Actors read every word, but the table came back column by column, so the rows of the invoice are no
longer together. This is the start of the getascraper output:

```text
№
Товар
Цемент М500.
Арматура 12 мм
Пісок річковий
T
Цегла рядова
Од.
мішок
2
шт.
```

On top of that, `40 530,00` became `40.530,00` in both, the unit «т» became a Latin `T`, and getascraper split
`24 500,00` into two lines. To get a table back from that, you would need another tool.

steadydata got 7 of the 12 numbers and none of the Cyrillic words right.

## Price

| Actor | One image | Notes |
|---|---|---|
| **mine** | **$0.004** | plus $0.0001 per run |
| getascraper | $0.004 | |
| steadydata | $0.004 | $0.003 read + $0.001 check, plus a start fee per run |
| zen-studio | about $0.007 | $0.005 per image plus $0.002 per run, and one run takes one image |
| gochujang | $0.003 | plus $0.001 per run |

So the price is the same as the Google Lens and steadydata Actors - the difference is what you get for it.

## Verdict

- **Exact text in Ukrainian and Russian, with one setting** - mine and the two Google Lens Actors.
- **Invoice as a real table with exact numbers** - only mine.
- **Price** - the same $0.004 as getascraper and steadydata, less than zen-studio.

While preparing this article, the test results showed me where my Actor could become the best in its category -
mixed Ukrainian and Russian documents and invoice tables without lines - so I improved it right away, before
publishing. The latest runs described above confirm it.

## Try it

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("ai_admin/image-to-text-ocr").call(run_input={
    "sources": [{"url": "https://api.apify.com/v2/key-value-stores/FloomuI2DrQCJazY8/records/invoice-noisy-uk.png"}],
    "languages": ["ukr", "rus"],
})
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item["markdown"])
    print(item["tables"])
```

It is also a tool for Claude, Cursor and other AI agents - see
[MCP server for document and media tools](/mcp-document-tools-for-ai-agents/). For whole PDFs, Word and Excel files,
see [5 document-to-Markdown Actors on 7 files](/ukrainian-documents-to-markdown-5-actors-compared/).

Which documents do you need to read from images - receipts, invoices, screenshots? Tell me in the comments, and I
will test those next.

## Try it in two minutes

1. Open [Image to Text OCR](https://apify.com/ai_admin/image-to-text-ocr) and press **Try for free**.
2. The input is already filled with a working example: press **Start**, or put in links to your own files.
3. Apify's free plan includes $5 of usage every month - enough to test it on your own data.
