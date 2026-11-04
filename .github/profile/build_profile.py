from pathlib import Path
from html import escape
import json
import math
import textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parents[1]
ASSETS = OUT / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)
WIDTH, HEIGHT = 1200, 368
COLORS = {'bg': '#070d19', 'panel': '#0b1628', 'cyan': '#80e7ff', 'blue': '#4a83ff', 'violet': '#7b82ff', 'text': '#e2f4ff', 'muted': '#9db4d3', 'line': '#254968'}
PHRASES = ['Building AI Systems', 'Learning for ML Researcher', 'Open to Collaborate']
LINKEDIN = None
PROJECTS = [
    {'name': 'Lattice', 'repo': 'Lattice', 'category': 'DISTRIBUTED SYSTEMS', 'description': 'Deploy applications across connected computers with resource-aware scheduling and guarded recovery.', 'tags': ['Python', 'FastAPI', 'Next.js'], 'icon': 'nodes'},
    {'name': 'Manora', 'repo': 'manora', 'category': 'AI COMPANION', 'description': 'Student-focused mental-health support built around a persistent AI companion called Buddy.', 'tags': ['Python', 'Conversational AI'], 'icon': 'orbit'},
    {'name': 'Revenue SRE', 'repo': 'revenue-sre', 'category': 'PAYMENT RELIABILITY', 'description': 'Detect payment failure spikes, investigate evidence, and coordinate approved recovery actions.', 'tags': ['FastAPI', 'PostgreSQL', 'React'], 'icon': 'pulse'},
    {'name': 'CNN Filter Explorer', 'repo': 'Visualizing-CNN-Filters', 'category': 'ML RESEARCH JOURNEY', 'description': 'Explore VGG16 filters and feature maps to understand how convolutional networks see an image.', 'tags': ['VGG16', 'Deep Learning', 'Notebooks'], 'icon': 'grid'},
]
# Edit profile-content.json, then run this script with Pillow and NumPy installed.
config_file = ROOT / 'profile-content.json'
if config_file.exists():
    config = json.loads(config_file.read_text(encoding='utf-8'))
    PHRASES = config['phrases']
    LINKEDIN = config.get('linkedin')
    PROJECTS = config['projects']

FONTDIR = Path(r'C:\Windows\Fonts')
NAME_FONT = ImageFont.truetype(str(FONTDIR / 'seguisb.ttf'), 82)
TYPE_FONT = ImageFont.truetype(str(FONTDIR / 'consola.ttf'), 31)
MICRO_FONT = ImageFont.truetype(str(FONTDIR / 'consola.ttf'), 14)

def center(draw, text, y, font, fill):
    length = draw.textlength(text, font=font)
    draw.text(((WIDTH - length) / 2, y), text, font=font, fill=fill)

def spaced(draw, text, center_x, y, spacing=3, color='#7fb9df'):
    widths = [draw.textlength(c, font=MICRO_FONT) for c in text]
    x = center_x - (sum(widths) + spacing * (len(text) - 1)) / 2
    for char, size in zip(text, widths):
        draw.text((x, y), char, font=MICRO_FONT, fill=color)
        x += size + spacing

def build_header():
    yy, xx = np.mgrid[0:HEIGHT, 0:WIDTH]
    strength = np.exp(-(((xx - WIDTH / 2) / 390) ** 2 + ((yy - 136) / 170) ** 2))
    rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    for c, base in enumerate([7, 13, 25]):
        rgb[:, :, c] = base + strength * [2, 12, 30][c]
    im = Image.fromarray(rgb)
    d = ImageDraw.Draw(im)
    d.line([(24, 70), (24, 24), (90, 24)], fill='#4c9ed4', width=2)
    d.line([(1110, 24), (1176, 24), (1176, 70)], fill='#4c9ed4', width=2)
    d.line([(24, 298), (24, 344), (90, 344)], fill='#254968', width=2)
    d.line([(1110, 344), (1176, 344), (1176, 298)], fill='#254968', width=2)
    d.line([(91, 24), (260, 24)], fill='#19364e')
    d.line([(940, 24), (1109, 24)], fill='#19364e')
    for x, y, flip in [(48, 92, 1), (1138, 92, -1), (48, 263, 1), (1138, 263, -1)]:
        for j in range(3):
            d.line([(x + j * 9 * flip, y), (x + (j * 9 + 5) * flip, y + 7)], fill='#315778', width=1)
    spaced(d, 'D E V E L O P E R   P R O F I L E', WIDTH / 2, 54, spacing=0)
    d.text((46, 319), 'SJ / 001', font=MICRO_FONT, fill='#6383a7')
    d.text((1011, 319), 'BUILD + LEARN', font=MICRO_FONT, fill='#6383a7')
    # The identity remains legible on the very first frame.
    mask = Image.new('L', (WIDTH, HEIGHT))
    md = ImageDraw.Draw(mask)
    center(md, 'Siddharth Jha', 97, NAME_FONT, 255)
    grad = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    for y in range(HEIGHT):
        t = np.clip((y - 105) / 96, 0, 1)
        grad[y, :, :] = np.array([210, 247, 255]) * (1 - t) + np.array([66, 126, 255]) * t
    glow = Image.new('RGB', im.size, '#376acf')
    im.paste(glow, (0, 0), mask.filter(ImageFilter.GaussianBlur(16)).point(lambda x: int(x * .38)))
    im.paste(Image.fromarray(grad), (0, 0), mask)
    return im

