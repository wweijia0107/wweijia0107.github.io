"""Generate the two-page public academic CV used by wweijia0107.github.io.

Dependencies: Python 3.10+ and reportlab.
Run: python scripts/build_cv.py
Source reviewed and updated on November 23, 2026.
"""
from __future__ import annotations

import argparse
from functools import partial
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    HRFlowable, KeepTogether, PageBreak, Paragraph,
    SimpleDocTemplate, Spacer, Table, TableStyle,
)

PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN = 43
BODY_WIDTH = PAGE_WIDTH - MARGIN * 2
INK = colors.HexColor('#233039')
MUTED = colors.HexColor('#58656e')
RULE = colors.HexColor('#b6c3c3')
LINK = '#215a57'
UPDATED = 'November 2026'

STYLES = {
    'name': ParagraphStyle('Name', fontName='Times-Bold', fontSize=25.5,
                           leading=27, textColor=INK, spaceAfter=3),
    'body': ParagraphStyle('Body', fontName='Helvetica', fontSize=9.3,
                           leading=12.35, textColor=INK, spaceAfter=2.5),
    'detail': ParagraphStyle('Detail', fontName='Helvetica', fontSize=9.1,
                             leading=12.0, textColor=MUTED, spaceAfter=2.0),
    'date': ParagraphStyle('Date', fontName='Helvetica', fontSize=8.6,
                           leading=11.8, alignment=TA_RIGHT, textColor=MUTED),
    'section': ParagraphStyle('Section', fontName='Times-Bold', fontSize=12.4,
                              leading=15, spaceBefore=7.7, spaceAfter=3,
                              keepWithNext=True, textColor=INK),
    'bullet': ParagraphStyle('Bullet', fontName='Helvetica', fontSize=9.1,
                             leading=12, leftIndent=11, firstLineIndent=-8,
                             spaceAfter=2, textColor=INK),
    'contact': ParagraphStyle('Contact', fontName='Helvetica', fontSize=9.3,
                              leading=12, textColor=MUTED, spaceAfter=2),
}


def p(s: str, kind: str = 'body') -> Paragraph:
    return Paragraph(s, STYLES[kind])


def section(name: str) -> list:
    rule = HRFlowable(width='100%', thickness=.55, color=RULE, spaceAfter=4)
    rule.keepWithNext = True
    return [p(name, 'section'), rule]


def dated(title: str, date: str) -> Table:
    table = Table([[p('<b>' + title + '</b>'), p(date, 'date')]],
                  colWidths=[BODY_WIDTH - 127, 127], hAlign='LEFT')
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    return table


def bullet(s: str) -> Paragraph:
    return p('- ' + s, 'bullet')


def entry(title: str, date: str, details: list[str] | None = None,
          bullets: list[str] | None = None) -> KeepTogether:
    parts = [dated(title, date)]
    parts += [p(s, 'detail') for s in (details or [])]
    parts += [bullet(s) for s in (bullets or [])]
    parts.append(Spacer(1, 2.5))
    return KeepTogether(parts)


def footer(canvas: Canvas, doc: SimpleDocTemplate) -> None:
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(.4)
    canvas.line(MARGIN, 32, PAGE_WIDTH - MARGIN, 32)
    canvas.setFillColor(MUTED)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(MARGIN, 20, f'Weijia Wang | Curriculum vitae | {UPDATED}')
    canvas.drawRightString(PAGE_WIDTH - MARGIN, 20, f'{doc.page} / 2')
    if doc.page > 1:
        canvas.setFont('Times-Bold', 10.5)
        canvas.setFillColor(INK)
        canvas.drawString(MARGIN, PAGE_HEIGHT - 27, 'Weijia Wang')
    canvas.restoreState()


