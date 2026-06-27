#!/usr/bin/env python3
"""
Fetch Xiao Wei Sun's publications from OpenAlex API and generate publications-data.js.

Author ID: A5033342186 (OpenAlex)
ORCID: https://orcid.org/0000-0002-2840-1880

Usage: python3 fetch_publications.py [--output publications-data.js] [--pages 20]
"""

import json
import sys
import os
import time
import urllib.request
import urllib.error
from datetime import datetime

# Configuration
AUTHOR_ID = "A5033342186"
BASE_URL = "https://api.openalex.org/works"
PER_PAGE = 50

# ── Strict exclusion: papers clearly NOT from this Sun Xiaowei ──
# These topics have zero overlap with his research (quantum dots, displays, LEDs, ZnO, semiconductors, AR)
EXCLUDE_TITLE_KEYWORDS = [
    # Medical / biology unrelated
    'nasal', 'staphylococcus', 'depressive', 'tumor', 'cancer', 'colorectal',
    'breast cancer', 'circulating tumor', 'antimicrobial', 'gonococcal',
    'pathogen', 'antibiotic', 'bacterial', 'virus', 'vaccine',
    # Agriculture / environment unrelated
    'microalgae', 'biomass', 'tobacco', 'pesticide', 'antifouling',
    'desalination', 'geopolymer', 'soil', 'crop', 'livestock',
    'ethane conversion', 'pyrolysis', 'coking', 'waste plastic',
    # Mechanical / civil engineering unrelated
    'bearing fault', 'voiceprint', 'substation', 'sport utility vehicle',
    'electric sport utility', 'tool wear', 'micro-milling',
    'cutting', 'machining', 'tribology', 'friction',
    # Cybersecurity / IT unrelated
    'network security', 'corporate governance', 'cyber', 'fuzzy naive bayes',
    'gaze-behavior', 'intention inference', 'blockchain',
    # Other clearly unrelated
    'body weight', 'bioelectrical', 'infrared imaging',
    'lithium metal batter', 'lithium-ion batter',
    'photovoltaic', 'solar cell', 'dye-sensitized',
    'hydrogen production', 'water splitting', 'photocatal',
    'corrosion inhibitor', 'anti-corrosion',
    'carbon quantum dot',  # different field
    'gold nanoparticle', 'plasmon',  # different subfield
    'proton conductor', 'solid oxide',
    'food', 'nutrition', 'pharmaceutical',
]

# ── Strong inclusion: papers clearly from this Sun Xiaowei ──
# Even if author disambiguation is imperfect, these topics are his signature work
INCLUDE_TITLE_KEYWORDS = [
    'quantum dot', 'qled', 'quantum-dot', 'quantum well',
    'light-emitting diode', 'light emitting diode', 'led device',
    'oled', 'micro-led', 'microled', 'miniled',
    'display', 'electroluminesc',
    'zno', 'zinc oxide', 'nanorod',
    'perovskite light', 'perovskite emit', 'perovskite nanocrystal',
    'waveguide', 'metasurface', 'achromatic',
    'electrophoretic deposition', 'electrodeposit',
    '3d display', 'autostereoscopic', 'glasses-free',
    'ar display', 'augmented reality display',
    'inkjet print', 'inkjet-print',
    'photoluminesc', 'cathodoluminesc',
    'epitaxial', 'pulsed laser deposition',
    'nanocrystal', 'colloidal',
    'wide bandgap', 'wide-bandgap',
    'whispering gallery',
    'injection', 'carrier transfer',
    'exciton', 'fluorescence',
    'inp quantum', 'cdse', 'cdzns', 'cdznete', 'ags quantum',
    'luminescent solar',  # his solar concentrator work uses QDs
]

# ── Venue-based inclusion ──
# Papers in these journals with his name are very likely his
HIGH_CONFIDENCE_VENUES = [
    'nature', 'science', 'nature communications', 'nature nanotechnology',
    'nature photonics', 'nature electronics', 'nature reviews',
    'advanced materials', 'advanced functional materials', 'advanced optical materials',
    'light: science', 'light sci', 'nano letters', 'acs nano',
    'ieee electron device', 'ieee transactions on electron',
    'applied physics letters', 'journal of applied physics',
    'nanoscale', 'journal of physical chemistry',
    'journal of the society for information display',
    'advanced electronic materials', 'acs applied',
    'the innovation', 'laser & photonics',
]



