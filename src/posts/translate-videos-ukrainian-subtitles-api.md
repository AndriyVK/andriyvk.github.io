title: Translate TikTok, Reels, Facebook and YouTube videos into Ukrainian and 20 more languages - transcript and SRT subtitles by API
description: One API call turns a video link from TikTok, Instagram Reels, Facebook, X or YouTube into a transcript and translated SRT/VTT subtitles in Ukrainian or 20 other languages - even when the video has no captions. Real runs, the output, and what the most used transcript Actors can and cannot do.
date: 2026-11-18
lang: en
slug: translate-videos-ukrainian-subtitles-api
pair: pereklad-video-ukrainskoyu-subtytry
---
Getting the text of a video is easy today. Getting it **translated, with subtitles timed to the video**, for a TikTok
or a Reel without captions is where most tools stop. This post shows a tool that does the whole chain in one call:
download, speech recognition, translation and subtitle files. Every output below is from real runs on 16 November
2026.

> Disclosure: I built the tool, [Video Transcript & Translation](https://apify.com/ai_admin/social-video-transcript)
> on Apify. The code is open: [AndriyVK/-apify-document-tools](https://github.com/AndriyVK/-apify-document-tools).

## One call

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("ai_admin/social-video-transcript").call(run_input={
    "videoUrls": [
        "https://www.tiktok.com/@nasa/video/7698805564884733198",
        "https://www.facebook.com/NASA/videos/360-degree-view-from-the-cupola/346691430131/",
    ],
    "translateTo": "uk",
})
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item["title"], item["translation"]["srtUrl"])
```

## What came back

| Video | Length | Source of the text | Translated into Ukrainian | Subtitles |
|---|---|---|---|---|
| NASA on TikTok: moving around on the Moon | 45 s | speech recognition (no captions) | 13 of 13 lines | SRT and VTT, original and Ukrainian |
| NASA on Facebook: view from the Cupola | 107 s | speech recognition (no captions) | 19 of 19 lines | SRT and VTT, original and Ukrainian |
| YouTube: «Me at the zoo» | 19 s | the video's own captions | 6 of 6 lines | SRT and VTT, original and Ukrainian |

The first lines of the TikTok, as they come in the subtitles - every translated line keeps the timing of the original:

```text
1.0-5.4   Think about hundreds of square miles where we have different assets.
          Подумайте про сотні квадратних миль, де у нас є різні активи.
5.4-7.4   Definitely mobility systems.
          Безумовно, системи мобільності.
7.4-11.7  There's a lot of people who spend a lot of time making sure every detail is right,
          Багато людей витрачають багато часу, щоб переконатися, що кожна деталь правильна,
```

So you can put the Ukrainian SRT next to the video and it lines up without any editing.

## What makes it different

I went through the most used transcript Actors in the Apify Store, their input settings and prices on the entry paid
plan (16 November 2026):

| Actor | Users a month | Platforms | Translation | Works without captions | Price per video |
|---|---|---|---|---|---|
| **ai_admin/social-video-transcript** | new | **YouTube, TikTok, Instagram, Facebook, X and many other sites** | **Ukrainian + 20 languages, with SRT/VTT** | **yes, Whisper large-v3** | **from $0.006** |
| johnvc/YoutubeTranscripts | 6974 | YouTube | YouTube's own machine translation of captions | captions only | $0.0025 |
| steadyfetch/instagram-reel-transcript-scraper | 3859 | Instagram | no translation option | yes | $0.014 |
| afanasenko/instagram-reel-script-extractor | 640 | Instagram | no translation option | - | $0.075 |
| clockworks/tiktok-transcript-extractor | 557 | TikTok | no translation option | yes | $0.003 + $0.041 per minute |
| tubetext/instagram-reels-transcript | 486 | Instagram | no translation option | yes | $0.0095 |
| sian.agency/best-tiktok-ai-transcript-extractor | 158 | several | into English only | - | $0.012 + $0.005 per run |

**By the numbers.** Of the seven most used transcript Actors, this is the only one that translates TikTok, Reels and
Facebook videos into Ukrainian - and into 21 target languages, where the others offer English only or YouTube only.
Every translated line keeps the original timing, missed speech is checked for free, and failed videos are not
charged - so you pay a fair price only for results. And it handles five platforms in one list of links, where most of them handle one.

What that means in practice:

1. **Translation for every platform, into Ukrainian and 20 more languages.** The tools that translate at all either
   work only on YouTube and only when YouTube itself can translate the captions, or translate only into English.
   Of the Instagram and TikTok tools in the table, only one translates, and only into English.
2. **Translated subtitles, not just text.** Ukrainian SRT and VTT files with the original timing, ready for a video
   editor or a player.
3. **All platforms in one tool.** One list of links can mix YouTube, TikTok, Reels, Facebook and X. Most
   alternatives handle one platform.
4. **Works when there are no captions.** The speech is recognised with Whisper large-v3; caption-only YouTube tools
   return nothing for such videos.
5. **Missed speech is checked for free.** Every transcript is checked for stretches where speech was skipped, and
   those places are recognised again.
6. **Failed videos are free.** A private or deleted video gets an error and is not charged.
7. **No API key of your own.** No OpenAI or other account - you pay per video through Apify.

For noisy recordings there is also an optional cross-check: the audio is recognised by a second model and the places
where the two disagree are listed, figures first (recognition is then charged twice).

## Price

| What | Paid plans | Free plan |
|---|---|---|
| One video: captions of any length, or up to 3 minutes of recognised speech | **$0.006** | $0.008 |
| Translation, per started minute of video | $0.007 | $0.01 |

The 45-second TikTok above with its Ukrainian translation costs $0.013 on a paid plan. Subtitles are free.

## Ideas

- **Ukrainian subtitles for foreign videos** in a channel or a course, without typing a line.
- **Monitoring what is said in TikTok and Reels** about a brand or a topic, in your language.
- **Content for AI**: transcripts and translations as text for search, summaries or RAG. The tool is also an MCP tool
  for Claude, Cursor and other agents - see [MCP server for document and media tools](/mcp-document-tools-for-ai-agents/).

Earlier post on the same tool, with captions and noisy audio:
[YouTube subtitles in Ukrainian](/youtube-subtitles-in-ukrainian/).

Which videos would you translate first - TikTok, Reels or YouTube? Tell me in the comments.
