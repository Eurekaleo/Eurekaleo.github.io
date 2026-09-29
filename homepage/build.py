#!/usr/bin/env python3
"""Build the production homepage from the approved V5.1 source. Standard library only."""
from pathlib import Path
import html
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
STYLE_VERSION = hashlib.sha256((ROOT / "styles.css").read_bytes()).hexdigest()[:12]
SCRIPT_VERSION = hashlib.sha256((ROOT / "app.js").read_bytes()).hexdigest()[:12]
D = json.loads((ROOT / 'content.json').read_text())
E = html.escape

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
    venue = p['venue'].replace('Arxiv','arXiv').replace('arxiv','arXiv')
    awards = []
    if 'Oral' in venue: awards.append('Oral')
    if 'Spotlight' in venue: awards.append('Spotlight')
    if '2nd Place' in venue: awards.append('2nd Place')
    if p['badge'] == 'HF Daily Paper #2': awards.append('HF Daily Paper #2')
    if p['id'] == 'paper-16': awards.append('Best Paper Award')
    venue = re.sub(r'\s*\((?:Oral|Oral, Spotlight|Challenge, 2nd Place)\)', '', venue).replace(' 2024','')
    venue = {'Workshop@MM':'ACM MM Workshop','SemEval@ACL':'SemEval @ ACL'}.get(venue,venue)
    refs = []
    if p['paper_url']: refs.append(link(p['paper_url'],'Paper'))
    seen = {p['paper_url']}
    for item in p['links']:
        if item['url'] in seen or item['url'].rstrip('/') == 'https://eurekaleo.github.io': continue
        seen.add(item['url'])
        label = 'GitHub' if 'github.com/' in item['url'] else 'Dataset' if 'huggingface.co/datasets/' in item['url'] else 'Project Page' if item['label'] == 'Project' else item['label']
        refs.append(link(item['url'],E(label)))
    image = f'homepage/assets/images/{Path(p["image"]).stem}.webp'
    badge_venue = {'EMNLP (Findings)':'EMNLP', 'ACM MM Workshop':'ACM MMW', 'SemEval @ ACL':'SemEval'}.get(venue, venue)
    award_text = f' <span class="recognition">{E(" · ".join(awards))}</span>' if awards else ''
    meta = f'<span class="venue">{E(venue)} {p["year"]}{award_text}</span>'
    refs_html = f'<div class="paper-links">{"<span aria-hidden=true>|</span>".join(refs)}</div>' if refs else ''
    return f'''<article class="paper paper-box" id="{p['id']}" aria-labelledby="{p['id']}-title">
      <div class="paper-box-image"><a class="paper-image" href="{image}" data-figure data-title="{E(p['title'],quote=True)}" aria-label="Enlarge figure: {E(p['title'],quote=True)}"><span class="paper-badge" aria-hidden="true">{E(badge_venue)} {p['year']}</span><img src="{image}" alt="Overview figure for {E(p['title'],quote=True)}" width="{p['image_dimensions']['width']}" height="{p['image_dimensions']['height']}" loading="lazy" decoding="async"></a></div>
      <div class="paper-copy"><h3 class="paper-title" id="{p['id']}-title">{E(p['title'])}</h3><p class="authors">{p['authors_html']}</p><p class="paper-meta">{meta}</p>{refs_html}</div>
    </article>'''

def news(n):
    title = link(n['url'],E(n['title'])) if n['url'] else E(n['title'])
    return f'<li id="{n["id"]}"><time datetime="{n["date"].replace(".","-")}">{n["date"]}</time><div><strong>{E(n["headline"])}</strong><p>{title}</p></div></li>'

def experience(item):
    date = f'<p class="activity-date"><time>{E(item["date_label"])}</time></p>' if item['date_label'] else ''
    program = f' <span class="program" lang="zh">（{E(item["program"])}）</span>' if item.get('program') else ''
    location = f' · {E(item["location"])}' if item.get('location') else ''
    description = f'<p class="mentors">{externalize(item["description_html"])}</p>' if item.get('description_html') else ''
    return f'''<article class="activity-row" id="experience-{item['id']}"><div class="activity-logo {item['id']}"><img src="homepage/{item['logo']}" alt="{E(item['organization'],quote=True)} logo" loading="lazy"></div><div class="activity-copy">{date}<h3>{E(item['role'])}{program}</h3><p>{link(item['url'],E(item['organization']))}{location}</p>{description}</div></article>'''

bio = externalize(D['bio'][0]['html']).replace('\nPrior to this,','</p><p>Prior to this,')
# Keep the original introduction and research statement, only repair its English opening.
bio = bio.replace('I am now a computer science PhD student at School of Computing in','I am a computer science PhD student at the School of Computing,')
contacts = ''.join(link(c['url'],icon({'Email':'mail','Github':'github','Google Scholar':'scholar'}[c['label']])+('GitHub' if c['label']=='Github' else c['label'])) for c in D['profile']['contacts'])
honors = ''.join(f'<div class="honor-group"><h4>{E(g["label"])}</h4><ul>{"".join(f"<li><time>{h['year']}</time><span>{E(h['description'])}</span></li>" for h in g["items"])}</ul></div>' for g in D['honors']['groups'])
scholar = next(c['url'] for c in D['profile']['contacts'] if c['label']=='Google Scholar')
visible_news = [n for n in D['news'] if int(n['date'][:4]) >= 2026]
older_news = [n for n in D['news'] if int(n['date'][:4]) < 2026]

