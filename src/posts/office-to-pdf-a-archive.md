title: Word, Excel and PowerPoint to PDF/A by API — for archives and e-filing
description: Convert DOCX, XLSX and PPTX (Cyrillic included) to PDF/A-2b in bulk with one API call — a real run, what I checked in the output, the price and the limits.
date: 2026-11-07
lang: en
slug: office-to-pdf-a-archive
pair: office-v-pdf-a-sud-arkhiv
---
Archives, document management systems and some e-filing portals accept only PDF/A: a PDF with every font embedded
and nothing that depends on the viewer's computer. Saving as PDF/A by hand works for one file. For a folder of
contracts, tables and slides you want it done by an API. Every output below is from a real run on 7 November 2026.

> Disclosure: I built the tool used here, [Office to PDF Converter](https://apify.com/ai_admin/office-to-pdf) on Apify.
> It runs LibreOffice in a container. The source code is open:
> [AndriyVK/-apify-document-tools](https://github.com/AndriyVK/-apify-document-tools).

## One call, several files

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("ai_admin/office-to-pdf").call(run_input={
    "sources": [
        {"url": "https://api.apify.com/v2/key-value-stores/FloomuI2DrQCJazY8/records/doc-uk.docx"},
        {"url": "https://api.apify.com/v2/key-value-stores/FloomuI2DrQCJazY8/records/sheet-uk.xlsx"},
    ],
    "pdfA": True,          # PDF/A-2b instead of a plain PDF
    "mergeIntoOne": True,  # also one merged.pdf in input order (free)
})
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item.get("fileName", "merged"), item["pages"], "pages", item["pdfUrl"])
```

The two sample files are public, so the code runs as is. Formats: DOCX, DOC, ODT, RTF, TXT, HTML, XLSX, XLS, ODS,
CSV, PPTX, PPT, ODP and images.

## The real output

```text
doc-uk.docx    1 page   44,040 bytes  pdfA: true
sheet-uk.xlsx  2 pages  32,574 bytes  pdfA: true
merged.pdf     3 pages  34,927 bytes  documents: 2
```

## What I checked in the PDF

A file that says «PDF/A» is not always one, so I opened the Word result:

- **The PDF/A label is there:** the XMP metadata says `pdfaid:part 2`, `pdfaid:conformance B` — PDF/A-2b.
- **All fonts are embedded** (`pdffonts`: `emb yes` for every font). This is what PDF/A is about: the file looks the
  same on any computer, in ten years too.
- **The Cyrillic text is real text,** not a picture: `pdftotext` gives back «Звіт про постачання», «Склад у Львові
  отримав 1240 палет…» — so the archive's search finds it.
- **Fonts were replaced.** The document asks for Calibri and Cambria, which are Microsoft fonts. The converter uses
  Carlito and Caladea instead — free fonts with the same letter widths, so lines and pages break in the same places.
  The look is close but not identical.

What I did not do: a full validation with [veraPDF](https://verapdf.org/), the reference PDF/A checker. If a portal
rejects files that fail veraPDF, run it on a sample before you convert the whole folder.

## Price

**$10 per 1,000 documents**, whatever the number of pages; merging is free; a file that fails to convert is not
charged. The run above cost two cents.

## Limits

- Password-protected files are not converted.
- Fonts that are not installed are replaced by metric-compatible ones; an unusual font may change the look slightly.
- Macros are not run.
- PDF/A is about how a file is stored. It does not sign it: if a court or an agency needs a qualified electronic
  signature, sign the PDF/A afterwards with your own signing tool.

## From an AI agent

The converter is also an MCP tool: `https://mcp.apify.com?tools=ai_admin/office-to-pdf`, so Claude, Cursor or any MCP
client can turn the files it has prepared into PDF/A.
