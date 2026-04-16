# falnorian-epub

Nicer formatted EPUB of the Falnorian rulebook.

A small pipeline that turns the source PDF (`falnorianrulebookapril2025.pdf`)
into a cleaned, well-formatted rulebook. `pdftotext` extracts split ligatures
(fi, fl, ff, ffi, ffl) as orphaned characters, so these scripts repair the
broken words and rebuild structure (headings, TOC, bullets, stat blocks) into
HTML.

## Files

- `convert.py` — full structural pass over `rulebook_layout.txt` → HTML
- `build_html.py` — ligature/artifact cleanup → `rulebook_cleaned.txt`
- `convert_to_html.py` — earlier ligature-fix prototype
- `falnorian_rulebook.epub` — generated EPUB output

The source PDF, intermediate text extracts, page-image JPGs, and the large
generated HTML are gitignored — they're regeneratable locally and too heavy
for the repo.
