import json, re, sys, urllib.request
SITE = 'https://andriyvk.github.io'
TAGS = {
    'ukrainian-scans-to-markdown': ['ocr', 'python', 'rag', 'ai'],
    'office-to-pdf-a-archive': ['pdf', 'python', 'api', 'productivity'],
    'ukrainian-text-to-speech-api': ['tts', 'python', 'api', 'ukrainian'],
    'youtube-subtitles-in-ukrainian': ['youtube', 'python', 'api', 'ai'],
}
def load(slug):
    head, body = open(f'/home/user/andriyvk.github.io/src/posts/{slug}.md', encoding='utf-8').read().split('\n---\n', 1)
    meta = dict(l.split(': ', 1) for l in head.splitlines() if ': ' in l)
    body = re.sub(r'<audio[^>]*src="([^"]+)"[^>]*></audio>', lambda m: f'[▶ Listen to the MP3 sample]({SITE}{m.group(1)})', body)
    body = re.sub(r'\]\((/[^)]*)\)', lambda m: f']({SITE}{m.group(1)})', body)
    body += f'\n\n---\n*Originally published at [{SITE.split("//")[1]}]({SITE}/{slug}/).*\n'
    return meta, body
def call(method, path, data=None):
    req = urllib.request.Request('https://dev.to/api' + path, method=method,
        data=json.dumps(data).encode() if data is not None else None,
        headers={'accept': 'application/vnd.forem.api-v1+json', 'api-key': 'proxy-injected',
                 'Content-Type': 'application/json', 'User-Agent': 'andriyvk-blog-crosspost'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)
if __name__ == '__main__':
    slug, published = sys.argv[1], sys.argv[2] == 'publish'
    meta, body = load(slug)
    art = {'title': meta['title'], 'body_markdown': body, 'published': published, 'tags': TAGS[slug],
           'canonical_url': f'{SITE}/{slug}/', 'description': meta['description'][:250]}
    if len(sys.argv) > 3:
        r = call('PUT', f'/articles/{sys.argv[3]}', {'article': art})
    else:
        r = call('POST', '/articles', {'article': art})
    print(r['id'], r.get('published'), r.get('url'), r.get('canonical_url'))