# ── Additional exclusions for disambiguation ──
EXTRA_EXCLUDE_KEYWORDS = [
    'microalg', 'visual relocalization', 'semantics supervision',
    'gaussian splatting', 'phononic crystal', 'elastic waveguide',
    'stagnation flame', 'ga2o3 thin film',
    'ray tracing',
    'piezoelectric nanogenerator', 'nanogenerator',
    'transparent wood',
    'sers', 'surface-enhanced raman',
    'silver nanowire', 'ag nw',
    'electrochrom', 'viologen', 'photochromic',
    'cholesteric', 'liquid crystal', 'blue phase',
    'azobenzene', 'photoinduced ordering',
    'black phosphor', 'phosphorene',
    'graphene nanostruct', 'contact lens',
    'water electrolysis', 'oxygen evolution', 'electrocatal',
    'lithium', 'battery', 'anode', 'cathode',
    'tandem solar', 'solar cell',
    'schottky barrier', 'rram', 'resistive switch',
    'triboelectric',
    'optical biosensor', 'cholic acid',
    'dichroic dye', 'optical haze',
    'type-switchable inverter', 'ambipolar',
    'phonon mode', 'ferroelectric',
]

def fetch_json(url, retries=3):
    """Fetch JSON from URL with retries."""
    headers = {
        'User-Agent': 'SunLab-Publications/1.0 (academic research)',
        'Accept': 'application/json',
    }
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def is_relevant(paper):
    """Determine if a paper belongs to Sun Xiaowei (SUSTech)."""
    title = (paper.get('title') or '').lower()
    
    # Step 0: Extra disambiguation exclusions
    for kw in EXTRA_EXCLUDE_KEYWORDS:
        if kw.lower() in title:
            return False
    
    # Step 1: Hard exclude - clearly unrelated topics
    for kw in EXCLUDE_TITLE_KEYWORDS:
        if kw.lower() in title:
            return False
    
    # Step 2: Strong include - signature research topics
    for kw in INCLUDE_TITLE_KEYWORDS:
        if kw.lower() in title:
            return True
    
    # Step 3: Check venue + SUSTech affiliation
    loc = paper.get('primary_location') or {}
    source = loc.get('source') or {}
    journal = (source.get('display_name') or '').lower()
    
    # Check if journal is high-confidence
    is_top_venue = any(v in journal for v in HIGH_CONFIDENCE_VENUES)
    
    # Check SUSTech affiliation for this specific author
    has_sustech = False
    for authorship in paper.get('authorships', []):
        author_id = authorship.get('author', {}).get('id') or ''
        if AUTHOR_ID in author_id:
            for inst in authorship.get('institutions', []):
                inst_name = (inst.get('display_name') or '').lower()
                if 'southern university of science and technology' in inst_name or 'sustech' in inst_name:
                    has_sustech = True
                    break
    
    # If it's a top venue AND has SUSTech affiliation, include
    if is_top_venue and has_sustech:
        return True
    
    # If has SUSTech affiliation, include (reasonable confidence)
    if has_sustech:
        return True
    
    # Otherwise, exclude (likely a different person with similar name)
    return False


def format_authors(authorships):
    """Format author list with Sun highlighted."""
    authors = []
    sun_index = -1
    
    for i, a in enumerate(authorships):
        name = a.get('author', {}).get('display_name', '')
        aid = a.get('author', {}).get('id') or ''
        if not name:
            continue
        authors.append(name)
        if AUTHOR_ID in aid:
            sun_index = len(authors) - 1
    
    if not authors:
        return ''
    
    # Highlight Sun's name
    def hl(name, idx):
        if idx == sun_index:
            return f"<span class='hl'>{name}</span>"
        return name
    
    if len(authors) <= 4:
        return ', '.join(hl(n, i) for i, n in enumerate(authors))
    else:
        # Show first 3 + ... + Sun (if not in first 3)
        first3 = ', '.join(hl(n, i) for i, n in enumerate(authors[:3]))
        if sun_index >= 0 and sun_index >= 3:
            return first3 + ', ..., ' + hl(authors[sun_index], sun_index)
        elif sun_index >= 0 and sun_index < 3:
            return first3 + ', ...'
        else:
            return first3 + ', ...'


def determine_tags(paper, year, cited):
    """Determine display tags for a paper."""
    tags = []
    current_year = datetime.now().year
    
    if year >= current_year - 1:
        tags.append('recent')
    if cited >= 300:
        tags.append('highly-cited')
    
    loc = paper.get('primary_location') or {}
    source = loc.get('source') or {}
    journal = (source.get('display_name') or '').lower()
    top_journals = [
        'nature', 'science', 'cell', 'nature communications',
        'nature nanotechnology', 'nature photonics', 'nature electronics',
        'nature reviews', 'nature materials', 'nature energy',
        'advanced materials', 'advanced functional materials',
        'light: science', 'nano letters', 'acs nano',
        'physical review letters', 'ieee trans',
        'advanced optical materials', 'journal of the american chemical',
        'angewandte', 'energy & environmental',
    ]
    if any(tj in journal for tj in top_journals):
        tags.append('top-journal')
    
    return tags


