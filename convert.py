#!/usr/bin/env python3
"""Convert Falnorian Rulebook to HTML using structural cues."""
import re, html as H

def read(path):
    with open(path) as f: return f.read()

def fix_ligatures(t):
    subs = [
        ('e ciency','efficiency'),('e cient','efficient'),
        ('o cial','official'),('o cially','officially'),('o cer','officer'),('o cers','officers'),
        ('su cient','sufficient'),('su ciently','sufficiently'),
        ('pro ciency','proficiency'),('pro cient','proficient'),
        ('a iction','affliction'),
        ('e ect','effect'),('e ects','effects'),('e ective','effective'),('e ectively','effectively'),
        ('e ectiveness','effectiveness'),
        ('a ect','affect'),('a ects','affects'),('a ected','affected'),('a ecting','affecting'),
        ('a ord','afford'),('a ords','affords'),
        ('o ense','offense'),('O ense','Offense'),('o ensive','offensive'),('O ensive','Offensive'),
        ('o er ','offer '),('o ered','offered'),('o ers','offers'),('o ering','offering'),
        ('di erent','different'),('di erently','differently'),('di erence','difference'),
        ('di cult','difficult'),('di culty','difficulty'),
        ('su er','suffer'),('su ered','suffered'),('su ering','suffering'),
        ('bo er','boffer'),('bo ers','boffers'),('bu alo','buffalo'),
        ('speci c','specific'),('speci cs','specifics'),('speci ed','specified'),
        ('speci cally','specifically'),('speci es','specifies'),
        ('signi cant','significant'),('signi cantly','significantly'),
        ('clari cation','clarification'),('clari ed','clarified'),
        ('forti cation','fortification'),('forti cations','fortifications'),
        ('forti ed','fortified'),('forti y','fortify'),
        ('modi cation','modification'),('modi cations','modifications'),
        ('modi er','modifier'),('modi ers','modifiers'),('modi ed','modified'),('modi y','modify'),
        ('ful lled','fulfilled'),('ful ll','fulfill'),('ful lling','fulfilling'),
        ('sacri ce','sacrifice'),('sacri ces','sacrifices'),('sacri cing','sacrificing'),
        ('de ned','defined'),('de ne','define'),('de nes','defines'),('de nition','definition'),
        ('classi cation','classification'),('classi ed','classified'),
        ('identi ed','identified'),('identi es','identifies'),('identi y','identify'),
        ('identi cation','identification'),
        ('Paci ed','Pacified'),('paci ed','pacified'),('paci y','pacify'),
        ('con rmed','confirmed'),('con rm','confirm'),
        ('bene t','benefit'),('bene ts','benefits'),('bene cial','beneficial'),
        ('pro le','profile'),('brie ng','briefing'),('brie y','briefly'),
        ('digni ed','dignified'),('magni cent','magnificent'),
        ('puri ed','purified'),('puri y','purify'),
        ('satis ed','satisfied'),('horri ed','horrified'),('horri c','horrific'),
        ('terri ed','terrified'),('arti cial','artificial'),
        ('noti ed','notified'),('justi ed','justified'),
        ('in uence','influence'),('in uences','influences'),
        ('in uential','influential'),('in uencing','influencing'),
        ('in ux','influx'),('in icted','inflicted'),('in ict','inflict'),
        ('con ict','conflict'),('con icts','conflicts'),('con icted','conflicted'),
        ('re ect','reflect'),('re ected','reflected'),('re ective','reflective'),
        ('fe owship','fellowship'),("gi s","gifts"),
    ]
    for old,new in subs: t = t.replace(old,new)
    initials = [
        (' eld','field'),(' elds','fields'),(' rst','first'),
        (' ght','fight'),(' ghting','fighting'),(' ghter','fighter'),(' ghters','fighters'),(' ghts','fights'),
        (' nd','find'),(' nding','finding'),(' nds','finds'),
        (' re','fire'),(' res','fires'),(' fteen','fifteen'),(' fth','fifth'),
        (' nished','finished'),(' nish','finish'),
        (' lled','filled'),(' ll','fill'),(' lling','filling'),
        (' ne','fine'),(' ner','finer'),(' nest','finest'),
        (' nal','final'),(' nalize','finalize'),(' nalized','finalized'),(' nally','finally'),
        (' gure','figure'),(' gures','figures'),(' gured','figured'),
        (' x','fix'),(' xed','fixed'),
        (' nger','finger'),(' ngers','fingers'),(' ngernails','fingernails'),(' ngertips','fingertips'),
        (' erce','fierce'),(' ercely','fiercely'),
        (' esh','flesh'),(' eshed','fleshed'),(' oor','floor'),
        (' ow','flow'),(' owing','flowing'),(' ows','flows'),
        (' ight','flight'),(' ighty','flighty'),(' ying','flying'),
        (' ock','flock'),(' ocks','flocks'),(' at','flat'),
        (' avored','flavored'),(' avorful','flavorful'),(' avor','flavor'),
        (' uency','fluency'),(' uencies','fluencies'),(' ourishing','flourishing'),
        (' ux','flux'),(' ee','flee'),(' eeing','fleeing'),
        (' ames','flames'),(' ame','flame'),(' ask','flask'),
    ]
    for old,new in initials:
        t = re.sub(r'(?<=\s)' + re.escape(old) + r'\b', ' '+new, t)
        t = re.sub(r'^' + re.escape(old.lstrip()) + r'\b', new, t, flags=re.MULTILINE)
    for old,new in [('Wild re','Wildfire'),('wild re','wildfire'),('camp res','campfires'),
                     ('camp re','campfire'),('battle elds','battlefields'),('battle eld','battlefield'),
                     ('Su ocate','Suffocate'),('su ocate','suffocate'),('In ame','Inflame'),
                     ('Sta Touch','Staff Touch'),('sta  ','staff '),('Sta  ','Staff '),
                     ('sign-o ','sign-off'),(' ga e ',' gaffe ')]:
        t = t.replace(old,new)
    return t

