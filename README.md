# Weijia Wang – Academic Website

Personal academic website: https://wweijia0107.github.io/

Static HTML/CSS/JavaScript, ready for GitHub Pages. Updated November 23, 2026.

## Content

- `index.html`: research, publication, accepted AGU/AAG presentations, awards, service, education, and experience.
- `styles.css` and `script.js`: responsive visual style and accessible mobile menu.
- `publications.bib`: WACV 2026 workshop paper, including DOI and official open-access link.
- `CV-Weijia_Wang.pdf`: downloadable two-page academic CV.
- `scripts/build_cv.py`: reproducible ReportLab PDF source; requires `reportlab`.

## Deploy

Upload the **contents** of this folder to the root of the `main` branch of the `wweijia0107/wweijia0107.github.io` repository, replacing files with the same names. Keep Pages configured to deploy from `main` / `(root)`.

Because this is a newly generated deployment bundle based on the existing site's visible structure and design, inspect the `index.html` diff before upload to confirm that any customizations made to the live repository after September 30 are retained.

Run locally using `python -m http.server 8000` and open `http://127.0.0.1:8000/`.

## Editorial accuracy

- WACV 2026 is a peer-reviewed **workshop paper**, not a main-conference paper.
- Harvard CGA award is a workshop travel grant, with no unverified amount claimed.
- AGU 2026 and AAG 2027 are accepted/upcoming presentations as of November 23, 2026.
- The survey's university ethics review was an **exempt determination** (August 2026), not publication of results.
