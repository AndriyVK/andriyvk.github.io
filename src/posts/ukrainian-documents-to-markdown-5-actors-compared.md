title: Ukrainian scans, invoices, Word and Excel to Markdown - 5 Apify Actors on 7 files, only one got every table right
description: Five document-to-Markdown Actors from the Apify Store on the same seven Ukrainian files - text PDF, clean and noisy scans, DOCX, XLSX and scanned invoices without table lines. Empty scans, changed prices, lost tables - and the one Actor that got every file right at the lowest price per scanned page.
date: 2026-11-15
lang: en
slug: ukrainian-documents-to-markdown-5-actors-compared
pair: dokumenty-ukrainskoyu-v-markdown-porivniannia
---
Search the Apify Store for "PDF to Markdown" and you get dozens of Actors with almost the same promise: text,
tables, OCR, ready for RAG. None of them tells you what happens with a Ukrainian scan, an Excel file or a scanned
invoice whose table has no lines. So I ran five of them on the same seven files and compared every output with the
text the files were made from. All results below are from real runs on 15 November 2026.

> Disclosure: one of the five is mine, [Document to Markdown for AI](https://apify.com/ai_admin/document-to-markdown).
> Every number below comes from a real run, the test files are public and the raw outputs are kept, so you can repeat
> and check all of it.

## Short answer

| | Files right (of 7) | Invoice without lines: rows exact | Reads Word and Excel | Price per scanned page |
|---|---|---|---|---|
| **ai_admin/document-to-markdown** | **7** | **5 of 5** | **yes** | **$0.004** |
| nidamindllc/doc-ocr | 2 | 4 of 5 | no (error) | $0.004 |
| lergassy/pdf-text-extractor | 1 | 0 | yes | $0.0111 |
| fabrikit/document-to-markdown | 2 | 0 | yes | $0.0105 |
| gochujang/pdf-text-extractor | 1 | 0 (empty) | no (PDF only) | $0.006 |

"Right" means the text, the heading and the table with the correct rows and with every number exactly as in the
document.

## The seven files

All Ukrainian, all generated from known text, so every character can be checked:

| File | What it is |
|---|---|
| `text-uk.pdf` | PDF with a text layer: heading, two sentences, a 3 x 3 table with prices like `96,50` |
| `scan-uk.pdf` | the same page as a clean scan |
| `scan-noisy-uk.pdf` | the same scan with noise and a slight tilt |
| `doc-uk.docx` | Word document with the text, a list and the table |
| `sheet-uk.xlsx` | Excel workbook: the table with a `Total` row `1,234.50`, and a sheet with the sentences |
| `scan-borderless-uk.pdf` | a scanned invoice: 5 x 6 table **without any lines**, amounts like `40 530,00` and `2 500` |
| `scan-noisy-borderless-uk.pdf` | the same invoice, noisy and tilted |

The last two are the hard case and the most common one: most invoices, waybills and bank statements are printed
without table lines. The files are public:
`https://api.apify.com/v2/key-value-stores/FloomuI2DrQCJazY8/records/<file name>`.

The Actors are the most used ones for this search plus one that lists Office formats. Settings: Ukrainian OCR
wherever the Actor has a language option (`ukr`); nidamindllc has no language option.

## Results, file by file

| File | mine | nidamindllc | lergassy | fabrikit | gochujang |
|---|---|---|---|---|---|
| Text PDF | **right** | one OCR typo, table right (HTML) | table flattened into the text | table as plain lines | right |
| Clean scan | **right** | right (HTML table) | table as broken lines | table lost | **empty** |
| Noisy scan | **right** | right (HTML table) | table as broken lines | rows without header | **empty** |
| DOCX | **right** | error | right | right | not supported |
| XLSX | **right**, `1,234.50` kept | error | `1,234.50` became `1234.5` | right | not supported |
| Invoice, no lines | **5/5 rows, 30/30 cells** | 4/5 rows, 29/30 cells | no table, `40 530,00` lost its space | no table, all in one line, `96,50` read as `96,0` | **empty** |
| Invoice, no lines, noisy | **5/5 rows, 30/30 cells** | 4/5 rows, 29/30 cells | no table, `96,50` read as `96,60` | no table, all in one line | **empty** |

This is what my Actor returned for the noisy invoice without lines - every cell, every number and the `№` sign as in
the document:

```text
Рахунок-фактура № 47

Постачальник: ТОВ «Будмайстер», м. Львів. Покупець: ФОП Коваленко О. В. Оплата протягом п'яти банківських днів з дати рахунку.

| № | Товар | Од. | Кількість | Ціна | Сума |
| --- | --- | --- | --- | --- | --- |
| 1 | Цемент М500 | мішок | 420 | 96,50 | 40 530,00 |
| 2 | Арматура 12 мм | шт. | 180 | 412,00 | 74 160,00 |
| 3 | Пісок річковий | т | 12 | 650,00 | 7 800,00 |
| 4 | Цегла рядова | шт. | 2 500 | 9,80 | 24 500,00 |

Разом: 146 990,00 грн
```

The same table also comes as rows of cells in the `tables` field, ready for a spreadsheet or a database, and the
record says how many pages went through OCR, so a pipeline knows which text came from a scan.

For comparison, the same line of the invoice from two other Actors:

```text
lergassy:  1 | Цемент М500 мішок 420 96,60 40530,00
fabrikit:  ... Мо Товар Од. Кількість Ціна Сума 1 Цемент М500 мішок 420 96,50 40 530,00 2 Арматура12мм шт. ...
```

## What stood out

- **gochujang returned empty text for all four scans** and still marked them `ok: true`; the run log says
  `Failed loading language 'ukr'`. It is the most used Actor of the five (40 users a month) and is clean on text
  PDFs, but it cannot read a Ukrainian scan.
- **nidamindllc is good on scans** - the only competitor that kept the invoice table - but it OCRs every PDF, even one
  with a text layer, which added a typo the file did not have, and it cannot open Word or Excel files at all.
- **lergassy and fabrikit read every format but not the tables.** On the invoice lergassy changed a price (`96,50` to
  `96,60`), and on the spreadsheet it changed `1,234.50` to `1234.5`; fabrikit read the same price as `96,0` on the clean
  invoice. In an invoice or a price list that is the worst kind of error: it looks right.
- **Mine got all seven files right**, including both invoices without lines, with the numbers exactly as written.

## What it cost

All five Actors charge per event. For a scanned page:

| Actor | One scanned page | Text page or Office file |
|---|---|---|
| **mine** | **$0.004** | **$0.001** |
| nidamindllc | $0.004 | $0.004 (OCRs everything) |
| gochujang | $0.006 | $0.006 per one-page PDF |
| fabrikit | $0.0105 | $0.0005 |
| lergassy | $0.0111 | $0.0031 |

My run of all seven files cost **$0.019** and took 11 seconds.

## About the test

- One file of each kind, small and synthetic. Real archives have worse scans, stamps and handwriting - try ten of
  your own files before you choose. That costs a few cents.
- Every Actor ran with the build that was public on 15 November 2026 (mine: 0.1.20).

While preparing this article, the test results showed me where my Actor could become the best in its category -
noisy scans and invoices without table lines - so I improved it right away, before publishing. The latest runs
described above confirm it.

## Try it

From Python:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("ai_admin/document-to-markdown").call(run_input={
    "sources": [{"url": "https://api.apify.com/v2/key-value-stores/FloomuI2DrQCJazY8/records/scan-noisy-borderless-uk.pdf"}],
    "ocrLanguages": ["ukr"],
})
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item["markdown"])
    print(item["tables"])
```

Or give it to Claude, Cursor or another AI agent as an MCP tool - see
[MCP server for document and media tools](/mcp-document-tools-for-ai-agents/).

## Related posts

- [Ukrainian scanned PDFs to Markdown for RAG and LLMs](/ukrainian-scans-to-markdown/)
- [Office to PDF/A for archives and e-filing](/office-to-pdf-a-archive/)
