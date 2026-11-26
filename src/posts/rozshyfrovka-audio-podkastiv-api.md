title: Розшифровка аудіо й подкастів через API - час кожного слова, переклад 21 мовою і безкоштовний підсумок
description: Один виклик API перетворює MP3, WAV, M4A, відео і RSS-стрічки подкастів на текст, сегменти з часом, субтитри SRT/VTT, кожне слово з його часом, переклад і підсумок із завданнями. Справжні запуски українською та англійською і скільки коштує кожна опція.
date: 2026-11-28
lang: uk
slug: rozshyfrovka-audio-podkastiv-api
pair: transcribe-audio-podcasts-api
---
Запис наради, інтерв'ю, випуск подкасту, лекція - найчастіше потрібні не лише слова. Потрібні слова **з їхнім часом**,
субтитри, переклад для колеги і короткий підсумок того, що вирішили. Тут - інструмент, що повертає все це одним
викликом. Усі результати нижче - зі справжніх запусків 26 листопада 2026 року.

> Розкриття: інструмент зробив я, [Audio & Video Transcriber](https://apify.com/ai_admin/audio-transcriber) на Apify.
> Код відкритий: [AndriyVK/-apify-document-tools](https://github.com/AndriyVK/-apify-document-tools).

## Один виклик

```python
from apify_client import ApifyClient

client = ApifyClient("<ВАШ_ТОКЕН_APIFY>")
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

У запуску були два файли і стрічка подкасту з двома випусками, англійською та українською, і він тривав 22 секунди.
Мову кожного файлу визначено автоматично.

## Що повернулося

**Розшифровка** - текстом і сегментами з часом, плюс файли субтитрів SRT і VTT:

```text
0.0-6.0    The warehouse in Lviv received 1,240 pallets of building materials during the third quarter.
6.0-10.7   Delivery times improved by 12% after the new routing schedule was introduced.
```

Український файл повернувся з правильними назвами й числами: «Склад у Львові отримав 1240 палет будівельних матеріалів протягом
третього кварталу». Назви міст пишуться правильно, навіть коли мову не задано: якщо слово схоже на неправильно
почуту назву міста, цей фрагмент розпізнається ще раз із підказкою назв.

**Кожне слово з його часом** - для караоке-субтитрів, пошуку всередині запису чи вирізання фрагмента:

```json
[{"start": 0.0, "end": 0.14, "word": "The"}, {"start": 0.14, "end": 0.56, "word": "warehouse"},
 {"start": 0.56, "end": 0.76, "word": "in"}, {"start": 0.76, "end": 1.14, "word": "Lviv"}]
```

**Переклад** - з власними файлами SRT і VTT на часі оригіналу:

```text
Склад у Львові отримав 1240 палет будівельних матеріалів у третьому кварталі.
```

**Підсумок із головними пунктами і завданнями:**

```json
{
  "summary": "The Lviv warehouse handled 1,240 pallets of building materials in the third quarter. Delivery times improved by 12% after implementing a new routing schedule...",
  "keyPoints": ["Lviv warehouse received 1,240 pallets in Q3.", "Delivery times improved by 12% as a result.", "..."],
  "actionItems": ["Arrange the cement and steel rods shipment for early December."]
}
```

**Випуски подкасту** приходять із назвою подкасту, назвою випуску і датою:

```json
{"podcastTitle": "Test podcast (synthetic)", "episodeTitle": "Episode 1: English sample",
 "publishedAt": "2026-11-23T09:00:00+00:00", "durationSeconds": 44.75}
```

## Що він уміє

- **Whisper large-v3**, 99 мов, зокрема українська; `quality: "fast"` вмикає large-v3-turbo за тією самою ціною.
- **На вході аудіо й відео:** MP3, WAV, M4A, AAC, OGG, OPUS, FLAC, MP4, MOV, MKV, WebM, AVI. Довгі файли діляться
  автоматично.
- **Подкасти через RSS:** дайте стрічку, і найновіші випуски буде розшифровано з назвами й датами.
- **Безкоштовно:** субтитри SRT і VTT, кожне слово з його часом і підсумок із головними пунктами та завданнями.
- **Переклад 21 мовою** - текст і субтитри. Якщо аудіо вже цією мовою, нічого не перекладається і не оплачується, а
  у результаті про це є примітка.
- **Ваші терміни:** у `vocabulary` можна вписати імена й написання, що трапляються в записі.
- **Звірка для шумних записів:** запис розпізнається ще раз другою моделлю, і місця, де дві розшифровки
  розходяться, показуються списком із часом.
- **Невдалі файли безкоштовні.**

## Ціна

| Що | Платні плани (Bronze) | Безкоштовний план | Gold і вище |
|---|---|---|---|
| Одна розпочата хвилина аудіо | $0,006 | $0,007 | $0,005 |
| Переклад, за хвилину | ще одна хвилина аудіо | | |

Субтитри, час слів і підсумок входять у ціну. Справедлива ціна, без прихованих доплат: файл на 45 секунд з
українським перекладом, субтитрами, часом слів і підсумком - це 2 хвилини, $0,012 на Bronze.

## Ідеї

- **Протоколи нарад** з рішеннями й завданнями - прямо із запису.
- **Архіви подкастів** як текст для пошуку, один запис на випуск, готово для RAG.
- **Субтитри й переклади** для інтерв'ю та лекцій.
- **ШІ-агенти:** інструмент є й інструментом MCP для Claude, Cursor та інших - див.
  [MCP-сервер для ШІ-агентів](/uk/mcp-instrumenty-dlia-shi-ahentiv/). Для посилань на TikTok, Reels і YouTube - див.
  [Переклад відео українською та ще 20 мовами](/uk/pereklad-video-ukrainskoyu-subtytry/).

Що б ви розшифрували першим - наради, інтерв'ю чи подкасти? Напишіть у коментарях.

## Спробувати за дві хвилини

1. Відкрийте [Audio & Video Transcriber](https://apify.com/ai_admin/audio-transcriber) і натисніть **Try for free**.
2. Поле вводу вже заповнене робочим прикладом: натисніть **Start** або вставте посилання на власні файли.
3. Безкоштовний план Apify щомісяця дає $5 на використання - цього досить, щоб перевірити інструмент на своїх даних.