def remove_artifacts(t):
    lines = t.split('\n')
    out = []
    for line in lines:
        s = line.strip()
        if re.match(r'^\d{1,3}$', s): continue
        if s in ('fi','fl','ff','ffi','ffl','ft','ll','f'): continue
        if s and all(c in '◻︎ \t' for c in s): continue
        if s == 'Chapter Title Page': continue
        if s == '(front cover)': continue
        if s.startswith('(Picture:'): continue
        out.append(line)
    return '\n'.join(out)

def e(text):
    return H.escape(text)

# --- Read and clean ---
raw = read('/Users/robennals/broomy-repos/rob-home/project/falnorian/rulebook_layout.txt')
text = remove_artifacts(raw)
text = fix_ligatures(text)
lines = text.split('\n')

# --- Classify each line ---
# For each line: (stripped_text, indent, raw_length, is_blank)
classified = []
for line in lines:
    s = line.strip()
    indent = len(line) - len(line.lstrip()) if s else 0
    classified.append({
        'text': s,
        'indent': indent,
        'raw_len': len(line.rstrip()),
        'blank': s == '',
        'raw': line,
    })

N = len(classified)

def next_nonblank(idx):
    """Return index of next non-blank line after idx, or N."""
    j = idx + 1
    while j < N and classified[j]['blank']:
        j += 1
    return j

def is_two_column(line_text):
    """Detect if a line has two-column layout (big gap in middle)."""
    return bool(re.search(r'\S\s{4,}\S', line_text))

# --- Detect TOC region ---
toc_start = None
toc_end = None
for idx in range(N):
    if classified[idx]['text'] == 'Table of Contents':
        toc_start = idx
    if toc_start and idx > toc_start + 2 and classified[idx]['text'].startswith('This rulebook is'):
        toc_end = idx
        break

# Parse TOC: split two-column lines into left/right
toc_left = []
toc_right = []
if toc_start and toc_end:
    for idx in range(toc_start + 1, toc_end):
        raw = classified[idx]['raw']
        s = classified[idx]['text']
        if not s: continue
        # Split at column ~50
        mid = 50
        left = raw[:mid].rstrip()
        right = raw[mid:].strip() if len(raw) > mid else ''
        # Parse "Title    PageNum" pattern
        def parse_entry(part):
            part = part.strip()
            if not part: return None
            m = re.match(r'(.+?)\s{2,}(\d+)\s*$', part)
            if m:
                return (m.group(1).strip(), m.group(2))
            return (part, '')
        le = parse_entry(left)
        re2 = parse_entry(right)
        if le: toc_left.append(le)
        if re2: toc_right.append(re2)

