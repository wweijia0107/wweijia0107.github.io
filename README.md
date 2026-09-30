# Weijia Wang - Academic Website

Personal academic website: https://wweijia0107.github.io/

Plain HTML, CSS, and JavaScript. No framework, build step, external fonts, or analytics.
GitHub Pages publishes the `main` branch from the repository root.

## Content

- `index.html`: profile, research, publications, experience, academic service, education, and projects.
- `styles.css`: responsive layout, accessible focus states, reduced-motion support, and print styles.
- `script.js`: mobile section navigation and active-section indicator; the content works without JavaScript.
- `publications.bib`: downloadable publication citation, checked against the CVF proceedings.
- `CV-Weijia_Wang.pdf`: current downloadable CV.
- `scripts/build_cv.py`: CV source, using ReportLab (`python -m pip install reportlab`).

## Preview

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Open http://127.0.0.1:8000/ and check the desktop and mobile layouts.

## Update

Edit the relevant entries in `index.html` and update its `<time>` element.
Update `scripts/build_cv.py` and run it from the repository root to regenerate the CV.
Preserve exact publication titles and distinguish workshop service from main-conference service.
The SDL role describes participation in the internship program, including the current proposal stage.

Changes pushed to `main` are published by GitHub Pages. Review the live website after the Pages build completes.
