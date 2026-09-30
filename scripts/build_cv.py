"""Build Weijia Wang's public, two-page academic CV.

Requirements: Python 3.10+ and reportlab.
Run from any directory: python scripts/build_cv.py
The output defaults to ../CV-Weijia_Wang.pdf relative to this script.
Use --output PATH to create a review copy. Facts are current as of 2026-09-30.

The source intentionally excludes private residential contact information and
avoids numerical VLM results that differ between earlier and published runs.
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
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN = 45
CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN
INK = colors.HexColor("#20262D")
MUTED = colors.HexColor("#56616B")
RULE = colors.HexColor("#9CA5AC")
LINK = "#294C67"
UPDATED = "September 2026"

STYLES = {
    "name": ParagraphStyle(
        "Name", fontName="Times-Bold", fontSize=26, leading=29,
        textColor=INK, spaceAfter=3,
    ),
    "body": ParagraphStyle(
        "Body", fontName="Helvetica", fontSize=10.3, leading=13.3,
        textColor=INK, spaceAfter=3,
    ),
    "detail": ParagraphStyle(
        "Detail", fontName="Helvetica", fontSize=10.0, leading=12.8,
        textColor=MUTED, spaceAfter=3,
    ),
    "date": ParagraphStyle(
        "Date", fontName="Helvetica", fontSize=9.7, leading=13.3,
        textColor=MUTED, alignment=TA_RIGHT,
    ),
    "section": ParagraphStyle(
        "Section", fontName="Times-Bold", fontSize=13.6, leading=16,
        textColor=INK, spaceBefore=10, spaceAfter=3, keepWithNext=True,
    ),
    "bullet": ParagraphStyle(
        "Bullet", fontName="Helvetica", fontSize=10.3, leading=13.3,
        textColor=INK, leftIndent=10, firstLineIndent=-8, spaceAfter=3,
    ),
    "contact": ParagraphStyle(
        "Contact", fontName="Helvetica", fontSize=9.8, leading=13,
        textColor=MUTED, spaceAfter=2,
    ),
}


def para(text: str, style: str = "body") -> Paragraph:
    return Paragraph(text, STYLES[style])


def section(title: str) -> list:
    rule = HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=6)
    rule.keepWithNext = True
    return [
        para(title, "section"),
        rule,
    ]


def dated_title(title: str, date: str) -> Table:
    table = Table(
        [[para(f"<b>{title}</b>"), para(date, "date")]],
        colWidths=[CONTENT_WIDTH - 135, 135],
        hAlign="LEFT",
    )
    table.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return table


def bullet(text: str) -> Paragraph:
    return para(f"- {text}", "bullet")


def entry(title: str, date: str, lines: list[str], bullets: list[str] | None = None) -> KeepTogether:
    parts = [dated_title(title, date)]
    parts.extend(para(line, "detail") for line in lines)
    parts.extend(bullet(line) for line in (bullets or []))
    parts.append(Spacer(1, 3))
    return KeepTogether(parts)


def footer(canvas: Canvas, doc: SimpleDocTemplate) -> None:
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.4)
    canvas.line(MARGIN, 35, PAGE_WIDTH - MARGIN, 35)
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN, 23, f"Weijia Wang | Curriculum vitae | {UPDATED}")
    canvas.drawRightString(PAGE_WIDTH - MARGIN, 23, f"{doc.page} / 2")
    if doc.page > 1:
        canvas.setFont("Times-Bold", 12)
        canvas.setFillColor(INK)
        canvas.drawString(MARGIN, PAGE_HEIGHT - 30, "Weijia Wang")
        canvas.setFont("Helvetica", 8.8)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 30, "Curriculum vitae")
    canvas.restoreState()


def content() -> list:
    story = [
        para("Weijia (Allen) Wang", "name"),
        para("M.S. student in Geography | University of Massachusetts Amherst", "detail"),
        para(
            f'<link href="mailto:weijiawang@umass.edu" color="{LINK}">weijiawang@umass.edu</link>'
            f' &nbsp; | &nbsp; <link href="https://wweijia0107.github.io/" color="{LINK}">wweijia0107.github.io</link>',
            "contact",
        ),
        para(
            f'ORCID: <link href="https://orcid.org/0009-0006-1000-9705" color="{LINK}">0009-0006-1000-9705</link>',
            "contact",
        ),
        Spacer(1, 5),
    ]
    story += section("Research interests")
    story.append(para(
        "Ethical and responsible GeoAI; location privacy, geoprivacy, and place-based privacy; "
        "vision-language models for Earth observation; spatial modeling and geospatial analysis."
    ))

    story += section("Education")
    story.append(entry(
        "University of Massachusetts Amherst", "Aug. 2026-present", [
            "M.S. in Geography (thesis-based) | Amherst, Massachusetts",
            "Department of Earth, Geographic, and Climate Sciences",
            "Research with Dr. Hongyu Zhang | Focus: ethical GeoAI and location / place-based privacy",
        ],
    ))
    story.append(entry(
        "Northern Illinois University", "Aug. 2024-May 2026", [
            "B.S. in Earth, Atmosphere and Environment - Geospatial Systems | DeKalb, Illinois",
            "GPA: 3.897/4.000; Summa Cum Laude",
            "2+2 dual-degree program with Lanzhou Jiaotong University",
        ],
    ))
    story.append(entry(
        "Lanzhou Jiaotong University", "Sep. 2022-Jun. 2026", [
            "B.S. in Geographic Information Science | Lanzhou, China",
        ],
    ))

    story += section("Academic appointments &amp; current internship")
    story.append(entry(
        "Teaching Assistant", "Sep. 6, 2026-present", [
            "University of Massachusetts Amherst",
            "Department of Earth, Geographic, and Climate Sciences",
        ],
    ))
    story.append(entry(
        "Intern, Spatial Data Lab Internship Program", "Sep. 2026-present", [
            "Remote | Guidance: Yongze Song",
        ], [
            "Currently developing a research proposal in GeoAI, Earth observation, spatial modeling, "
            "and geospatial analysis.",
        ],
    ))

    story += section("Publication &amp; presentation")
    story.append(para(
        '<b>Wang, Weijia</b>; Fang, Jichao; Luo, Wei. "Steering Instruction-Tuned Vision-Language Models '
        'for Multi-Label Landcover Classification." <i>Proceedings of the IEEE/CVF Winter Conference '
        'on Applications of Computer Vision (WACV) Workshops</i>, March 2026, pp. 1475-1483. '
        'CV4EO Workshop. Peer-reviewed archival proceedings.'
    ))
    story.append(Spacer(1, 3))
    story.append(para(
        '<b>Wang, Weijia</b>; Fang, Jichao; Luo, Wei. "Parameter-Efficient Fine-Tuning of Vision-Language '
        'Models for High-Performance Earth Observation Tasks." <i>AGU Fall Meeting 2025</i>, '
        'New Orleans, Louisiana. <b>Oral presentation.</b>'
    ))

    story += section("Academic service")
    story.append(entry(
        "Program Committee Member / Reviewer", "Sep. 2026-present", [
            "4th Computer Vision for Earth Observation (CV4EO) Workshop at WACV 2027",
        ],
    ))

    story.append(PageBreak())
    story += section("Research experience &amp; projects")
    story.append(entry(
        "Undergraduate Student Researcher", "Aug. 2025-May 2026", [
            "Northern Illinois University | Supervisor: Prof. Wei Luo | DeKalb, Illinois",
            "Project: instruction-tuned vision-language models for Earth observation (Apr. 2025-May 2026)",
        ], [
            "Developed parameter-efficient supervised fine-tuning and model-steering workflows for "
            "multi-label land-cover classification using Qwen3-VL, 4-bit LoRA, and BigEarthNet-S2 imagery.",
            "Compared prompt engineering, chain-of-thought zero-shot, and fine-tuning baselines; "
            "analyzed inference-time precision-recall trade-offs, adaptation patterns, and LoRA sparsity.",
        ],
    ))
    story.append(entry(
        "Ground-penetrating radar inversion", "Oct. 2024-May 2025", [
            "Kaggle GprMax Deep Learning Challenge 1 (GDLC-1) | Remote",
        ], [
            "Designed a TransUNet framework with a CNN encoder, Vision Transformer, and skip-connected "
            "decoder to reconstruct 2-D subsurface permittivity maps from GPR B-scans.",
            "Used gprMax FDTD simulations for data augmentation and a physics-aware loss combining "
            "MAE, SSIM, FFT, and gradient regularization in PyTorch.",
            "Achieved IoU of 0.873 on the hidden test set; ranked 1st among 14 finalist teams.",
        ],
    ))
    story.append(entry(
        "Remote-sensing LLM prototype", "Jan. 2024-Dec. 2024", [
            "College Students' Innovative Entrepreneurial Training Plan Program | Lanzhou, China",
            "Lanzhou Jiaotong University | Supervisor: Prof. Haowen Yan",
        ], [
            "Adapted VisualGLM-6B with LoRA for natural-language queries about Sentinel-2 imagery and "
            "Google Earth Engine assets; supported GeoJSON-based areas of interest and RGB+NIR previews.",
            "Deployed an interactive prototype with NVIDIA Triton Inference Server and Gradio; "
            "evaluated failure modes including spectral aliasing and ambiguous prompts.",
        ],
    ))

    story += section("Previous internships")
    story.append(entry(
        "Henan Remote Sensing Institute", "Jun. 2025-Jul. 2025", [
            "Intern, Satellite Remote Sensing Application Center | Zhengzhou, China",
        ], [
            "Preprocessed remote-sensing imagery, extracted features, and performed classification; "
            "explored machine learning to improve repetitive analysis workflows.",
        ],
    ))
    story.append(entry(
        "Henan Academy of Agricultural Sciences", "May 2025-Jun. 2025", [
            "Intern, Institute of Agricultural Information Technology | Zhengzhou, China",
        ], [
            "Collected and analyzed satellite, UAV, and crop-sampling data for winter-wheat yield "
            "estimation; labeled training samples and explored machine learning for data processing.",
        ],
    ))

    story += section("Honors &amp; awards")
    story.append(bullet(
        "NIU: President's Student Service &amp; Leadership Award (2026); Harold A. &amp; Marjorie K. "
        "Winters Scholarship (2026); Richard E. Dahlberg Memorial Scholarship, top 2% (2025)."
    ))
    story.append(bullet("NIU Dean's List: Fall 2024, Spring 2025, Fall 2025, Spring 2026."))
    story.append(bullet(
        "Second Prize, 2023 Gansu Province College Student GIS Map Making Application Skills "
        "Competition; top 10%, provincial level (2024)."
    ))

    story += section("Technical skills")
    story.append(para(
        "<b>Programming &amp; machine learning:</b> Python, PyTorch, LoRA/QLoRA fine-tuning, Git, C++, SPSS."
    ))
    story.append(para(
        "<b>Geospatial:</b> ArcGIS Pro, ERDAS, ENVI, QGIS, Google Earth Engine, GeoDa."
    ))
    return story


def build(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output), pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=43, bottomMargin=47,
        title="Weijia Wang - Academic Curriculum Vitae",
        author="Weijia Wang",
        subject="Geography, responsible GeoAI, geoprivacy, and Earth observation",
        creator="ReportLab; scripts/build_cv.py",
        invariant=1,
    )
    doc.build(
        content(), onFirstPage=footer, onLaterPages=footer,
        canvasmaker=partial(Canvas, invariant=1),
    )
    if doc.page != 2:
        raise RuntimeError(f"Expected exactly 2 CV pages; produced {doc.page}.")
    print(output.resolve())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).resolve().parents[1] / "CV-Weijia_Wang.pdf",
    )
    build(parser.parse_args().output)