# --- Build HTML ---
out = []
out.append('''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Falnorian Rulebook</title>
<style>
body { font-family: Georgia, "Times New Roman", serif; max-width: 45em; margin: 2em auto; padding: 0 1em; line-height: 1.6; color: #222; background: #faf8f5; }
h1 { font-size: 2em; margin: 1.5em 0 0.3em; border-bottom: 2px solid #555; padding-bottom: 0.3em; }
h2 { font-size: 1.6em; margin: 1.8em 0 0.5em; border-bottom: 1px solid #999; padding-bottom: 0.2em; color: #333; }
h3 { font-size: 1.25em; margin: 1.4em 0 0.4em; color: #444; }
h4 { font-size: 1.1em; margin: 1em 0 0.3em; }
p { margin: 0.5em 0; }
ul { margin: 0.5em 0 0.5em 1.5em; }
li { margin: 0.2em 0; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 0.93em; }
th, td { border: 1px solid #aaa; padding: 0.3em 0.6em; text-align: left; }
th { background: #e8e4df; font-weight: bold; }
tr:nth-child(even) { background: #f4f2ef; }
.boxed { background: #f0ede8; border: 1px solid #ccc; padding: 1em; margin: 1em 0; border-radius: 4px; }
.boxed h4 { margin-top: 0; }
.poem { font-style: italic; margin: 1.5em 0; padding: 0.5em 1em; border-left: 3px solid #bbb; }
.uc { color: #888; font-style: italic; margin: 1em 0; padding: 0.5em; border: 1px dashed #aaa; }
.toc p { margin: 0.1em 0; }
.toc .ch { font-weight: bold; }
.toc .sub { margin-left: 1.5em; }
</style></head><body>
''')

# Big chapter headings
chapter_names = {
    'Falnorian Rulebook', 'Introduction Section', 'Adventuring Basics', 'Character Creation',
    'Classes', 'Supporting Class Information', 'Expanded Mechanics',
    'Markets & Price Lists', 'Monster Book', 'Junior League', 'Animals',
}

i = 0
para_words = []
in_ul = False

def flush():
    global para_words
    if para_words:
        out.append(f'<p>{e(" ".join(para_words))}</p>\n')
        para_words = []

def end_ul():
    global in_ul
    if in_ul:
        out.append('</ul>\n')
        in_ul = False