def fetch_all_papers(max_pages=20):
    """Fetch all papers for the author from OpenAlex using cursor pagination."""
    all_papers = []
    cursor = '*'
    
    for page in range(max_pages):
        url = (
            f"{BASE_URL}?filter=author.id:{AUTHOR_ID}"
            f"&sort=publication_date:desc"
            f"&per_page={PER_PAGE}"
            f"&cursor={cursor}"
            f"&select=id,title,authorships,publication_date,primary_location,doi,cited_by_count"
        )
        
        print(f"  Fetching page {page + 1}...", file=sys.stderr)
        data = fetch_json(url)
        
        items = data.get('results', [])
        if not items:
            break
        
        all_papers.extend(items)
        
        cursor = data.get('meta', {}).get('next_cursor')
        if not cursor:
            break
        
        time.sleep(0.5)  # Be nice to the API
    
    return all_papers


def generate_js(papers, output_path):
    """Generate publications-data.js file."""
    entries = []
    seen_titles = set()
    current_year = datetime.now().year
    recent_threshold = current_year - 2  # Last 3 years (inclusive)
    min_citations_old = 300  # Minimum citations for papers before recent period
    
    for paper in papers:
        title = paper.get('title', '')
        if not title:
            continue
        
        # Deduplicate by normalized title
        norm_title = title.lower().strip()
        if norm_title in seen_titles:
            continue
        seen_titles.add(norm_title)
        
        pub_date = paper.get('publication_date', '')
        year = int(pub_date[:4]) if pub_date and pub_date[:4].isdigit() else 0
        
        # Filter: recent papers (last 3 years) kept in full; older papers need >= 100 citations
        if year < recent_threshold:
            cited = paper.get('cited_by_count', 0) or 0
            if cited < min_citations_old:
                continue
        
        doi = paper.get('doi', '') or ''
        cited = paper.get('cited_by_count', 0) or 0
        
        authors = format_authors(paper.get('authorships', []))
        
        loc = paper.get('primary_location') or {}
        source = loc.get('source') or {}
        journal = source.get('display_name', '') or ''
        
        tags = determine_tags(paper, year, cited)
        
        entry = {
            'title': title,
            'authors': authors,
            'journal': journal,
            'year': year,
            'doi': doi,
            'citations': cited,
            'tags': tags,
        }
        entries.append(entry)
    
    # Sort by year desc, then citations desc
    entries.sort(key=lambda x: (-x['year'], -x['citations']))
    
    # Generate JS
    js_lines = ['var PUBLICATIONS_DATA=[']
    for entry in entries:
        tags_str = '[' + ','.join(f'"{t}"' for t in entry['tags']) + ']'
        # Escape title for JS string
        safe_title = entry['title'].replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
        safe_journal = entry['journal'].replace('\\', '\\\\').replace('"', '\\"')
        line = (
            f'{{title:"{safe_title}",'
            f'authors:"{entry["authors"]}",'
            f'journal:"{safe_journal}",'
            f'year:{entry["year"]},'
            f'doi:"{entry["doi"]}",'
            f'citations:{entry["citations"]},'
            f'tags:{tags_str}}},'
        )
        js_lines.append(line)
    js_lines.append('];')
    
    content = '\n'.join(js_lines)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return len(entries)


def main():
    output_path = 'publications-data.js'
    max_pages = 20
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--output' and i + 1 < len(args):
            output_path = args[i + 1]
            i += 2
        elif args[i] == '--pages' and i + 1 < len(args):
            max_pages = int(args[i + 1])
            i += 2
        else:
            i += 1
    
    print(f"Fetching papers for Xiao Wei Sun (OpenAlex ID: {AUTHOR_ID})...", file=sys.stderr)
    
    all_papers = fetch_all_papers(max_pages)
    print(f"Total papers fetched from API: {len(all_papers)}", file=sys.stderr)
    
    relevant = [p for p in all_papers if is_relevant(p)]
    print(f"After filtering for relevance: {len(relevant)}", file=sys.stderr)
    
    count = generate_js(relevant, output_path)
    print(f"Generated {output_path} with {count} unique papers.", file=sys.stderr)
    
    # Summary by year
    years = {}
    for p in relevant:
        y = (p.get('publication_date') or '')[:4]
        if y and y.isdigit():
            years[y] = years.get(y, 0) + 1
    print(f"\nPapers by year:", file=sys.stderr)
    for y in sorted(years.keys(), reverse=True):
        print(f"  {y}: {years[y]}", file=sys.stderr)
    
    print(f"\nDone. Output: {output_path}", file=sys.stderr)


if __name__ == '__main__':
    main()
