title: Ukrainian text to speech by API — natural voices, MP3 and subtitles
description: Turn Ukrainian text, articles or DOCX/PDF files into natural speech with one API call — three Ukrainian neural voices, MP3 plus SRT, a real run you can listen to, the price and the limits.
date: 2026-11-07
lang: en
slug: ukrainian-text-to-speech-api
pair: ukrainska-ozvuchka-tekstu-api
---
Good Ukrainian voices are rare in text-to-speech APIs: many offer none, and open voices often put the stress on the
wrong syllable. This guide shows one API call that turns Ukrainian text into an MP3 with subtitles, with a sample
you can play right here. The run below is from 7 November 2026.

> Disclosure: I built the tool used here, [Text to Speech](https://apify.com/ai_admin/text-to-speech) on Apify. The
> voices run inside it ([Piper](https://github.com/OHF-Voice/piper1-gpl) neural models), so no other service and no
> key of yours is involved. The source code is open:
> [AndriyVK/-apify-document-tools](https://github.com/AndriyVK/-apify-document-tools).

## Listen first

<audio controls preload="none" src="/assets/audio/tts-uk-tetiana.mp3"></audio>

Voice `uk_UA-tetiana-high`, speed 1.12, MP3. This is the file exactly as the API returned it, not edited.

## The call

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("ai_admin/text-to-speech").call(run_input={
    "text": "Добрий день! Це український голос, створений нейромережею.\n\n"
            "Він читає статті, документи та субтитри природно і без акценту.",
    "voice": "uk_UA-tetiana-high",   # or uk_UA-mykyta-high, uk_UA-oleksa-high
    "speed": 1.12,
    "format": "mp3",                 # mp3, wav or ogg
    "subtitles": True,               # SRT and VTT, free
})
item = next(client.dataset(run["defaultDatasetId"]).iterate_items())
print(item["durationSeconds"], item["audioUrl"], item["srtUrl"])
```

Instead of `text` you can pass `sources`: links to TXT, Markdown, HTML, DOCX or PDF files (with a text layer), one
audio file each.

## The real output

```text
voice: uk_UA-tetiana-high   characters: 120   sentences: 3   durationSeconds: 10.59
```

And the subtitles that came with it — one cue per sentence, timed to the audio:

```text
1
00:00:00,000 --> 00:00:01,068
Добрий день!

2
00:00:01,291 --> 00:00:04,240
Це український голос, створений нейромережею.

3
00:00:04,865 --> 00:00:10,589
Він читає статті, документи та субтитри природно і без акценту.
```

The whole run took 30 seconds, most of it the container start. As a rule of thumb, 750–900 characters make one minute
of speech.

## Price

Per started minute of audio: **$40 per 1,000 minutes with the `high` voices** (4 cents a minute) and $10 per 1,000
with `medium`/`low` voices. All three Ukrainian voices are `high`. The sample above is one started minute — 4 cents.
Subtitles are free.

## Limits

- Numbers, abbreviations and foreign words are read by the voice's rules and may sound odd: write «двадцять п'ять»
  or check how «25» sounds.
- Scanned PDFs without a text layer are not read — run them through OCR first (see
  [Ukrainian scans to Markdown](/ukrainian-scans-to-markdown/)).
- It is a synthetic voice. For an audiobook it is fine for drafts and accessibility; a professional narrator is still
  better for a final release.

## From an AI agent

`https://mcp.apify.com?tools=ai_admin/text-to-speech` adds the voice as an MCP tool, so an agent can write a text and
hand back the audio.
