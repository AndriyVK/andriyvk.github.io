title: MCP server for document and media tools - give Claude or Cursor OCR, PDF and audio tools
description: One MCP server gives an AI agent 9 tools - documents and scans to Markdown, Office to PDF/A, OCR, speech to text, text to speech, screenshots, domain checks, video frames. Real calls from an MCP client, the output, the price and the limits.
date: 2026-11-15
lang: en
slug: mcp-document-tools-for-ai-agents
pair: mcp-instrumenty-dlia-shi-ahentiv
---
An AI agent is good at reading text, but a lot of real work arrives as files: a scanned invoice, a spreadsheet, a
voice note, a website that has to be checked. The Model Context Protocol (MCP) lets an agent call tools for that. This
post shows one MCP server that gives Claude, Cursor or any other MCP client nine such tools, and what two of them
returned when an MCP client called them on 15 November 2026.

> Disclosure: I built this server and the Apify Actors behind it. The code is open (MIT):
> [AndriyVK/-apify-document-tools](https://github.com/AndriyVK/-apify-document-tools/tree/main/mcp-server).

## The tools

| Tool | What it does | Price on paid plans (billed by Apify) |
|---|---|---|
| `convert_document_to_markdown` | PDF (text and scanned, OCR), images, DOCX/DOC, XLSX/XLS, PPTX/PPT, ODT, RTF, HTML to Markdown, JSON tables, RAG chunks | $2 / 1,000 text pages, $4 / 1,000 OCR pages |
| `convert_office_to_pdf` | Word, Excel, PowerPoint, OpenDocument, RTF, HTML, images to PDF or PDF/A-2b, optional merge | $10 / 1,000 documents |
| `convert_pdf_or_images` | PDF pages to PNG/JPG/WebP/TIFF, images to PDF, iPhone HEIC to JPG, resize | $2 / 1,000 images |
| `transcribe_audio` | Audio and video to text, timestamped segments, SRT/VTT (Whisper large-v3) | $6 / 1,000 minutes |
| `ocr_images` | Images and scanned PDFs to text, lines with confidence and boxes | $4 / 1,000 images |
| `text_to_speech` | Text or PDF/DOCX/HTML to MP3/WAV/OGG plus SRT subtitles | $10 / 1,000 audio minutes |
| `screenshot_website` | Full-page screenshots or PDF of web pages or your own HTML | $4 / 1,000 pages |
| `check_domains` | WHOIS/RDAP (registrar, expiry), DNS records, SSL certificate expiry | $3 / 1,000 domains |
| `extract_video_frames` | Video to frames with timecodes, scene changes, contact sheet | $2 / 1,000 frames |

Every tool takes public file URLs and a `max_charge_usd` limit per call (default $1), so an agent in a loop cannot
spend more than you allow.

## Set it up

The server is a small Python program that runs the Actors with your own Apify token:

```bash
git clone https://github.com/AndriyVK/-apify-document-tools
cd -- -apify-document-tools/mcp-server
pip install -r requirements.txt
```

Then add it to your MCP client. For Claude Desktop or Cursor the config looks like this:

```json
{
  "mcpServers": {
    "document-tools": {
      "command": "python",
      "args": ["/path/to/-apify-document-tools/mcp-server/server.py"],
      "env": { "APIFY_TOKEN": "<YOUR_APIFY_TOKEN>" }
    }
  }
}
```

The token is in Apify Console, Settings, API & Integrations. New Apify accounts get a free monthly usage credit.

## A real session

To show exactly what an agent receives, I called the server from a plain Python MCP client (the official `mcp`
package, stdio transport), the same way Claude Desktop does it:

```python
import asyncio, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server = StdioServerParameters(command=sys.executable, args=["server.py"],
                                   env={"APIFY_TOKEN": "<YOUR_APIFY_TOKEN>"})
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as s:
            await s.initialize()
            print([t.name for t in (await s.list_tools()).tools])
            r = await s.call_tool("convert_document_to_markdown", {
                "urls": ["https://api.apify.com/v2/key-value-stores/FloomuI2DrQCJazY8/records/scan-uk.pdf"],
                "ocr_languages": ["ukr"], "max_charge_usd": 0.2})
            print(r.content[0].text)

asyncio.run(main())
```

The server answered as `apify-document-tools` 0.3.0 and listed all nine tools.

### Call 1: a scanned Ukrainian page to Markdown

The input is a one-page scan with no text layer (a delivery report with a small table). The call took 8.6 seconds
from the client's side, of which the conversion itself was 0.68 s; the rest is starting the run on Apify. The agent
got this back (shortened):

```json
{
  "fileName": "scan-uk.pdf",
  "sourcePages": 1,
  "textPages": 0,
  "ocrPages": 1,
  "warnings": [],
  "characters": 300,
  "tables": [[["Товар", "Кількість", "Ціна"],
              ["Цемент", "420", "96,50"],
              ["Арматура", "180", "412,00"]]],
  "markdown": "Звіт про постачання\n\nСклад у Львові отримав 1240 палет будівельних матеріалів протягом\n\nтретього кварталу. ..."
}
```

Two things matter for an agent here. First, `ocrPages: 1` and `textPages: 0` tell it the text came from OCR, so it
knows how far to trust it. Second, the table comes back twice: as a Markdown table inside the text and as rows of
cells in `tables`, so the agent can do arithmetic on it without parsing Markdown.

One small flaw is visible: the OCR split one sentence into two paragraphs (`протягом\n\nтретього`). For an LLM this does
not change the meaning, but if you index the text for search, join lines inside paragraphs first.

### Call 2: check two domains

`check_domains` with `["andriyvk.github.io", "dev.to"]` took 4.6 seconds. For each domain the agent gets the
registration (registrar, created and expiry dates, days left), DNS records and the SSL certificate. A shortened piece:

```json
{
  "domain": "andriyvk.github.io",
  "registrableDomain": "github.io",
  "registration": {"source": "whois", "registrar": "MarkMonitor Inc.", "expiresDate": "2027-03-08", "daysUntilExpiry": 113},
  "dns": {"A": ["185.199.108.153", "185.199.109.153", "185.199.110.153", "185.199.111.153"], "MX": []},
  "ssl": {"valid": true, "protocol": "TLSv1.3", "issuer": "Let's Encrypt", "validTo": "2026-12-29", "daysLeft": 44}
}
```

Note `registrableDomain`: for a subdomain the registration data is that of the parent domain (`github.io`), and the
result says so instead of pretending the subdomain has its own WHOIS record. For `dev.to` the data came from RDAP
(registrar Tonic, expires 2027-04-05), with SPF and DMARC records parsed out of TXT.

## Price

For a buyer on a paid plan the two calls above cost:

- scan to Markdown: 1 OCR page $0.004 plus run starts $0.0001 = **$0.0041**;
- two domains: 2 x $0.003 plus a run start $0.00005 = **$0.00605**.

About one cent together. You pay Apify at the Actors' prices; the MCP server itself is free and adds no
fee.

## Limits

- Files must be reachable by a public URL. A local file has to be uploaded somewhere first (for example to an Apify
  key-value store).
- Each call is a synchronous Actor run, and Apify keeps such a run open for at most 300 seconds. A long video or a
  big folder needs to be split into several calls.
- OCR quality depends on the scan. The result says how many pages went through OCR, but it does not check the text
  against the original.
- Apify also offers a hosted MCP endpoint with the same Actors
  (`https://mcp.apify.com?tools=ai_admin/document-to-markdown,...`, full list in the
  [README](https://github.com/AndriyVK/-apify-document-tools/tree/main/mcp-server)). I did not test it for this post;
  the session above is the local server.

## Try it in two minutes

1. Open [Document to Markdown for AI](https://apify.com/ai_admin/document-to-markdown) and press **Try for free**.
2. The input is already filled with a working example: press **Start**, or put in links to your own files.
3. Apify's free plan includes $5 of usage every month - enough to test it on your own data.

## Related posts

- [Ukrainian scanned PDFs to Markdown for RAG and LLMs](/ukrainian-scans-to-markdown/)
- [Office to PDF/A for archives and e-filing](/office-to-pdf-a-archive/)
- [Ukrainian text to speech by API](/ukrainian-text-to-speech-api/)
- [YouTube subtitles in Ukrainian](/youtube-subtitles-in-ukrainian/)
