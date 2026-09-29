#!/usr/bin/env python3
"""Build the production homepage from the approved V5.1 source. Standard library only."""
from pathlib import Path
import argparse
import html
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--content', type=Path, default=ROOT / 'content.json')
parser.add_argument('--output', type=Path, default=ROOT.parent / 'index.html')
args = parser.parse_args()
STYLE_VERSION = hashlib.sha256((ROOT / "styles.css").read_bytes()).hexdigest()[:12]
SCRIPT_VERSION = hashlib.sha256((ROOT / "app.js").read_bytes()).hexdigest()[:12]
try:
    D = json.loads(args.content.read_text(encoding='utf-8'))
except json.JSONDecodeError as error:
    raise SystemExit(f'{args.content}:{error.lineno}:{error.colno}: {error.msg}')
E = html.escape
S = D['site']
P = D['profile']
I = D['intro']
L = D['labels']

def validate_content():
    for section in ('news', 'publications', 'professional_experience'):
        identifiers = set()
        for item in D[section]:
            identifier = item['id']
            if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', identifier):
                raise ValueError(f'{section}: invalid id {identifier!r}; use letters, numbers, hyphens or underscores.')
            if identifier in identifiers:
                raise ValueError(f'{section}: duplicate id {identifier!r}; give each item a unique id.')
            identifiers.add(identifier)
    for item in D['news']:
        if not re.fullmatch(r'\d{4}\.(0[1-9]|1[0-2])', item['date']):
            raise ValueError(f'news {item["id"]}: use a date such as 2026.09.')
    images = [P['avatar'], S['favicon'], S['share_image']]
    images += [p['image'] for p in D['publications']]
    images += [e['logo'] for e in D['professional_experience']]
    for path in images:
        if not (ROOT / path).is_file():
            raise ValueError(f'Image not found: homepage/{path}. Upload this image or correct the path in content.json.')

validate_content()

ICONS = {
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    'scholar': '<path d="m2 9 10-6 10 6-10 6L2 9Zm4 3v6c4 3 8 3 12 0v-6M22 9v8"/>',
    'menu': '<path d="M4 6h16M4 12h16M4 18h16"/>',
    'down': '<path d="m6 9 6 6 6-6"/>',
    'close': '<path d="m6 6 12 12M6 18 18 6"/>',
    'zoom': '<path d="M4 9V4h5m6 0h5v5M4 15v5h5m6 0h5v-5"/>',
    'external': '<path d="M14 4h6v6m0-6L10 14M9 4H4v16h16v-5"/>',
}

def icon(name):
    if name == 'github':
        return (ROOT/'assets/logos/github.svg').read_text().replace('<svg ', '<svg class="icon github-icon" aria-hidden="true" ')
    return f'<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'

def link(url, label, css=''):
    external = ' target="_blank" rel="noopener noreferrer"' if url.startswith('https://') else ''
    return f'<a href="{E(url,quote=True)}" class="{css}"{external}>{label}</a>'

def externalize(fragment):
    return re.sub(r'<a href="(https://[^"]+)"', r'<a target="_blank" rel="noopener noreferrer" href="\1"', fragment)

def paper(p):
    venue = p['venue']
    awards = p.get('recognitions', [])
    refs = [link(item['url'], E(item['label'])) for item in p.get('links', [])]
    image = E('homepage/' + p['image'], quote=True)
    dimensions = p.get('image_dimensions')
    size = f' width="{int(dimensions["width"])}" height="{int(dimensions["height"])}"' if dimensions else ''
    badge_venue = p.get('badge_venue', venue)
    award_text = f' <span class="recognition">{E(" · ".join(awards))}</span>' if awards else ''
    meta = f'<span class="venue">{E(venue)} {p["year"]}{award_text}</span>'
    refs_html = f'<div class="paper-links">{"<span aria-hidden=true>|</span>".join(refs)}</div>' if refs else ''
    return f'''<article class="paper paper-box" id="{p['id']}" aria-labelledby="{p['id']}-title">
      <div class="paper-box-image"><a class="paper-image" href="{image}" data-figure data-title="{E(p['title'],quote=True)}" aria-label="Enlarge figure: {E(p['title'],quote=True)}"><span class="paper-badge" aria-hidden="true">{E(badge_venue)} {p['year']}</span><img src="{image}" alt="Overview figure for {E(p['title'],quote=True)}"{size} loading="lazy" decoding="async"></a></div>
      <div class="paper-copy"><h3 class="paper-title" id="{p['id']}-title">{E(p['title'])}</h3><p class="authors">{p['authors_html']}</p><p class="paper-meta">{meta}</p>{refs_html}</div>
    </article>'''

def news(n):
    title = link(n['url'],E(n['title'])) if n.get('url') else E(n['title'])
    return f'<li id="{n["id"]}"><time datetime="{n["date"].replace(".","-")}">{n["date"]}</time><div><strong>{E(n["headline"])}</strong><p>{title}</p></div></li>'

def experience(item):
    date = f'<p class="activity-date"><time>{E(item["date_label"])}</time></p>' if item['date_label'] else ''
    program = f' <span class="program" lang="zh">（{E(item["program"])}）</span>' if item.get('program') else ''
    location = f' · {E(item["location"])}' if item.get('location') else ''
    description = f'<p class="mentors">{externalize(item["description_html"])}</p>' if item.get('description_html') else ''
    return f'''<article class="activity-row" id="experience-{item['id']}"><div class="activity-logo {item['id']}"><img src="homepage/{item['logo']}" alt="{E(item['organization'],quote=True)} logo" loading="lazy"></div><div class="activity-copy">{date}<h3>{E(item['role'])}{program}</h3><p>{link(item['url'],E(item['organization']))}{location}</p>{description}</div></article>'''