def typed_state(t):
    cycle = 5.2
    index = int(t / cycle) % len(PHRASES)
    local = t % cycle
    phrase = PHRASES[index]
    type_duration = len(phrase) / 12
    if local < .25:
        length = 0
    elif local < .25 + type_duration:
        length = int((local - .25) * 12)
    elif local < 4.20:
        length = len(phrase)
    elif local < 5.05:
        length = max(0, int(len(phrase) * (5.05 - local) / .85))
    else:
        length = 0
    return phrase[:length], index

def header_frame(t):
    im = HEADER.copy()
    d = ImageDraw.Draw(im)
    text, current = typed_state(t)
    width = d.textlength(text, font=TYPE_FONT)
    x = (WIDTH - width) / 2
    d.text((x, 225), text, font=TYPE_FONT, fill='#83d9ff')
    if int(t * 2.5) % 2 == 0 or len(text) < len(PHRASES[current]):
        d.rectangle((x + width + 5, 232, x + width + 8, 258), fill='#72caff')
    # A small three-step indicator follows the active line without extra words.
    for i in range(3):
        px = WIDTH / 2 - 37 + i * 27
        color = '#71cbff' if i == current else '#1f3a55'
        d.line([(px, 295), (px + 18, 295)], fill=color, width=2)
    return im

HEADER = build_header()
fps = 12.5
duration = 15.6
frame_count = round(fps * duration)
frames_rgb = [header_frame(i / fps) for i in range(frame_count)]
# One shared palette avoids color changes around the stationary lettering.
palette = header_frame(2.8).quantize(colors=128)
frames = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in frames_rgb]
header_path = ASSETS / 'system-header-v1.gif'
frames[0].save(header_path, save_all=True, append_images=frames[1:], duration=80, loop=0, optimize=True, disposal=1)
# The README uses the animated GIF directly.

def defs():
    return '''<defs>
      <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#72dbff"/><stop offset=".45" stop-color="#327ed1"/><stop offset="1" stop-color="#636fff"/></linearGradient>
      <linearGradient id="title" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#e2f7ff"/><stop offset="1" stop-color="#85bdff"/></linearGradient>
      <radialGradient id="aura" cx="90%" cy="0%" r="100%"><stop stop-color="#163259" stop-opacity=".7"/><stop offset="1" stop-color="#0b1526" stop-opacity="0"/></radialGradient>
    </defs>'''

def icon_markup(kind):
    attrs='fill="none" stroke="#76d5ff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"'
    if kind == 'nodes':
        body='<path d="M10 10 34 4 43 27 19 39 10 10ZM10 10 27 22 34 4M27 22 43 27M27 22 19 39"/><circle cx="10" cy="10" r="3" fill="#0b1628"/><circle cx="34" cy="4" r="3" fill="#0b1628"/><circle cx="43" cy="27" r="3" fill="#0b1628"/><circle cx="19" cy="39" r="3" fill="#0b1628"/>'
    elif kind == 'orbit':
        body='<circle cx="24" cy="21" r="15"/><ellipse cx="24" cy="21" rx="24" ry="7" transform="rotate(-35 24 21)"/><circle cx="24" cy="21" r="4" fill="#76d5ff"/><circle cx="44" cy="8" r="2" fill="#76d5ff"/>'
    elif kind == 'pulse':
        body='<path d="M1 23H11L16 9 24 35 31 16 36 23H47"/><path d="M7 3H17M37 3H45M7 43H17M37 43H45" stroke-opacity=".4"/>'
    else:
        body=''.join(f'<rect x="{x*15+4}" y="{y*15+1}" width="9" height="9" opacity="{.3+(x+y)/6}"/>' for y in range(3) for x in range(3))
    return f'<g {attrs}>{body}</g>'

