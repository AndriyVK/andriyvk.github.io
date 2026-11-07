"""Build the static site from src/ into the repository root (GitHub Pages serves it as is, .nojekyll).
Usage: python build.py   (needs: pip install markdown==3.7)
Posts: src/posts/*.md with a header of 'key: value' lines, then a line '---', then Markdown.
Keys: title, description, date (YYYY-MM-DD), lang (en|uk), slug, pair (slug of the same post in the other language)."""
import datetime
import html
import json
import os
import re
import shutil

import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://andriyvk.github.io'
NAME = 'AndriyVK Tools'
GOAT = ('<script data-goatcounter="https://andriyvk.goatcounter.com/count" '
        'async src="//gc.zgo.at/count.js"></script>')
TEXT = {
    'en': {'home': 'Guides', 'tagline': 'Practical guides to open-source tools for documents, audio, video and the web - '
           'with real outputs, prices and limits.', 'read': 'Read', 'other': 'Українською', 'posts': 'Guides',
           'tools': 'Tools', 'about': 'Every guide is tested on real files. I build the Apify Actors shown here; '
           'their source code is open on GitHub.'},
    'uk': {'home': 'Інструкції', 'tagline': 'Практичні інструкції до відкритих інструментів для документів, звуку, '
           'відео та вебу - з реальними результатами, цінами й обмеженнями.', 'read': 'Читати', 'other': 'English',
           'posts': 'Інструкції', 'tools': 'Інструменти', 'about': 'Кожну інструкцію перевірено на справжніх файлах. '
           'Apify Actors, про які тут ідеться, зробив я; їхній код відкритий на GitHub.'},
}
TOOLS = [
    ('Document to Markdown for AI', 'https://apify.com/ai_admin/document-to-markdown'),
    ('Office to PDF & PDF/A', 'https://apify.com/ai_admin/office-to-pdf'),
    ('Image to Text OCR', 'https://apify.com/ai_admin/image-to-text-ocr'),
    ('Audio & Video Transcriber', 'https://apify.com/ai_admin/audio-transcriber'),
    ('Video Transcript & Translation', 'https://apify.com/ai_admin/social-video-transcript'),
    ('Text to Speech', 'https://apify.com/ai_admin/text-to-speech'),
    ('PDF to Image & Image Converter', 'https://apify.com/ai_admin/pdf-image-converter'),
    ('Website Screenshot & HTML to PDF', 'https://apify.com/ai_admin/website-screenshot'),
    ('Domain WHOIS, DNS & SSL', 'https://apify.com/ai_admin/domain-whois-dns-ssl'),
    ('Video Frame Extractor', 'https://apify.com/ai_admin/video-frame-extractor'),
]


def read_post(path):
    head, body = open(path, encoding='utf-8').read().split('\n---\n', 1)
    meta = dict(line.split(': ', 1) for line in head.strip().splitlines())
    meta['body'] = body
    return meta


def url_of(p):
    return f"/{'uk/' if p['lang'] == 'uk' else ''}{p['slug']}/"


