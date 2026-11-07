# andriyvk.github.io

Blog and guides about open-source document, audio and web tools by AndriyVK -
[Apify Actors](https://apify.com/ai_admin) and their source code in
[AndriyVK/-apify-document-tools](https://github.com/AndriyVK/-apify-document-tools).

Live at https://andriyvk.github.io/

## How it is built

Posts are Markdown files in `src/posts/`; `python build.py` (needs `pip install markdown==3.7`) writes the HTML pages,
`sitemap.xml`, `feed.xml` and `robots.txt`. GitHub Pages serves the built files as they are (`.nojekyll`).
Visits are counted with GoatCounter (no cookies).
