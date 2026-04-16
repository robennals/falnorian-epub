#!/usr/bin/env python3
"""Convert Falnorian Rulebook PDF text to well-formatted HTML."""

import re

def read_layout_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def clean_ligature_artifacts(text):
    """Remove orphaned ligature characters that pdftotext splits out."""
    # Remove lines that are just ligature fragments (fi, fl, ff, ffi, ffl)
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Skip lines that are just ligature fragments
        if stripped in ('fi', 'fl', 'ff', 'ffi', 'ffl', 'ft', 'll', 'f'):
            continue
        # Skip standalone page numbers on their own line
        if re.match(r'^\d{1,3}$', stripped):
            continue
        cleaned.append(line)
    return '\n'.join(cleaned)

def fix_broken_words(text):
    """Fix words broken by ligature extraction."""
    # Common broken words from fi ligature
    fixes = {
        r'\bspeci c\b': 'specific',
        r'\b eld\b': 'field',
        r'\b rst\b': 'first',
        r'\b ght\b': 'fight',
        r'\b ghting\b': 'fighting',
        r'\b ghter\b': 'fighter',
        r'\b ghters\b': 'fighters',
        r'\b ghts\b': 'fights',
        r'\b nd\b': 'find',
        r'\b nding\b': 'finding',
        r'\b re\b': 'fire',
        r'\b fteen\b': 'fifteen',
        r'\b nished\b': 'finished',
        r'\b nish\b': 'finish',
        r'\b lled\b': 'filled',
        r'\b ll\b': 'fill',
        r'\b lling\b': 'filling',
        r'\b ne\b': 'fine',
        r'\b nal\b': 'final',
        r'\b nalize\b': 'finalize',
        r'\b nalized\b': 'finalized',
        r'\b gure\b': 'figure',
        r'\bclari cation\b': 'clarification',
        r'\bforti cation\b': 'fortification',
        r'\bforti cations\b': 'fortifications',
        r'\bmodi cation\b': 'modification',
        r'\bmodi cations\b': 'modifications',
        r'\bmodi er\b': 'modifier',
        r'\bmodi ers\b': 'modifiers',
        r'\bmodi ed\b': 'modified',
        r'\bsigni cant\b': 'significant',
        r'\bsigni cantly\b': 'significantly',
        r'\bful lled\b': 'fulfilled',
        r'\bpro ciency\b': 'proficiency',
        r'\bpro cient\b': 'proficient',
        r'\bsacri ce\b': 'sacrifice',
        r'\bsacri ces\b': 'sacrifices',
        r'\bsacri cing\b': 'sacrificing',
        r'\bde ned\b': 'defined',
        r'\bde ne\b': 'define',
        r'\bclassi cation\b': 'classification',
        r'\bidenti ed\b': 'identified',
        r'\bidenti es\b': 'identifies',
        r'\bueozoa\b': 'influence',  # skip this one
        # fl ligature
        r'\b esh\b': 'flesh',
        r'\b eshed\b': 'fleshed',
        r'\b oor\b': 'floor',
        r'\b ow\b': 'flow',
        r'\b owing\b': 'flowing',
        r'\b ight\b': 'flight',
        r'\b ighty\b': 'flighty',
        r'\b ying\b': 'flying',
        r'\b ock\b': 'flock',
        r'\b ocks\b': 'flocks',
        r'\b at\b': 'flat',
        r'\b avored\b': 'flavored',
        r'\b avorful\b': 'flavorful',
        r'\b avor\b': 'flavor',
        r'\b uency\b': 'fluency',
        r'\b uencies\b': 'fluencies',
        r'\b ourishing\b': 'flourishing',
        r'\b ux\b': 'flux',
        r'\b ee\b': 'flee',
        r'\bin uence\b': 'influence',
        r'\bin uential\b': 'influential',
        r'\bin uencing\b': 'influencing',
        r'\bin ux\b': 'influx',
        r'\bin icted\b': 'inflicted',
        r'\bcon ict\b': 'conflict',
        r'\bcon icts\b': 'conflicts',
        r'\bcon icted\b': 'conflicted',
        r'\bre ect\b': 'reflect',
        r'\bre ected\b': 'reflected',
        r'\bre ective\b': 'reflective',
        r'\bre ect magic\b': 'reflect magic',
        # ff ligature
        r'\be ect\b': 'effect',
        r'\be ects\b': 'effects',
        r'\be ective\b': 'effective',
        r'\be ectively\b': 'effectively',
        r'\ba ect\b': 'affect',
        r'\ba ects\b': 'affects',
        r'\ba ected\b': 'affected',
        r'\ba ecting\b': 'affecting',
        r'\bo ense\b': 'offense',
        r'\bo ensive\b': 'offensive',
        r'\bo er\b': 'offer',
        r'\bo ered\b': 'offered',
        r'\bdi erent\b': 'different',
        r'\bdi erently\b': 'differently',
        r'\bdi cult\b': 'difficult',
        r'\bdi culty\b': 'difficulty',
        r'\bbo er\b': 'boffer',
        r'\bbo ers\b': 'boffers',
        r'\bbu alo\b': 'buffalo',
        r'\bsu er\b': 'suffer',
        r'\bsu ered\b': 'suffered',
        r'\bsu ering\b': 'suffering',
        r'\bsu cient\b': 'sufficient',
        r'\bsu ciently\b': 'sufficiently',
        r'\bsta \b': 'staff ',
        r'\bSta \b': 'Staff ',
        r'\bo cial\b': 'official',
        r'\ba ord\b': 'afford',
        r'\ba iction\b': 'affliction',
        r'\bga e\b': 'gaffe',
        r'\bsueozoa\b': 'suffocate', # skip
        # ffi ligature
        r'\be ciency\b': 'efficiency',
        r'\be cient\b': 'efficient',
        r'\bo cers\b': 'officers',
        r'\bsu ciency\b': 'sufficiency',
    }
    for pattern, replacement in fixes.items():
        text = re.sub(pattern, replacement, text)

    # Also fix "Su ocate" -> "Suffocate"
    text = text.replace('Su ocate', 'Suffocate')
    text = text.replace('In ame', 'Inflame')
    text = text.replace('Wild re', 'Wildfire')
    text = text.replace('camp res', 'campfires')
    text = text.replace('camp re', 'campfire')
    text = text.replace('battle elds', 'battlefields')
    text = text.replace('battle eld', 'battlefield')
    text = text.replace('A ffliction', 'Affliction')
    text = text.replace(' ngernails', 'fingernails')
    text = text.replace(' ngertips', 'fingertips')
    text = text.replace(' ngers', 'fingers')
    text = text.replace(' erce', 'fierce')
    text = text.replace(' ercely', 'fiercely')
    text = text.replace('Paci ed', 'Pacified')
    text = text.replace('ceozoa re', 'fire')

    return text

def html_escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# Read the full raw text
raw = read_layout_text('/Users/robennals/broomy-repos/rob-home/project/falnorian/rulebook_full.txt')

# Clean up
text = clean_ligature_artifacts(raw)
text = fix_broken_words(text)

# Write cleaned text for inspection
with open('/Users/robennals/broomy-repos/rob-home/project/falnorian/rulebook_cleaned.txt', 'w') as f:
    f.write(text)

print(f"Cleaned text: {len(text)} chars")
print("First 2000 chars:")
print(text[:2000])