def page(lang, title, description, canonical, content, alternates=(), extra_head=''):
    alt = ''.join(f'<link rel="alternate" hreflang="{lg}" href="{SITE}{u}">' for lg, u in alternates)
    other = next((u for lg, u in alternates if lg != lang), '/uk/' if lang == 'en' else '/')
    t = TEXT[lang]
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{SITE}{canonical}">{alt}
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{SITE}{canonical}">
<meta property="og:type" content="article">
<link rel="alternate" type="application/rss+xml" title="{NAME}" href="{SITE}/feed.xml">
<link rel="stylesheet" href="/assets/style.css">{extra_head}
</head>
<body>
<header class="top"><a class="brand" href="{'/uk/' if lang == 'uk' else '/'}">{NAME}</a>
<nav><a href="{other}">{t['other']}</a> <a href="https://github.com/AndriyVK/-apify-document-tools">GitHub</a></nav></header>
<main>
{content}
</main>
<footer><p>{t['about']}</p>
<p><a href="https://apify.com/ai_admin">Apify Store</a> · <a href="https://github.com/AndriyVK/-apify-document-tools">GitHub</a> · <a href="/feed.xml">RSS</a></p></footer>
{GOAT}
</body>
</html>
'''


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


LONG_DASHES = ('\u2014', '\u2013')   # owner's rule: only the short "-" on the site


def main():
    for n in sorted(os.listdir(os.path.join(ROOT, 'src/posts'))):
        text = open(os.path.join(ROOT, 'src/posts', n), encoding='utf-8').read()
        if any(d in text for d in LONG_DASHES):
            raise SystemExit(f'{n}: long dash found, use "-"')
    posts = sorted((read_post(os.path.join(ROOT, 'src/posts', n)) for n in os.listdir(os.path.join(ROOT, 'src/posts'))
                    if n.endswith('.md')), key=lambda p: p['date'], reverse=True)
    by_slug = {p['slug']: p for p in posts}
    for lang in ('en', 'uk'):  # old builds: remove generated post folders, then write again
        base = os.path.join(ROOT, 'uk') if lang == 'uk' else ROOT
        if os.path.isdir(base):
            for n in os.listdir(base):
                if os.path.isfile(os.path.join(base, n, '.generated')):
                    shutil.rmtree(os.path.join(base, n))
    md = markdown.Markdown(extensions=['fenced_code', 'tables', 'toc'])
    for p in posts:
        md.reset()
        body = md.convert(p['body'])
        alts = [(p['lang'], url_of(p))]
        if p.get('pair') in by_slug:
            alts.append((by_slug[p['pair']]['lang'], url_of(by_slug[p['pair']])))
        d = datetime.date.fromisoformat(p['date'])
        ld = json.dumps({'@context': 'https://schema.org', '@type': 'TechArticle', 'headline': p['title'],
                         'description': p['description'], 'datePublished': p['date'], 'inLanguage': p['lang'],
                         'author': {'@type': 'Person', 'name': 'AndriyVK', 'url': 'https://github.com/AndriyVK'}},
                        ensure_ascii=False)
        content = (f'<article><p class="date">{d:%d.%m.%Y}</p><h1>{html.escape(p["title"])}</h1>'
                   f'<p class="lead">{html.escape(p["description"])}</p>{body}</article>')
        rel = url_of(p).strip('/')
        write(f'{rel}/index.html', page(p['lang'], p['title'], p['description'], url_of(p), content, alts,
                                       f'\n<script type="application/ld+json">{ld}</script>'))
        write(f'{rel}/.generated', '')
    for lang in ('en', 'uk'):
        t = TEXT[lang]
        items = ''.join(f'<li><a href="{url_of(p)}"><strong>{html.escape(p["title"])}</strong></a>'
                        f'<p>{html.escape(p["description"])}</p></li>' for p in posts if p['lang'] == lang)
        tools = ''.join(f'<li><a href="{u}">{html.escape(n)}</a></li>' for n, u in TOOLS)
        content = (f'<h1>{t["home"]}</h1><p class="lead">{t["tagline"]}</p><h2>{t["posts"]}</h2>'
                   f'<ul class="posts">{items}</ul><h2>{t["tools"]}</h2><ul class="tools">{tools}</ul>')
        home = '/uk/' if lang == 'uk' else '/'
        write(('uk/' if lang == 'uk' else '') + 'index.html',
              page(lang, f'{NAME} - {t["home"]}', t['tagline'], home, content, [('en', '/'), ('uk', '/uk/')]))
    urls = ['/', '/uk/'] + [url_of(p) for p in posts]
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + ''.join(f'<url><loc>{SITE}{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
    rss = ''.join(f'<item><title>{html.escape(p["title"])}</title><link>{SITE}{url_of(p)}</link>'
                  f'<guid>{SITE}{url_of(p)}</guid><description>{html.escape(p["description"])}</description>'
                  f'<pubDate>{datetime.date.fromisoformat(p["date"]):%a, %d %b %Y} 08:00:00 +0000</pubDate></item>\n'
                  for p in posts)
    write('feed.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>{NAME}</title>'
          f'<link>{SITE}/</link><description>{html.escape(TEXT["en"]["tagline"])}</description>\n{rss}</channel></rss>\n')
    write('.nojekyll', '')
    write('404.html', page('en', 'Not found', 'Page not found', '/404.html',
                           '<h1>Not found</h1><p><a href="/">Guides</a> · <a href="/uk/">Інструкції</a></p>'))
    print(f'built {len(posts)} posts, {len(urls)} urls')


if __name__ == '__main__':
    main()