def content() -> list:
    s = [
        p('Weijia (Allen) Wang', 'name'),
        p('M.S. student in Geography (thesis-based) | University of Massachusetts Amherst', 'detail'),
        p(f'<link href="mailto:weijiawang@umass.edu" color="{LINK}">weijiawang@umass.edu</link>'
          f' &nbsp; | &nbsp; <link href="https://wweijia0107.github.io/" color="{LINK}">wweijia0107.github.io</link>', 'contact'),
        p(f'ORCID: <link href="https://orcid.org/0009-0006-1000-9705" color="{LINK}">0009-0006-1000-9705</link>', 'contact'),
        Spacer(1, 3),
    ]

    s += section('Research interests')
    s.append(p('Responsible GeoAI and geoprivacy; location disclosure and contextual integrity; '
               'vision-language models for Earth observation; robustness and generalization '
               'in remote sensing and geospatial AI.'))

    s += section('Education')
    s.append(entry('University of Massachusetts Amherst', 'Aug. 2026-present', [
        'M.S. in Geography (thesis-based) | Amherst, Massachusetts',
        'Advisor: Dr. Hongyu Zhang | Research in ethical GeoAI and place-based location privacy',
    ]))
    s.append(entry('Northern Illinois University', 'Aug. 2024-May 2026', [
        'B.S. in Earth, Atmosphere and Environment - Geospatial Systems | DeKalb, Illinois',
        'GPA 3.897/4.000; Summa Cum Laude; GIS Undergraduate Certificate',
    ]))
    s.append(entry('Lanzhou Jiaotong University', 'Sep. 2022-Jun. 2026', [
        'B.S. in Geographic Information Science | Lanzhou, China | 2+2 dual-degree program',
    ]))

    s += section('Peer-reviewed publication')
    s.append(p('<b>Wang, Weijia</b>, Jichao Fang, and Wei Luo (2026). '
               '"Steering Instruction-Tuned Vision-Language Models for Multi-Label Landcover '
               'Classification." <i>Proceedings of the IEEE/CVF Winter Conference on '
               'Applications of Computer Vision (WACV) Workshops</i>, 1475-1483. '
               f'<link href="https://doi.org/10.1109/WACVW68408.2026.00159" color="{LINK}">'
               'doi:10.1109/WACVW68408.2026.00159</link>. '
               '<i>CV4EO workshop paper (not main conference).</i>'))

    s += section('Conference presentations &amp; accepted abstracts')
    s.append(entry('Does Geographic Context Become a Shortcut? Auditing Functional Place Inference from Earth Observation Imagery with a Vision-Language Model',
                   'Dec. 2026', [
        'AGU Fall Meeting 2026 | San Francisco, CA | Accepted poster, scheduled Dec. 7',
    ]))
    s.append(entry('Privacy in Place: How Place Categories and Information Recipients Shape Location Privacy Concerns',
                   'Feb. 2027', [
        'AAG Annual Meeting 2027 | New York, NY | Accepted paper abstract; assigned to the Environmental Perception session (Behavioral Geography)',
    ]))
    s.append(entry('Parameter-Efficient Fine-Tuning of Vision-Language Models for High-Performance Earth Observation Tasks',
                   'Dec. 2025', [
        'AGU Fall Meeting 2025 | New Orleans, LA | Oral presentation',
    ]))

    s += section('Academic service')
    s.append(entry('Program Committee Member / Reviewer', '2026 review cycle', [
        '4th Computer Vision for Earth Observation (CV4EO) Workshop at WACV 2027',
        'Invited to the program committee; contributed to workshop peer review via OpenReview.',
    ]))

    s.append(PageBreak())

    s += section('Current research')
    s.append(entry('Privacy in Place - place-category privacy concern survey', '2026-present', [
        'M.S. thesis research | University of Massachusetts Amherst | Advisor: Dr. Hongyu Zhang',
    ], [
        'Developing a scenario-based survey on how place types, recipients of location information, '
        'and respondent characteristics shape perceived disclosure concerns.',
        'Grounded in contextual integrity and place-based geoprivacy; study design includes a '
        'Qualtrics survey, an IRB-exempt determination (Aug. 2026), pilot planning, and proposed ordinal mixed-effects analysis.',
    ]))

    s += section('Academic appointments &amp; internships')
    s.append(entry('Teaching Assistant', 'Sep. 2026-present', [
        'University of Massachusetts Amherst | GEOG 100 and GEOG 585',
    ]))
    s.append(entry('Spatial Data Lab Internship Program', 'Sep. 2026-present', [
        'Remote research internship | Mentor: Prof. Yongze Song',
        'Research proposal development in remote sensing, environmental applications, and GeoAI.',
    ]))
    s.append(entry('Henan Remote Sensing Institute', 'Jun.-Jul. 2025', [
        'Satellite Remote Sensing Application Center | Zhengzhou, China',
        'Imagery preprocessing, feature extraction, remote-sensing classification, and ML workflows.',
    ]))
    s.append(entry('Henan Academy of Agricultural Sciences', 'May-Jun. 2025', [
        'Institute of Agricultural Information Technology | Zhengzhou, China',
        'Satellite/UAV imagery and crop-sampling data for winter-wheat yield estimation.',
    ]))

    s += section('Selected research and technical projects')
    s.append(entry('Remote-sensing VLM adaptation', '2025-2026', [
        'Northern Illinois University | Advisor: Prof. Wei Luo',
    ], [
        'Fine-tuned Qwen3-VL with 4-bit LoRA for BigEarthNet-S2 multi-label classification; '
        'evaluated model steering, prompt baselines, and adaptation sparsity.',
    ]))
    s.append(entry('Ground-penetrating radar inversion', '2024-2025', [
        'Kaggle GprMax Deep Learning Challenge 1 (GDLC-1)',
    ], [
        'Developed a TransUNet inversion pipeline for permittivity-map reconstruction; '
        'IoU 0.873 on the hidden test set; <b>1st of 14 finalist teams</b>.',
    ]))
    s.append(entry('Remote-sensing language-model prototype', '2024', [
        'Lanzhou Jiaotong University | Supervisor: Prof. Haowen Yan',
    ], [
        'Adapted VisualGLM-6B with LoRA to answer questions over Sentinel-2 imagery and '
        'Google Earth Engine assets; deployed an interactive Gradio prototype.',
    ]))

    s += section('Honors &amp; awards')
    s.append(bullet('<b>Harvard CGA Workshop Travel Grant</b> (2026), for the National AI Computing '
                    'Research Resources Workshop at the CGA 20th Anniversary Conference.'))
    s.append(bullet("<b>President's Student Service &amp; Leadership Award</b>, Northern Illinois University (2026)."))
    s.append(bullet('<b>Harold A. &amp; Marjorie K. Winters Scholarship</b> (2026); '
                    '<b>Richard E. Dahlberg Memorial Scholarship</b> (2025), Northern Illinois University.'))
    s.append(bullet("<b>Dean's List</b>, Northern Illinois University: Fall 2024, Spring 2025, "
                    'Fall 2025, Spring 2026.'))
    s.append(bullet('<b>1st place</b> (14 finalist teams), Kaggle GDLC-1 Ground-Penetrating Radar '
                    'Inversion Challenge (2025).'))
    s.append(bullet('<b>Second Prize</b>, Gansu Provincial College Student GIS Mapping '
                    'Competition (2024).'))

    s += section('Technical skills')
    s.append(p('<b>Programming / ML:</b> Python, PyTorch, LoRA/QLoRA, Git, R, C++, SPSS.'))
    s.append(p('<b>Geospatial:</b> ArcGIS Pro, QGIS, Google Earth Engine, ENVI, ERDAS, GeoDa.'))
    return s


def build(out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(out), pagesize=letter,
                            leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=41, bottomMargin=43,
                            title='Weijia Wang - Academic Curriculum Vitae',
                            author='Weijia Wang',
                            subject='Geography, geoprivacy, responsible GeoAI and Earth observation',
                            creator='ReportLab / scripts/build_cv.py', invariant=1)
    doc.build(content(), onFirstPage=footer, onLaterPages=footer,
              canvasmaker=partial(Canvas, invariant=1))
    if doc.page != 2:
        raise RuntimeError(f'CV should be exactly 2 pages; generated {doc.page}')
    print(out.resolve())


if __name__ == '__main__':
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument('--output', type=Path,
                      default=Path(__file__).resolve().parents[1] / 'CV-Weijia_Wang.pdf')
    args = argp.parse_args()
    build(args.output)
