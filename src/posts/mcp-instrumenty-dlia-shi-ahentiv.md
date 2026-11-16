title: MCP-сервер для ШІ-агентів - OCR, PDF, аудіо і перевірка доменів для Claude чи Cursor
description: Один MCP-сервер дає ШІ-агенту 9 інструментів - документи і скани в Markdown, Office у PDF/A, OCR, розпізнавання та озвучування мовлення, знімки сайтів, перевірка доменів, кадри з відео. Справжні виклики з клієнта MCP, результат, ціна та обмеження.
date: 2026-11-15
lang: uk
slug: mcp-instrumenty-dlia-shi-ahentiv
pair: mcp-document-tools-for-ai-agents
---
ШІ-агент добре працює з текстом, але справжня робота часто приходить файлами: скан рахунку, таблиця, голосове
повідомлення, сайт, який треба перевірити. Протокол MCP (Model Context Protocol) дозволяє агенту викликати для цього
інструменти. Тут - один MCP-сервер, що дає Claude, Cursor чи будь-якому іншому клієнту MCP дев'ять таких
інструментів, і що повернули два з них, коли клієнт MCP викликав їх 15 листопада 2026 року.

> Розкриття: сервер і Actors на Apify, що стоять за ним, зробив я. Код відкритий (MIT):
> [AndriyVK/-apify-document-tools](https://github.com/AndriyVK/-apify-document-tools/tree/main/mcp-server).

## Інструменти

| Інструмент | Що робить | Ціна (списує Apify) |
|---|---|---|
| `convert_document_to_markdown` | PDF (текстові та скани, OCR), зображення, DOCX/DOC, XLSX/XLS, PPTX/PPT, ODT, RTF, HTML у Markdown, таблиці JSON, фрагменти для RAG | $1 за 1000 текстових сторінок, $4 за 1000 сторінок з OCR |
| `convert_office_to_pdf` | Word, Excel, PowerPoint, OpenDocument, RTF, HTML, зображення у PDF або PDF/A-2b, за бажанням в один файл | $10 за 1000 документів |
| `convert_pdf_or_images` | сторінки PDF у PNG/JPG/WebP/TIFF, зображення в PDF, HEIC з iPhone у JPG, зміна розміру | $2 за 1000 зображень |
| `transcribe_audio` | аудіо та відео в текст, фрагменти з часом, SRT/VTT (Whisper large-v3) | $5 за 1000 хвилин |
| `ocr_images` | зображення та скани в текст, рядки з упевненістю та координатами | $4 за 1000 зображень |
| `text_to_speech` | текст або PDF/DOCX/HTML у MP3/WAV/OGG та субтитри SRT, є українські голоси | $10 за 1000 хвилин аудіо |
| `screenshot_website` | знімки сторінки на всю довжину або PDF сайту чи свого HTML | $4 за 1000 сторінок |
| `check_domains` | WHOIS/RDAP (реєстратор, термін), записи DNS, термін сертифіката SSL | $2 за 1000 доменів |
| `extract_video_frames` | кадри з відео з часовими мітками, зміни сцен, аркуш мініатюр | $1 за 1000 кадрів |

Кожен інструмент приймає публічні посилання на файли та ліміт `max_charge_usd` на виклик (типово $1), тож агент у
циклі не витратить більше, ніж ви дозволили.

## Як підключити

Сервер - невелика програма на Python, яка запускає Actors з вашим власним токеном Apify:

```bash
git clone https://github.com/AndriyVK/-apify-document-tools
cd -- -apify-document-tools/mcp-server
pip install -r requirements.txt
```

Потім додайте його у свій клієнт MCP. Для Claude Desktop чи Cursor налаштування таке:

```json
{
  "mcpServers": {
    "document-tools": {
      "command": "python",
      "args": ["/path/to/-apify-document-tools/mcp-server/server.py"],
      "env": { "APIFY_TOKEN": "<ВАШ_ТОКЕН_APIFY>" }
    }
  }
}
```

Токен - в Apify Console, Settings, API & Integrations. Нові акаунти Apify щомісяця отримують безкоштовний кредит.

## Справжній сеанс

Щоб показати, що саме отримує агент, я викликав сервер зі звичайного клієнта MCP на Python (офіційний пакет `mcp`,
транспорт stdio) - так само, як це робить Claude Desktop:

```python
import asyncio, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server = StdioServerParameters(command=sys.executable, args=["server.py"],
                                   env={"APIFY_TOKEN": "<ВАШ_ТОКЕН_APIFY>"})
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

Сервер відповів як `apify-document-tools` 0.3.0 і показав усі дев'ять інструментів.

### Виклик 1: скан українською в Markdown

На вході - скан однієї сторінки без текстового шару (звіт про постачання з невеликою таблицею). Виклик тривав 8,6 с
з боку клієнта, з них саме перетворення - 0,68 с; решта - запуск на Apify. Агент отримав (скорочено):

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

Для агента тут важливі дві речі. Перша: `ocrPages: 1` і `textPages: 0` кажуть, що текст отримано через OCR, тож агент
знає, наскільки йому довіряти. Друга: таблиця приходить двічі - як таблиця Markdown у тексті та як рядки клітинок у
`tables`, тож агент може рахувати з неї, не розбираючи Markdown.

Видно й невелику ваду: OCR розбив одне речення на два абзаци (`протягом\n\nтретього`). Для мовної моделі зміст від
цього не змінюється, але якщо текст іде в пошуковий індекс, спершу з'єднайте рядки всередині абзаців.

### Виклик 2: перевірка двох доменів

`check_domains` з `["andriyvk.github.io", "dev.to"]` тривав 4,6 с. Для кожного домену агент отримує реєстрацію
(реєстратор, дати створення і закінчення, скільки днів лишилося), записи DNS і сертифікат SSL. Фрагмент:

```json
{
  "domain": "andriyvk.github.io",
  "registrableDomain": "github.io",
  "registration": {"source": "whois", "registrar": "MarkMonitor Inc.", "expiresDate": "2027-03-08", "daysUntilExpiry": 113},
  "dns": {"A": ["185.199.108.153", "185.199.109.153", "185.199.110.153", "185.199.111.153"], "MX": []},
  "ssl": {"valid": true, "protocol": "TLSv1.3", "issuer": "Let's Encrypt", "validTo": "2026-12-29", "daysLeft": 44}
}
```

Зверніть увагу на `registrableDomain`: для піддомену дані реєстрації - це дані батьківського домену (`github.io`), і
результат прямо це показує, а не вдає, що в піддомену є власний запис WHOIS. Для `dev.to` дані прийшли з RDAP
(реєстратор Tonic, термін до 2027-04-05), а SPF і DMARC виділено із записів TXT.

## Ціна

Для покупця два виклики вище коштували:

- скан у Markdown: 1 сторінка з OCR $0,004 плюс запуск $0,0001 = **$0,0041**;
- два домени: 2 x $0,002 плюс запуск $0,00005 = **$0,00405**.

Разом - близько восьми десятих цента. Платите Apify за цінами Actors; сам MCP-сервер безкоштовний і нічого не додає.

## Обмеження

- Файли мають бути доступні за публічним посиланням. Локальний файл спершу треба кудись вивантажити (наприклад, у
  сховище key-value store на Apify).
- Кожен виклик - синхронний запуск Actor, а Apify тримає такий запуск відкритим не довше 300 с. Довге відео чи велику
  теку треба ділити на кілька викликів.
- Якість OCR залежить від скану. Результат каже, скільки сторінок пройшли через OCR, але не звіряє текст з
  оригіналом.
- Apify має й розміщену точку MCP з тими самими Actors
  (`https://mcp.apify.com?tools=ai_admin/document-to-markdown,...`, повний список - у
  [README](https://github.com/AndriyVK/-apify-document-tools/tree/main/mcp-server)). Для цієї статті я її не
  перевіряв; сеанс вище - з локальним сервером.

## Інші статті

- [Скани українською в Markdown для ШІ](/uk/skany-ukrainskoyu-v-markdown/)
- [Word, Excel і PowerPoint у PDF/A для архіву та суду](/uk/office-v-pdf-a-sud-arkhiv/)
- [Українська озвучка тексту через API](/uk/ukrainska-ozvuchka-tekstu-api/)
- [Субтитри YouTube українською](/uk/subtytry-youtube-ukrainskoyu/)
