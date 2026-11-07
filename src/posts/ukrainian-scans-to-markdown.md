title: Ukrainian scanned PDFs to Markdown for RAG and LLMs
description: How to turn scanned Ukrainian (Cyrillic) PDFs, Word and Excel files into clean Markdown and chunks for an AI pipeline — with a real run, its output, the price and the limits.
date: 2026-11-06
lang: en
slug: ukrainian-scans-to-markdown
pair: skany-ukrainskoyu-v-markdown
---
Most document-to-text tools are tuned for English. A scanned Ukrainian invoice or court decision often comes back
as Latin look-alike gibberish, or with its tables lost. This guide shows a pipeline that keeps Cyrillic text,
headings and tables, and shows exactly what it does and does not do — every output below is from a real run on
6 November 2026.

> **Update, 7 November 2026.** The first run showed two problems: a table in a scan came back as one flat row, and
> `["ukr", "eng"]` turned «Арматура» into `Apmatypa`. Both are fixed now; the outputs below are from the fixed
> version (build 0.1.14), and the old ones are kept in the text so you can see the difference.

> Disclosure: I built the tool used here, [Document to Markdown for AI](https://apify.com/ai_admin/document-to-markdown)
> on Apify. Its source code is open: [AndriyVK/-apify-document-tools](https://github.com/AndriyVK/-apify-document-tools).

## What you get

One record per document: the Markdown, every table as rows of cells, optional chunks with their nearest heading
(ready for a vector database), and page counts. PDF pages with a text layer are read directly; scanned pages and
images go through Tesseract OCR, which has a proper Ukrainian model.

Formats: PDF, scanned PDF, PNG/JPG/TIFF, DOCX/DOC, XLSX/XLS, PPTX/PPT, ODT/ODS/ODP, RTF, HTML.

## Run it from Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("ai_admin/document-to-markdown").call(run_input={
    "sources": [
        {"url": "https://api.apify.com/v2/key-value-stores/FloomuI2DrQCJazY8/records/scan-uk.pdf"},
        {"url": "https://api.apify.com/v2/key-value-stores/FloomuI2DrQCJazY8/records/sheet-uk.xlsx"},
    ],
    "ocrMode": "auto",          # OCR only pages without a text layer
    "ocrLanguages": ["ukr"],    # list only the languages that are really in the scan
    "includeTables": True,
    "chunkSize": 800,           # characters per chunk, 0 = no chunks
})
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item["fileName"], item["ocrPages"], "OCR pages")
    print(item["markdown"])
```

The two sample files are public, so you can run this as is. Your own files work by URL, or from your Apify
key-value store.

## The real output

**A one-page scan** (`scan-uk.pdf`, no text layer — 1 OCR page):

```text
Звіт про постачання

Склад у Львові отримав 1240 палет будівельних матеріалів протягом

третього кварталу. Терміни доставки скоротилися на дванадцять відсотків після запровадження

нового графіка.

| Товар | Кількість | Ціна |
| --- | --- | --- |
| Цемент | 420 | 96,50 |
| Арматура | 180 | 412,00 |
```

The text is right, letter for letter, and the ruled table is a real table again — in the Markdown and as JSON rows
`[["Товар", "Кількість", "Ціна"], ["Цемент", "420", "96,50"], ["Арматура", "180", "412,00"]]`. On 6 November the
same scan gave one flat row: `| Товар | Кількість | Ціна | Цемент | 420 | 96,50 | Арматура | 180 | 412,00`.

**The same content as an Excel file** (`sheet-uk.xlsx`, 0.2 s) — here the structure is exact:

```text
## Data

| Товар | Кількість | Ціна |
| --- | --- | --- |
| Цемент | 420 | 96,50 |
| Арматура | 180 | 412,00 |
| Total | 600 | 1,234.50 |
```

Cell values are kept as written: `96,50` stays `96,50`, it is not turned into a float.

## One setting that matters: OCR languages

On 6 November, with `"ocrLanguages": ["ukr", "eng"]`, the word «Арматура» came back as `Apmatypa` — the OCR picked
Latin letters that look the same. Now such a word is put back in Cyrillic when it is in Tesseract's Ukrainian
dictionary and the Latin spelling is not an English word, so `Excel`, `API` or `copy` stay as they are. The run on
7 November with `["ukr", "eng"]` gave «Арматура» correctly. Still, list only the languages that are really on the
page: every extra language is one more way for the OCR to guess wrong.

## Price

You pay per page: **$1 per 1,000 text pages and $4 per 1,000 OCR pages** (Apify pay-per-event pricing; OCR is
charged only for pages that needed it). A document that cannot be downloaded or read is not charged. The two files
above cost a fraction of a cent.

## Limits — honestly

- **Tables in scans** come back as tables when they have ruled grid lines and the scan is clean. A borderless table,
  or a grid lost in a noisy 200 dpi scan, still comes out as text. If you have the original Word or Excel file,
  convert that instead — its tables are exact.
- **OCR quality follows the scan.** Clean 300 dpi scans read well; phone photos at an angle are worse. For photos, the
  [Image to Text OCR](https://apify.com/ai_admin/image-to-text-ocr) Actor auto-rotates pages and returns a confidence
  for every word.
- **Handwriting** is not supported.

## Use it from an AI agent

The same tool is available through the Apify MCP server, so Claude, Cursor or any MCP client can call it:
`https://mcp.apify.com?tools=ai_admin/document-to-markdown`. A local MCP server with all our tools is in
[the GitHub repository](https://github.com/AndriyVK/-apify-document-tools/tree/main/mcp-server).