def card(project, number):
    name = escape(project['name'])
    description = textwrap.wrap(project['description'], width=55)
    body = ''.join(f'<text x="32" y="{146+i*25}" fill="#a9bdd9" font-family="Segoe UI,Arial,sans-serif" font-size="17">{escape(line)}</text>' for i, line in enumerate(description))
    tags = ''
    tx = 32
    for tag in project['tags']:
        width = len(tag) * 7 + 21
        tags += f'<path d="M{tx+4} 228h{width-4}v24h-{width}v-20Z" fill="#10243d" stroke="#244865"/><text x="{tx+10}" y="244" fill="#9ed0ee" font-family="Consolas,monospace" font-size="12">{escape(tag)}</text>'
        tx += width + 9
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="298" viewBox="0 0 600 298" role="img" aria-label="{name}: {escape(project['description'])}">
    {defs()}
    <path d="M18 2H580L598 20V280L582 296H2V18Z" fill="#0b1526" stroke="#223d5b" stroke-width="1.3"/>
    <path d="M18 2H580L598 20V280L582 296H2V18Z" fill="url(#aura)"/>
    <path d="M2 48V18L18 2H120M480 2H580L598 20V48M598 250V280L582 296H480M120 296H2V250" fill="none" stroke="url(#edge)" stroke-width="2"/>
    <text x="32" y="35" fill="#75bce9" font-family="Consolas,monospace" font-size="11" letter-spacing="2">PROJECT // {number:02d}</text>
    <path d="M32 48H470" stroke="#1c3550"/><path d="M32 48H85" stroke="#59baff" stroke-width="2"/>
    <text x="32" y="94" fill="url(#title)" font-family="Segoe UI,Arial,sans-serif" font-size="31" font-weight="700">{name}</text>
    <text x="32" y="119" fill="#62b8ed" font-family="Consolas,monospace" font-size="10.5" letter-spacing="1.7">{project['category']}</text>
    <g transform="translate(512 67)">{icon_markup(project['icon'])}</g>
    {body}{tags}
    <text x="32" y="279" fill="#6081a5" font-family="Consolas,monospace" font-size="10" letter-spacing="1.4">SIDDHARTHJHA123 / OPEN SOURCE</text>
    <g stroke="#8bd9ff" fill="none" stroke-width="1.5"><path d="M553 270h15v-15M568 255 552 271"/></g>
    </svg>'''

for i, project in enumerate(PROJECTS, 1):
    (ASSETS / f'project-{i:02d}.svg').write_text(card(project, i), encoding='utf-8')

def social(label, icon):
    text = '&lt;/&gt;' if icon == 'code' else 'in'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="178" height="48" viewBox="0 0 178 48" role="img" aria-label="{label}">{defs()}
    <path d="M10 1H177V37L167 47H1V11Z" fill="#0c192c" stroke="#386a9c"/>
    <path d="M1 16V11L10 1H27M151 47H167L177 37V30" fill="none" stroke="url(#edge)" stroke-width="1.6"/>
    <text x="29" y="30" fill="#83d6ff" font-family="Consolas,monospace" font-size="18" font-weight="700" text-anchor="middle">{text}</text>
    <path d="M52 13v22" stroke="#2a4664"/><text x="67" y="30" font-family="Segoe UI,Arial,sans-serif" font-size="16" font-weight="600" fill="#d2ecff">{label}</text>
    </svg>'''

(ASSETS/'social-github.svg').write_text(social('GitHub','code'),encoding='utf-8')
(ASSETS/'social-linkedin.svg').write_text(social('LinkedIn','in'),encoding='utf-8')
(ASSETS/'projects-heading.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="75" viewBox="0 0 1200 75"><path d="M0 38H357M843 38H1200" stroke="#244362"/><path d="M327 38H357M843 38H873" stroke="#5fc3ff" stroke-width="2"/><text x="600" y="43" text-anchor="middle" font-family="Consolas,monospace" font-size="20" letter-spacing="4" fill="#9bdcff">SELECTED PROJECTS</text></svg>''',encoding='utf-8')

readme = '''<p align="center">
  <img src="assets/ascii-portrait-wind-v2.gif" alt="Siddharth Jha with his laptop" width="100%" />
</p>

<p align="center">
  <img src="assets/system-header-v1.gif" alt="Siddharth Jha — Building AI Systems; Learning for ML Researcher; Open to Collaborate" width="100%" />
</p>

<p align="center">
  <a href="https://github.com/siddharthjha123"><img src="assets/social-github.svg" alt="GitHub" width="145" /></a>
  LINKEDIN_BUTTON
</p>

<p align="center">
  <img src="assets/projects-heading.svg" alt="Selected projects" width="100%" />
</p>

'''
linkedin_button = '<img src="assets/social-linkedin.svg" alt="LinkedIn — profile link pending" width="145" />'
if LINKEDIN:
    linkedin_button=f'<a href="{LINKEDIN}"><img src="assets/social-linkedin.svg" alt="LinkedIn" width="145" /></a>'
readme=readme.replace('LINKEDIN_BUTTON',linkedin_button)
for i in [0,2]:
    readme+='<p align="center">\n'
    for j in [i,i+1]:
        project=PROJECTS[j]
        readme+=f'  <a href="https://github.com/siddharthjha123/{project["repo"]}"><img src="assets/project-{j+1:02d}.svg" alt="{project["name"]} — {project["category"].title()}" width="390" /></a>\n'
    readme+='</p>\n\n'
(OUT/'README.md').write_text(readme.rstrip()+'\n',encoding='utf-8')
(ROOT/'profile-content.json').write_text(json.dumps({'name':'Siddharth Jha','phrases':PHRASES,'linkedin':LINKEDIN,'projects':PROJECTS},indent=2),encoding='utf-8')
print(json.dumps({'header_frames':len(frames),'header_bytes':header_path.stat().st_size,'seconds':duration,'assets':len(list(ASSETS.iterdir()))}))