bio = '</p><p>'.join(externalize(paragraph) for paragraph in I['paragraphs_html'])
contacts = ''.join(link(c.get('url') or 'mailto:' + P['email'], icon(c['icon']) + E(c['label'])) for c in P['contacts'])
honors = ''.join(f'<div class="honor-group"><h4>{E(g["label"])}</h4><ul>{"".join(f"<li><time>{h['year']}</time><span>{E(h['description'])}</span></li>" for h in g["items"])}</ul></div>' for g in D['honors']['groups'])
scholar = next((c['url'] for c in P['contacts'] if c['icon'] == 'scholar'), None)
scholar_link = link(scholar, E(L['scholar']) + ' ' + icon('external'), 'scholar-link') if scholar else ''
visible_news = [n for n in D['news'] if int(n['date'][:4]) >= D['news_archive']['before_year']]
older_news = [n for n in D['news'] if int(n['date'][:4]) < D['news_archive']['before_year']]
archive_label = D['news_archive']['label'].replace('{count}', str(len(older_news)))
service = ''.join(f'<li>{E(item)}</li>' for item in D['academic_service'])

page=f'''<!doctype html>
<html lang="en" class="no-js"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(S['title'])}</title><meta name="description" content="{E(S['description'],quote=True)}"><meta name="robots" content="index, follow"><link rel="canonical" href="{E(S['url'],quote=True)}"><meta property="og:type" content="website"><meta property="og:title" content="{E(S['title'],quote=True)}"><meta property="og:description" content="{E(S['share_description'],quote=True)}"><meta property="og:url" content="{E(S['url'],quote=True)}"><meta property="og:image" content="{E(S['url'].rstrip('/') + '/homepage/' + S['share_image'],quote=True)}"><meta name="twitter:card" content="summary"><meta name="theme-color" content="#ffffff">
<link rel="icon" href="homepage/{E(S['favicon'],quote=True)}" type="image/png"><link rel="stylesheet" href="homepage/styles.css?v={STYLE_VERSION}"><script src="homepage/app.js?v={SCRIPT_VERSION}" defer></script></head>
<body id="top"><a class="skip-link" href="#main">Skip to content</a>
<header class="masthead"><div class="masthead-inner"><a href="#about-me" class="home-link">{E(L['home'])}</a><button class="menu-toggle" type="button" aria-label="Open navigation" aria-controls="primary-nav" aria-expanded="false">{icon('menu')}</button><nav id="primary-nav" aria-label="Main navigation"><a href="#about-me" aria-current="location">{E(L['about'])}</a><a href="#news">{E(L['news'])}</a><a href="#publications">{E(L['publications'])}</a><a href="#experience">{E(L['experience'])}</a><a href="#honors">{E(L['service_nav'])}</a></nav></div></header>
<div class="page-layout"><aside class="profile" aria-label="Profile and contact details"><img class="portrait" src="homepage/{E(P['avatar'],quote=True)}" alt="{E(P['avatar_alt'],quote=True)}" width="800" height="800" fetchpriority="high"><div class="profile-text"><h1 class="profile-name">{E(P['name'])}</h1><p class="affiliation">{E(P['affiliation'])}</p><p class="profile-role">{E(P['role'])}</p><div class="profile-links">{contacts}</div></div></aside>
<main id="main"><section id="about-me" class="intro" aria-label="{E(L['about'],quote=True)}"><div class="bio"><p>{bio}</p><p class="research-statement">{E(I['research_prefix'])} <strong>{E(I['research_statement'])}</strong></p><p>{E(I['contact_prefix'])} {link('mailto:' + P['email'], E(P['email']))}{E(I['contact_suffix'])}</p></div></section>
<section id="news" class="section"><h2 id="-news">{E(L['news'])}</h2><ul class="news-list current-news">{''.join(news(n) for n in visible_news)}</ul><details class="news-archive"><summary><span class="closed-label">{E(archive_label)}</span><span class="open-label">{E(L['news_hide'])}</span>{icon('down')}</summary><ul class="news-list">{''.join(news(n) for n in older_news)}</ul></details></section>
<section id="publications" class="section"><div class="section-heading"><h2 id="-publications">{E(L['publications'])}</h2>{scholar_link}</div><div class="paper-list">{''.join(paper(p) for p in D['publications'])}</div></section>
<section id="experience" class="section"><h2 id="-professional-activity">{E(L['experience'])}</h2><div class="activities">{''.join(experience(item) for item in D['professional_experience'])}</div></section>
<section id="honors" class="section"><h2 id="-honors-and-awards">{E(L['service'])}</h2><ul class="service-list">{service}</ul><div class="honors"><h3>{E(L['honors'])}</h3><p class="period">{E(D['honors']['period'])}</p>{honors}</div></section>
<footer><p>{E(D['footer']['text'])} <span lang="zh">{E(D['footer']['text_zh'])}</span></p><a href="#top">{E(L['back_to_top'])}</a></footer></main></div>
<dialog id="figure-dialog" aria-labelledby="figure-caption"><div class="dialog-heading"><span>Research figure</span><button type="button" id="close-figure" aria-label="Close research figure">{icon('close')}</button></div><div class="dialog-body"><img id="expanded-figure" alt=""><p id="figure-caption"></p><a id="original-figure" target="_blank" rel="noopener">Open image {icon('external')}</a></div></dialog></body></html>'''
args.output.write_text(page, encoding='utf-8')
print(f'Built V5.1: {len(D["publications"])} works; {len(visible_news)} current news visible, {len(older_news)} earlier news archived; {len(D["professional_experience"])} logo entries.')
