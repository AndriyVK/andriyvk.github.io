title: YouTube subtitles in Ukrainian - transcript and translated SRT by API
description: Get a YouTube or TikTok video's transcript and Ukrainian subtitles (SRT/VTT) with one API call - real runs with their output, how it works with and without captions, the price and the limits.
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

## TikTok without captions: four real runs

TikTok videos usually have no caption track, so here the audio itself is recognised. Four public videos, one run on
7 November 2026, with Ukrainian translation switched on (`"translateTo": "uk"`):

```python
run_input = {
    "videoUrls": [
        "https://www.tiktok.com/@nasa/video/7698805564884733198",
        "https://www.tiktok.com/@bbcnews/video/7699782697031404822",
        "https://www.tiktok.com/@hromadske.ua/video/7704723523511635221",
        "https://www.tiktok.com/@hromadske.ua/video/7704712902082874645",
    ],
    "translateTo": "uk",
    "subtitles": True,
    "includeSegments": True,
}
```

All four came back with `transcriptSource: speech-recognition`, none failed. The excerpts below are copied from the
output as they are, mistakes included.

**1. NASA, English, 45 seconds, 11 segments.** Clear studio speech, recognised without a single error I could spot:

```text
00:14  Viper very much acts as a scout for Moonbase.
00:19  We've already built three mock-ups, actually two of them within three weeks.
00:37  Our goal is to enable humans to be operating on the surface of the moon on a permanent basis.
```

Ukrainian translation of the last line: «Наша мета - забезпечити можливість для людей працювати на поверхні Місяця на
постійній основі.»

**2. BBC News, English, 35 seconds, 5 segments.** A weather presenter outdoors, in a storm:

```text
00:00  The full force of Storm Austin has arrived here in Newquay and Cornwall.
       We are now seeing gusts of wind of 17, even 18 miles an hour.
00:16  These strong winds have the potential to bring down branches and trees. There could well be power cuts.
00:21  Now the strong winds will move their way a bit further east with drought in the morning ...
```

This is the hard case, and it shows. The storm is called Austen (the video's own hashtag), not Austin. Gusts of
17-18 mph would not bring down trees, and the Met Office forecast for Cornwall that day was 60-70 mph, up to 80 in
exposed places. I cross-checked by running the same video again with `"quality": "fast"` (Whisper large-v3-turbo):
it heard «70, even 80 miles an hour» and «throughout the morning», so «drought», which the translation faithfully
turned into «посуха», is a mishearing too. The second model made its own mistake in the same sentence («just a room
of» instead of «gusts of wind of»). Wind noise is what breaks numbers and short words, so check figures in such videos;
a second run with the other `quality` costs $0.01 and shows where the two disagree.

**3. hromadske, Ukrainian, 74 seconds, 14 segments.** A performer in an interview, conversational speech:

```text
00:00  Я себе ловлю на тому, що мене чіпляє все, що з Росією пов'язано.
00:10  У 22-му році я поїхав в Естонію.
00:15  І я в аеропорту підхожу до гейту і чую позаду мене чокання, акання.
00:51  І буде відчуття несправедливості, і буде нас це тригерить постійно ...
```

Even slang like «тригерить» and «чокання, акання» came through. The language was detected as Ukrainian, so the
translation was skipped with the warning `the video is already in the target language` and no translated minutes were
charged.

**4. hromadske, Ukrainian, 91 seconds, 7 segments.** A calmer interview about the Ukrainian language:

```text
00:00  Захист мови є частиною національної безпеки.
00:08  З того часу, коли росіяни зросифіковували українців, вони діяли страхом, примусом ...
00:19  А з іншого боку, у нас демократична країна, демократичні методи українізації суспільства.
```

One word is wrong: «зросифіковували» should be «русифікували». The rest reads like a clean transcript. The long
segments (up to 20 seconds) follow the speaker's sentences; for subtitles on a phone screen you may want to split them.

What the run cost a user on a paid plan: four videos at $0.01 plus two started minutes of translation at $0.007, so
**$0.054** in total ($0.017 for each English video with translation, $0.01 for each Ukrainian one). Videos up to three
minutes cost the same flat $0.01 with speech recognition as with captions.

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
