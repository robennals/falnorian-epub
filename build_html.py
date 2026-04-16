#!/usr/bin/env python3
"""Build a well-formatted HTML version of the Falnorian Rulebook from the cleaned text."""

import re

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def fix_ligatures(text):
    """Fix broken ligatures from PDF extraction.

    pdftotext extracts ligatures (fi, fl, ff, ffi, ffl) as separate chars on
    their own lines at page bottom, leaving a space in the word where the
    ligature was. So 'specific' becomes 'speci c' and 'field' becomes ' eld'.
    """

    # Word-internal breaks: ' c' was 'fic', ' t' was 'fit', etc.
    # Use simple string replacement with careful ordering
    word_internal = [
        # ffi -> ' ci' or 'ffi ci'
        ('e ciency', 'efficiency'), ('e cient', 'efficient'),
        ('o cial', 'official'), ('o cially', 'officially'),
        ('o cer', 'officer'), ('o cers', 'officers'),
        ('su cient', 'sufficient'), ('su ciently', 'sufficiently'),
        ('su ciency', 'sufficiency'),
        ('pro ciency', 'proficiency'), ('pro cient', 'proficient'),
        ('de ciency', 'deficiency'), ('de cient', 'deficient'),

        # ffl -> ' l'
        ('a iction', 'affliction'),

        # ff -> ' '  (two chars become space)
        ('e ect', 'effect'), ('e ects', 'effects'),
        ('e ective', 'effective'), ('e ectively', 'effectively'),
        ('e ectiveness', 'effectiveness'),
        ('a ect', 'affect'), ('a ects', 'affects'),
        ('a ected', 'affected'), ('a ecting', 'affecting'),
        ('a ord', 'afford'), ('a ords', 'affords'),
        ('di erent', 'different'), ('di erently', 'differently'),
        ('di erence', 'difference'), ('di erences', 'differences'),
        ('di cult', 'difficult'), ('di culty', 'difficulty'),
        ('su er', 'suffer'), ('su ered', 'suffered'),
        ('su ering', 'suffering'), ('su ers', 'suffers'),
        ('o ense', 'offense'), ('o ensive', 'offensive'),
        ('O ense', 'Offense'), ('O ensive', 'Offensive'),
        ('o er ', 'offer '), ('o ered', 'offered'), ('o ers', 'offers'),
        ('o ering', 'offering'),
        ('bo er', 'boffer'), ('bo ers', 'boffers'),
        ('bu alo', 'buffalo'),
        ('shu e', 'shuffle'), ('scu e', 'scuffle'),
        ('ba e', 'baffle'), ('ba ed', 'baffled'),

        # fi -> ' ' (two chars become space)
        ('speci c', 'specific'), ('speci cs', 'specifics'),
        ('speci ed', 'specified'), ('speci cally', 'specifically'),
        ('speci es', 'specifies'),
        ('signi cant', 'significant'), ('signi cantly', 'significantly'),
        ('signi cance', 'significance'),
        ('clari cation', 'clarification'), ('clari ed', 'clarified'),
        ('forti cation', 'fortification'), ('forti cations', 'fortifications'),
        ('forti ed', 'fortified'), ('forti y', 'fortify'),
        ('modi cation', 'modification'), ('modi cations', 'modifications'),
        ('modi er', 'modifier'), ('modi ers', 'modifiers'),
        ('modi ed', 'modified'), ('modi y', 'modify'),
        ('ful lled', 'fulfilled'), ('ful ll', 'fulfill'),
        ('ful lling', 'fulfilling'),
        ('sacri ce', 'sacrifice'), ('sacri ces', 'sacrifices'),
        ('sacri cing', 'sacrificing'),
        ('de ned', 'defined'), ('de ne', 'define'),
        ('de nes', 'defines'), ('de nition', 'definition'),
        ('classi cation', 'classification'), ('classi ed', 'classified'),
        ('identi ed', 'identified'), ('identi es', 'identifies'),
        ('identi y', 'identify'), ('identi cation', 'identification'),
        ('Paci ed', 'Pacified'), ('paci ed', 'pacified'),
        ('paci y', 'pacify'),
        ('con rmed', 'confirmed'), ('con rm', 'confirm'),
        ('con rms', 'confirms'),
        ('bene t', 'benefit'), ('bene ts', 'benefits'),
        ('bene cial', 'beneficial'),
        ('pro le', 'profile'), ('pro les', 'profiles'),
        ('brie ng', 'briefing'), ('brie y', 'briefly'),
        ('digni ed', 'dignified'),
        ('certi cate', 'certificate'),
        ('magni cent', 'magnificent'),
        ('puri ed', 'purified'), ('puri y', 'purify'),
        ('satis ed', 'satisfied'), ('satis y', 'satisfy'),
        ('horri ed', 'horrified'), ('horri c', 'horrific'),
        ('terri ed', 'terrified'), ('terri c', 'terrific'),
        ('arti cial', 'artificial'),
        ('noti ed', 'notified'), ('noti y', 'notify'),
        ('justi ed', 'justified'), ('justi y', 'justify'),
        ('ampli ed', 'amplified'), ('ampli y', 'amplify'),
        ('solidi ed', 'solidified'),

        # fl -> ' ' (two chars become space)
        ('in uence', 'influence'), ('in uences', 'influences'),
        ('in uential', 'influential'), ('in uencing', 'influencing'),
        ('in ux', 'influx'),
        ('in icted', 'inflicted'), ('in ict', 'inflict'),
        ('con ict', 'conflict'), ('con icts', 'conflicts'),
        ('con icted', 'conflicted'),
        ('re ect', 'reflect'), ('re ected', 'reflected'),
        ('re ective', 'reflective'), ('re ection', 'reflection'),
    ]

    for broken, fixed in word_internal:
        text = text.replace(broken, fixed)

    # Word-initial fi breaks: ' eld' -> 'field', ' rst' -> 'first'
    # These appear as space+remaining after fi is removed
    # We need to use regex to avoid false positives
    initial_breaks = [
        # fi-initial words (the 'fi' becomes a space)
        (r' eld\b', ' field'), (r' elds\b', ' fields'),
        (r' rst\b', ' first'),
        (r' ght\b', ' fight'), (r' ghting\b', ' fighting'),
        (r' ghter\b', ' fighter'), (r' ghters\b', ' fighters'),
        (r' ghts\b', ' fights'),
        (r' nd\b', ' find'), (r' nding\b', ' finding'), (r' nds\b', ' finds'),
        (r' re\b', ' fire'), (r' res\b', ' fires'),
        (r' fteen\b', ' fifteen'), (r' fth\b', ' fifth'),
        (r' nished\b', ' finished'), (r' nish\b', ' finish'),
        (r' lled\b', ' filled'), (r' ll\b', ' fill'),
        (r' lling\b', ' filling'),
        (r' ne\b', ' fine'), (r' ner\b', ' finer'), (r' nest\b', ' finest'),
        (r' nal\b', ' final'), (r' nalize\b', ' finalize'),
        (r' nalized\b', ' finalized'), (r' nally\b', ' finally'),
        (r' gure\b', ' figure'), (r' gures\b', ' figures'),
        (r' gured\b', ' figured'),
        (r' x\b', ' fix'), (r' xed\b', ' fixed'), (r' xes\b', ' fixes'),
        (r' nger\b', ' finger'), (r' ngers\b', ' fingers'),
        (r' ngernails\b', ' fingernails'), (r' ngertips\b', ' fingertips'),
        (r' erce\b', ' fierce'), (r' ercely\b', ' fiercely'),
        (r' lter\b', ' filter'), (r' lters\b', ' filters'),
        (r' le\b', ' file'), (r' les\b', ' files'),

        # fl-initial words
        (r' esh\b', ' flesh'), (r' eshed\b', ' fleshed'),
        (r' oor\b', ' floor'), (r' oors\b', ' floors'),
        (r' ow\b', ' flow'), (r' owing\b', ' flowing'),
        (r' ows\b', ' flows'),
        (r' ight\b', ' flight'), (r' ighty\b', ' flighty'),
        (r' ying\b', ' flying'), (r' ies\b', ' flies'),
        (r' ock\b', ' flock'), (r' ocks\b', ' flocks'),
        (r' at\b', ' flat'), (r' atten\b', ' flatten'),
        (r' avored\b', ' flavored'), (r' avorful\b', ' flavorful'),
        (r' avor\b', ' flavor'),
        (r' uency\b', ' fluency'), (r' uencies\b', ' fluencies'),
        (r' ourishing\b', ' flourishing'),
        (r' ux\b', ' flux'),
        (r' ee\b', ' flee'), (r' eeing\b', ' fleeing'),
        (r' ames\b', ' flames'), (r' ame\b', ' flame'),
        (r' ags\b', ' flags'), (r' ag\b', ' flag'),
        (r' ash\b', ' flash'),
        (r' ask\b', ' flask'),

        # ff-initial (rare, but sta  -> staff)
    ]

    for pattern, replacement in initial_breaks:
        text = re.sub(pattern, replacement, text)

    # Direct string replacements for remaining specific cases
    text = text.replace('fe owship', 'fellowship')
    text = text.replace("gi s", "gifts")
    text = text.replace('Wild re', 'Wildfire')
    text = text.replace('wild re', 'wildfire')
    text = text.replace('camp res', 'campfires')
    text = text.replace('camp re', 'campfire')
    text = text.replace('battle elds', 'battlefields')
    text = text.replace('battle eld', 'battlefield')
    text = text.replace('Su ocate', 'Suffocate')
    text = text.replace('su ocate', 'suffocate')
    text = text.replace('In ame', 'Inflame')
    text = text.replace('in ame', 'inflame')
    text = text.replace('Sta Touch', 'Staff Touch')
    text = text.replace('sta  ', 'staff ')
    text = text.replace('Sta  ', 'Staff ')
    text = text.replace('sign-o ', 'sign-off')
    text = text.replace(' ga e ', ' gaffe ')
    text = text.replace('ga er', 'gaffer')

    return text


def remove_page_artifacts(text):
    """Remove page numbers and ligature-only lines."""
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        s = line.strip()
        if re.match(r'^\d{1,3}$', s):
            continue
        if s in ('fi', 'fl', 'ff', 'ffi', 'ffl', 'ft', 'll', 'f'):
            continue
        cleaned.append(line)
    return '\n'.join(cleaned)


# Read and clean
raw = read_file('/Users/robennals/broomy-repos/rob-home/project/falnorian/rulebook_layout.txt')
text = remove_page_artifacts(raw)
text = fix_ligatures(text)

# Verify
for word, broken in [('specific', 'speci c'), ('field', ' eld'), ('first', ' rst'),
                      ('fight', ' ght'), ('effect', 'e ect'), ('different', 'di erent'),
                      ('difficult', 'di cult'), ('influence', 'in uence'),
                      ('sufficient', 'su cient'), ('flesh', ' esh')]:
    found = text.lower().count(word)
    still_broken = text.count(broken)
    print(f"  {word}: {found} found, {still_broken} still broken")

with open('/Users/robennals/broomy-repos/rob-home/project/falnorian/rulebook_cleaned.txt', 'w') as f:
    f.write(text)

print(f"\nSaved: {len(text)} chars")