while i < N:
    c = classified[i]
    s = c['text']
    indent = c['indent']

    # Skip blanks (they just flush paragraphs)
    if c['blank']:
        flush()
        i += 1
        continue

    # Skip UNDER CONSTRUCTION
    if 'UNDER CONSTRUCTION' in s:
        flush(); end_ul()
        out.append('<div class="uc">— Under Construction —</div>\n')
        i += 1
        continue

    # Dedication poem
    if 'years of fellowship' in s.lower() or ('years of fe' in s.lower() and 'owship' in s.lower()):
        flush(); end_ul()
        out.append('<div class="poem">\n')
        while i < N:
            cs = classified[i]['text']
            if cs == '':
                # If next non-blank is Table of Contents, stop
                j = next_nonblank(i)
                if j < N and 'Table of Contents' in classified[j]['text']:
                    break
                if j < N and classified[j]['blank']:
                    break
                i += 1
                continue
            if 'Table of Contents' in cs:
                break
            out.append(f'{e(cs)}<br>\n')
            i += 1
        out.append('</div>\n')
        continue

    # TOC
    if s == 'Table of Contents' and toc_start is not None:
        flush(); end_ul()
        out.append('<h2>Table of Contents</h2>\n<div class="toc">\n')
        # Left column then right column
        for entries in [toc_left, toc_right]:
            for title, page in entries:
                is_chapter = any(title == cn for cn in chapter_names) or not page or title in ('Adventuring Rules','Markets & Price Lists','Monster Book','Junior League')
                cls = 'ch' if (is_chapter or indent < 3) else 'sub'
                # Heuristic: if the entry was indented in source, it's a sub-entry
                # Actually just check if title is in chapter_names
                if title in chapter_names or title in ('Adventuring Rules',):
                    cls = 'ch'
                else:
                    cls = 'sub'
                pg = f' &mdash; {page}' if page else ''
                out.append(f'<p class="{cls}">{e(title)}{pg}</p>\n')
        out.append('</div>\n')
        i = toc_end if toc_end else i + 1
        continue

    # Bullet points
    if s.startswith('• ') or s.startswith('• '):
        flush()
        if not in_ul:
            out.append('<ul>\n')
            in_ul = True
        out.append(f'<li>{e(s[2:].strip())}</li>\n')
        i += 1
        continue
    else:
        if in_ul:
            # Check if this is a continuation of a bullet (indented under bullet)
            if indent > 6 and i > 0 and (classified[i-1]['text'].startswith('•') or classified[i-1]['indent'] > 6):
                # Continuation of bullet - append to previous li
                # Actually just make a new li with extra indent indicator
                out.append(f'<li style="margin-left:1.5em">{e(s)}</li>\n')
                i += 1
                continue
            end_ul()

    # Detect headings structurally:
    # A heading is: a short line (< 60 chars, no period at end) where the
    # NEXT non-blank line is indented more than this line
    is_heading = False
    if len(s) < 70 and not s.endswith('.') and not s.endswith(',') and not s.startswith('•'):
        j = next_nonblank(i)
        if j < N:
            next_indent = classified[j]['indent']
            next_text = classified[j]['text']
            # Heading if next line is more indented, OR if current line matches known pattern
            if next_indent > indent + 3 and not next_text.startswith('•'):
                is_heading = True
            # Also heading if it's a known chapter name
            if s in chapter_names:
                is_heading = True

    if is_heading:
        flush(); end_ul()
        if s in chapter_names or s == 'Falnorian Rulebook':
            if s == 'Falnorian Rulebook':
                out.append(f'<h1>{e(s)}</h1>\n')
            else:
                out.append(f'<h2>{e(s)}</h2>\n')
        else:
            # Determine h3 vs h4 - use h3 for now
            out.append(f'<h3>{e(s)}</h3>\n')
        i += 1
        continue

    # Stat lines: "2HP, 2 Mana, Size 3..."
    if re.match(r'^\d+HP,\s', s) or re.match(r'^Variable HP', s) or re.match(r'^Base HP', s):
        flush()
        out.append(f'<p><strong>{e(s)}</strong></p>\n')
        i += 1
        continue

    # Labeled fields (monster stat blocks, etc)
    label_match = re.match(r'^(Creature Type|Offense|Defense|Passive|Senses & Mobility|Habitat|Play Notes|Restrictions|Stat Bonuses|Abilities|Max AV|Warrior Ability|Appearance|Description|In Falnorian|Starting Gold|Additional Training|Add\. Training):\s*(.*)', s)
    if label_match:
        flush()
        label = label_match.group(1) + ':'
        rest = label_match.group(2)
        out.append(f'<p><strong>{e(label)}</strong> {e(rest)}</p>\n')
        i += 1
        continue

    # Numbered skill lines: "1. Something" or "4A. Something"
    skill_match = re.match(r'^(\d+[A-Z]?)\.\s+(.+)', s)
    if skill_match:
        flush()
        out.append(f'<p><strong>{e(skill_match.group(1))}.</strong> {e(skill_match.group(2))}</p>\n')
        i += 1
        continue

    # Two-column lines: if there's a big gap, just keep as-is for now
    # (tables will need manual fixing later)

    # Default: add to paragraph buffer (joining wrapped lines)
    para_words.append(s)
    i += 1

flush()
end_ul()
out.append('</body></html>\n')

output = ''.join(out)
with open('/Users/robennals/broomy-repos/rob-home/project/falnorian/falnorian_rulebook.html', 'w') as f:
    f.write(output)

print(f"Done: {len(output)} chars, TOC: {len(toc_left)}L + {len(toc_right)}R entries")