page=f'''<!doctype html>
<html lang="en" class="no-js"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Meng Luo — Homepage</title><meta name="description" content="Meng Luo, PhD student at the National University of Singapore. Multimodal video understanding, reasoning, and generation."><meta name="robots" content="index, follow"><link rel="canonical" href="https://eurekaleo.github.io/"><meta property="og:type" content="website"><meta property="og:title" content="Meng Luo — Homepage"><meta property="og:description" content="CS PhD student at NUS. Multimodal video understanding, reasoning, and generation."><meta property="og:url" content="https://eurekaleo.github.io/"><meta property="og:image" content="https://eurekaleo.github.io/homepage/assets/images/luomeng.webp"><meta name="twitter:card" content="summary"><meta name="theme-color" content="#ffffff">
<link rel="icon" href="homepage/assets/favicon.png" type="image/png"><link rel="stylesheet" href="homepage/styles.css?v={STYLE_VERSION}"><script src="homepage/app.js?v={SCRIPT_VERSION}" defer></script></head>
<body id="top"><a class="skip-link" href="#main">Skip to content</a>
<header class="masthead"><div class="masthead-inner"><a href="#about-me" class="home-link">Homepage</a><button class="menu-toggle" type="button" aria-label="Open navigation" aria-controls="primary-nav" aria-expanded="false">{icon('menu')}</button><nav id="primary-nav" aria-label="Main navigation"><a href="#about-me" aria-current="location">About Me</a><a href="#news">News</a><a href="#publications">Selected Works</a><a href="#experience">Professional Activity</a><a href="#honors">Service and Honors</a></nav></div></header>
<div class="page-layout"><aside class="profile" aria-label="Profile and contact details"><img class="portrait" src="homepage/assets/images/luomeng.webp" alt="Meng Luo by the ocean" width="800" height="800" fetchpriority="high"><div class="profile-text"><h1 class="profile-name">Meng Luo</h1><p class="affiliation">National University of Singapore</p><p class="profile-role">CS PhD student</p><div class="profile-links">{contacts}</div></div></aside>
<main id="main"><section id="about-me" class="intro" aria-label="About Me"><div class="bio"><p>{bio}</p><p class="research-statement">My research interest includes <strong>Bridging Physical and Mental Worlds toward Human-Like Intelligence through Multimodal (Video) Understanding, Reasoning, and Generation.</strong></p><p>I am always exploring new collaboration opportunities. If you are interested in these topics, please feel free to email me at {link('mailto:mluo@u.nus.edu','mluo@u.nus.edu')}.</p></div></section>
<section id="news" class="section"><h2 id="-news">News</h2><ul class="news-list current-news">{''.join(news(n) for n in visible_news)}</ul><details class="news-archive"><summary><span class="closed-label">2025 and earlier ({len(older_news)} updates)</span><span class="open-label">Hide earlier updates</span>{icon('down')}</summary><ul class="news-list">{''.join(news(n) for n in older_news)}</ul></details></section>
<section id="publications" class="section"><div class="section-heading"><h2 id="-publications">Selected Works</h2>{link(scholar,'Google Scholar '+icon('external'),'scholar-link')}</div><div class="paper-list">{''.join(paper(p) for p in D['publications'])}</div></section>
<section id="experience" class="section"><h2 id="-professional-activity">Professional Activity</h2><div class="activities">{''.join(experience(item) for item in D['professional_experience'])}</div></section>
<section id="honors" class="section"><h2 id="-honors-and-awards">Academic Service and Honors</h2><ul class="service-list"><li>{E(D['professional_activities'][2]['text'])}</li></ul><div class="honors"><h3>Honors and Awards</h3><p class="period">During my undergraduate studies</p>{honors}</div></section>
<footer><p>Wisdom begins in wonder. <span lang="zh">网罗天下，广结同盟。</span></p><a href="#top">Back to top ↑</a></footer></main></div>
<dialog id="figure-dialog" aria-labelledby="figure-caption"><div class="dialog-heading"><span>Research figure</span><button type="button" id="close-figure" aria-label="Close research figure">{icon('close')}</button></div><div class="dialog-body"><img id="expanded-figure" alt=""><p id="figure-caption"></p><a id="original-figure" target="_blank" rel="noopener">Open image {icon('external')}</a></div></dialog></body></html>'''
(ROOT.parent/'index.html').write_text(page)
print(f'Built V5.1: {len(D["publications"])} works; {len(visible_news)} current news visible, {len(older_news)} earlier news archived; {len(D["professional_experience"])} logo entries.')
