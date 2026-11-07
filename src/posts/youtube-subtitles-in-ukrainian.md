title: YouTube subtitles in Ukrainian - transcript and translated SRT by API
description: Get a YouTube video's transcript and Ukrainian subtitles (SRT/VTT) with one API call - a real run with its output, how it works with and without captions, the price and the limits.
date: 2026-11-07
lang: en
slug: youtube-subtitles-in-ukrainian
pair: subtytry-youtube-ukrainskoyu
---
Plenty of tools fetch a YouTube transcript. Fewer give you **subtitles in Ukrainian**, timed to the video, ready to
load into a player or an editor. This guide shows one call that returns the original transcript, its Ukrainian
translation and both as SRT/VTT files. The output below is from a real run on 7 November 2026.

> Disclosure: I built the tool used here, [Video Transcript & Translation](https://apify.com/ai_admin/social-video-transcript)
> on Apify. The source code is open: [AndriyVK/-apify-document-tools](https://github.com/AndriyVK/-apify-document-tools).

## The call

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("ai_admin/social-video-transcript").call(run_input={
    "videoUrls": ["https://www.youtube.com/watch?v=jNQXAC9IVRw"],
    "translateTo": "uk",      # Ukrainian; 20 more languages are available
    "subtitles": True,        # SRT and VTT, original and translation (free)
})
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item["title"], item["transcriptSource"])
    print(item["translation"]["text"])
    print(item["translation"]["srtUrl"])
```

The same list takes TikTok, Instagram Reels, Facebook, X and Vimeo links.

## The real output

The video is the first one ever uploaded to YouTube, «Me at the zoo» (19 seconds).

```text
title: Me at the zoo   language: en   transcriptSource: uploaded-captions   seconds: 18.2
```

The Ukrainian SRT file (first three cues):

```text
1
00:00:01,200 --> 00:00:03,360
Гаразд, тож ми тут, перед слонами

2
00:00:05,320 --> 00:00:07,970
круте в цих тварин те, що у них справді...

3
00:00:07,970 --> 00:00:12,620
справді дуже довгі хоботи
```

Each translated cue keeps the timing of the original one, so the file lines up with the video without any editing.
The translation is natural Ukrainian («довгі хоботи», not a word-for-word copy), and even the elephant sound
`(baaaaaaaaaaahhh!!)` became `(бааааааааа!!)`.

## Captions or speech recognition

- **The video has captions** (uploaded or YouTube's automatic ones): they are used. Fast, any length, one flat
  price. That was the case above: `uploaded-captions`.
- **No captions:** the audio is recognised with Whisper large-v3, which handles Ukrainian well. Then you pay per
  minute, and `maxDurationMinutes` (60 by default) keeps you from transcribing a four-hour stream by accident.

## Price

On a paid Apify plan: **$10 per 1,000 videos** with captions, plus **$7 per 1,000 minutes** translated. The video
above: one video plus one started minute of translation, $0.017. On the free plan: $0.025. A YouTube video without
captions is $10 per 1,000 minutes instead. Failed videos are free.

## Limits

- Private videos, videos that need a login and live streams are not supported.
- YouTube sometimes refuses downloads from servers; such a video gets an `error` field and is not charged.
- Speakers are not labelled.
- The translation is done by a language model: good for watching and searching, but read it before you publish it
  as official subtitles.
- Transcribe and translate only videos you are allowed to use.

## From an AI agent

`https://mcp.apify.com?tools=ai_admin/social-video-transcript` gives Claude, Cursor or any MCP client one tool that
reads a video link and answers in text.
