title: Transcribe audio and podcasts by API - word timestamps, translation into 21 languages and a free summary
description: One API call turns MP3, WAV, M4A or video files and podcast RSS feeds into text, timed segments, SRT/VTT subtitles, every word with its time, a translation and a summary with action items. Real runs in Ukrainian and English, and what each option costs.
date: 2026-11-28
lang: en
slug: transcribe-audio-podcasts-api
pair: rozshyfrovka-audio-podkastiv-api
---
A meeting recording, an interview, a podcast episode, a lecture - most of the time you need more than the words.
You need the words **with their times**, subtitles, a translation for a colleague and a short summary of what was
decided. This post shows a tool that returns all of that from one call. Every output below is from real runs on
26 November 2026.

> Disclosure: I built the tool, [Audio & Video Transcriber](https://apify.com/ai_admin/audio-transcriber) on Apify.
> The code is open: [AndriyVK/-apify-document-tools](https://github.com/AndriyVK/-apify-document-tools).

## One call

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("ai_admin/audio-transcriber").call(run_input={
    "sources": [{"url": "https://api.apify.com/v2/key-value-stores/FloomuI2DrQCJazY8/records/speech-en.mp3"}],
    "podcastFeeds": ["https://api.apify.com/v2/key-value-stores/FloomuI2DrQCJazY8/records/test-podcast.xml"],
    "maxEpisodesPerFeed": 2,
    "translateTo": "uk",
    "wordTimestamps": True,
    "summarize": True,
})
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item["language"], item["text"])
    print(item["summary"]["actionItems"])
```

The run had two files and a podcast feed with two episodes, in English and Ukrainian, and took 22 seconds. The
language of each file was detected automatically.

## What came back

**The transcript**, as text and as timed segments, plus SRT and VTT subtitle files:

```text
0.0-6.0    The warehouse in Lviv received 1,240 pallets of building materials during the third quarter.
6.0-10.7   Delivery times improved by 12% after the new routing schedule was introduced.
```

The Ukrainian file came back word for word: «Склад у Львові отримав 1240 палет будівельних матеріалів протягом
третього кварталу». City names are spelled right even when the language is not set: if a word looks like a
misheard place name, that part is recognised again with the names as a hint.

**Every word with its time** - for karaoke captions, search inside a recording or cutting a clip:

```json
[{"start": 0.0, "end": 0.14, "word": "The"}, {"start": 0.14, "end": 0.56, "word": "warehouse"},
 {"start": 0.56, "end": 0.76, "word": "in"}, {"start": 0.76, "end": 1.14, "word": "Lviv"}]
```

**The translation**, with its own SRT and VTT files on the original timing:

```text
Склад у Львові отримав 1240 палет будівельних матеріалів у третьому кварталі.
```

**A summary with key points and action items:**

```json
{
  "summary": "The Lviv warehouse handled 1,240 pallets of building materials in the third quarter. Delivery times improved by 12% after implementing a new routing schedule...",
  "keyPoints": ["Lviv warehouse received 1,240 pallets in Q3.", "Delivery times improved by 12% as a result.", "..."],
  "actionItems": ["Arrange the cement and steel rods shipment for early December."]
}
```

**Podcast episodes** come with the podcast title, the episode title and the date:

```json
{"podcastTitle": "Test podcast (synthetic)", "episodeTitle": "Episode 1: English sample",
 "publishedAt": "2026-11-23T09:00:00+00:00", "durationSeconds": 44.75}
```

## What it does

- **Whisper large-v3**, 99 languages including Ukrainian; `quality: "fast"` switches to large-v3-turbo at the same
  price.
- **Audio and video in:** MP3, WAV, M4A, AAC, OGG, OPUS, FLAC, MP4, MOV, MKV, WebM, AVI. Long files are split
  automatically.
- **Podcasts by RSS:** give the feed, and the newest episodes are transcribed with their titles and dates.
- **Free extras:** SRT and VTT subtitles, every word with its time, and the summary with key points and action items.
- **Translation into 21 languages**, transcript and subtitles. If the audio is already in that language, nothing is
  translated and nothing is charged - the output says so in a note.
- **Your own terms:** `vocabulary` takes names and spellings that appear in the recording.
- **Cross-check for noisy audio:** the recording is recognised again by the second model and the places where the two
  disagree are listed with their times.
- **Failed files are free.**

## Price

| What | Paid plans (Bronze) | Free plan | Gold and higher |
|---|---|---|---|
| One started minute of audio | $0.006 | $0.007 | $0.005 |
| Translation, per minute | one more audio minute | | |

Subtitles, word times and the summary are included. A fair price, with no hidden extras: a 45-second file with its
Ukrainian translation, subtitles, word times and summary is 2 minutes, $0.012 on Bronze.

## Ideas

- **Meeting notes** with decisions and tasks, straight from the recording.
- **Podcast archives** as searchable text, one record per episode, ready for RAG.
- **Subtitles and translations** for interviews and lectures.
- **AI agents**: the tool is also an MCP tool for Claude, Cursor and others - see
  [MCP server for document and media tools](/mcp-document-tools-for-ai-agents/). For TikTok, Reels and YouTube links,
  see [Translate videos into Ukrainian and 20 more languages](/translate-videos-ukrainian-subtitles-api/).

What would you transcribe first - meetings, interviews or podcasts? Tell me in the comments.

## Try it in two minutes

1. Open [Audio & Video Transcriber](https://apify.com/ai_admin/audio-transcriber) and press **Try for free**.
2. The input is already filled with a working example: press **Start**, or put in links to your own files.
3. Apify's free plan includes $5 of usage every month - enough to test it on your own data.
