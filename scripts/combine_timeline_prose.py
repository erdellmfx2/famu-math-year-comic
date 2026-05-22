#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer


REPO = "erdellmfx2/famu-math-year-comic"
FOLDER = "story/timeline-weeks-prose"
EXPECTED_WEEKS = list(range(1, 55))


@dataclass
class ProseFile:
    week: int
    name: str
    content: str


def run_gh_api(path: str) -> object:
    result = subprocess.run(
        ["gh", "api", path],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def parse_week(name: str) -> int | None:
    match = re.fullmatch(r"prose_(\d+)\.md", name)
    return int(match.group(1)) if match else None


def fetch_file_list() -> list[tuple[int, str]]:
    payload = run_gh_api(f"repos/{REPO}/contents/{FOLDER}")
    files: list[tuple[int, str]] = []
    for item in payload:
        if item.get("type") != "file":
            continue
        name = item["name"]
        week = parse_week(name)
        if week is not None:
            files.append((week, name))
    files.sort(key=lambda item: item[0])
    return files


def fetch_file_content(name: str) -> str:
    payload = run_gh_api(f"repos/{REPO}/contents/{FOLDER}/{name}")
    encoded = payload["content"].replace("\n", "")
    return base64.b64decode(encoded).decode("utf-8")


def load_local_overrides(override_dir: Path) -> dict[int, ProseFile]:
    overrides: dict[int, ProseFile] = {}
    if not override_dir.exists():
        return overrides
    for path in sorted(override_dir.glob("prose_*.md")):
        week = parse_week(path.name)
        if week is None:
            continue
        overrides[week] = ProseFile(
            week=week,
            name=path.name,
            content=path.read_text(encoding="utf-8"),
        )
    return overrides


def set_run_font(run, size: float, bold: bool = False, color: RGBColor | None = None) -> None:
    run.font.name = "Arial"
    run._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    run._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    run.font.size = Pt(size)
    run.bold = bold
    if color is not None:
        run.font.color.rgb = color


def configure_document(doc: Document) -> None:
    section = doc.sections[0]
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.header_distance = Inches(0.492)
    section.footer_distance = Inches(0.492)

    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    normal.font.size = Pt(11)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(8)
    normal.paragraph_format.line_spacing = 1.15

    for style_name, size, color in [
        ("Heading 1", 20, RGBColor(0, 0, 0)),
        ("Heading 2", 16, RGBColor(0, 0, 0)),
        ("Heading 3", 14, RGBColor(67, 67, 67)),
    ]:
        style = doc.styles[style_name]
        style.font.name = "Arial"
        style._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
        style._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
        style.font.size = Pt(size)
        style.font.bold = False
        style.font.color.rgb = color


def add_title_page(doc: Document, missing_weeks: list[int]) -> None:
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    title.paragraph_format.space_before = Pt(0)
    title.paragraph_format.space_after = Pt(3)
    run = title.add_run("FAMU Math Year Comic Timeline Prose")
    set_run_font(run, 26, bold=False, color=RGBColor(0, 0, 0))

    subtitle = doc.add_paragraph()
    subtitle.paragraph_format.space_before = Pt(0)
    subtitle.paragraph_format.space_after = Pt(8)
    subtitle_run = subtitle.add_run("Combined manuscript from story/timeline-weeks-prose")
    set_run_font(subtitle_run, 11, color=RGBColor(85, 85, 85))

    if missing_weeks:
        note = doc.add_paragraph()
        note.paragraph_format.space_before = Pt(0)
        note.paragraph_format.space_after = Pt(8)
        note_run = note.add_run(
            "Source note: GitHub did not currently include "
            + ", ".join(f"prose_{week}.md" for week in missing_weeks)
            + "."
        )
        set_run_font(note_run, 11, color=RGBColor(85, 85, 85))


def add_markdown_paragraph(doc: Document, text: str, style: str | None = None) -> None:
    paragraph = doc.add_paragraph(style=style)
    paragraph.paragraph_format.line_spacing = 1.15
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(8 if style is None else 6)

    pieces = re.split(r"(\*\*.*?\*\*)", text)
    for piece in pieces:
        if not piece:
            continue
        if piece.startswith("**") and piece.endswith("**") and len(piece) >= 4:
            run = paragraph.add_run(piece[2:-2])
            set_run_font(run, 11 if style is None else {"Heading 1": 20, "Heading 2": 16, "Heading 3": 14}[style], bold=True)
        else:
            run = paragraph.add_run(piece)
            set_run_font(run, 11 if style is None else {"Heading 1": 20, "Heading 2": 16, "Heading 3": 14}[style], bold=False)


def render_markdown_block(doc: Document, block: str) -> None:
    stripped = block.strip()
    if not stripped:
        return
    if stripped.startswith("### "):
        add_markdown_paragraph(doc, stripped[4:].strip(), style="Heading 3")
    elif stripped.startswith("## "):
        add_markdown_paragraph(doc, stripped[3:].strip(), style="Heading 2")
    elif stripped.startswith("# "):
        add_markdown_paragraph(doc, stripped[2:].strip(), style="Heading 1")
    else:
        for line in stripped.splitlines():
            if re.match(r"^\d+\.\s+", line):
                paragraph = doc.add_paragraph(style="Normal")
                paragraph.style = doc.styles["Normal"]
                paragraph.paragraph_format.left_indent = Inches(0.5)
                paragraph.paragraph_format.first_line_indent = Inches(-0.25)
                paragraph.paragraph_format.space_after = Pt(4)
                run = paragraph.add_run(line)
                set_run_font(run, 11)
            elif line.startswith(("- ", "* ")):
                paragraph = doc.add_paragraph(style="Normal")
                paragraph.paragraph_format.left_indent = Inches(0.5)
                paragraph.paragraph_format.first_line_indent = Inches(-0.25)
                paragraph.paragraph_format.space_after = Pt(4)
                run = paragraph.add_run("• " + line[2:].strip())
                set_run_font(run, 11)
            else:
                add_markdown_paragraph(doc, line)


def add_week_content(doc: Document, prose: ProseFile, is_first_week: bool) -> None:
    if not is_first_week:
        doc.add_page_break()
    blocks = re.split(r"\n\s*\n", prose.content.strip())
    for block in blocks:
        render_markdown_block(doc, block)


def write_combined_markdown(files: list[ProseFile], destination: Path, missing_weeks: list[int]) -> None:
    parts = [
        "# FAMU Math Year Comic Timeline Prose",
        "",
        "Combined from `story/timeline-weeks-prose`.",
        "",
    ]
    if missing_weeks:
        parts.extend(
            [
                "## Source Note",
                "",
                "The following expected weekly files were not present in GitHub at export time: "
                + ", ".join(f"`prose_{week}.md`" for week in missing_weeks)
                + ".",
                "",
            ]
        )

    for prose in files:
        parts.append(prose.content.strip())
        parts.append("")
        parts.append("---")
        parts.append("")

    destination.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")


def write_docx(files: list[ProseFile], destination: Path, missing_weeks: list[int]) -> None:
    doc = Document()
    configure_document(doc)
    add_title_page(doc, missing_weeks)

    for index, prose in enumerate(files):
        add_week_content(doc, prose, is_first_week=index == 0)

    doc.save(destination)


def build_pdf_styles():
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TimelineTitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=26,
            leading=30,
            spaceAfter=6,
            textColor=HexColor("#000000"),
            alignment=TA_LEFT,
        ),
        "meta": ParagraphStyle(
            "TimelineMeta",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=14,
            spaceAfter=8,
            textColor=HexColor("#555555"),
        ),
        "body": ParagraphStyle(
            "TimelineBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "TimelineH1",
            parent=styles["Heading1"],
            fontName="Helvetica",
            fontSize=20,
            leading=24,
            spaceBefore=20,
            spaceAfter=6,
            textColor=HexColor("#000000"),
        ),
        "h2": ParagraphStyle(
            "TimelineH2",
            parent=styles["Heading2"],
            fontName="Helvetica",
            fontSize=16,
            leading=20,
            spaceBefore=18,
            spaceAfter=6,
            textColor=HexColor("#000000"),
        ),
        "h3": ParagraphStyle(
            "TimelineH3",
            parent=styles["Heading3"],
            fontName="Helvetica",
            fontSize=14,
            leading=18,
            spaceBefore=16,
            spaceAfter=4,
            textColor=HexColor("#434343"),
        ),
        "bullet": ParagraphStyle(
            "TimelineBullet",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            leftIndent=0.5 * inch,
            firstLineIndent=-0.2 * inch,
            spaceAfter=4,
        ),
    }


def markup_to_reportlab(text: str) -> str:
    escaped = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)


def pdf_block_to_flowables(block: str, styles: dict[str, ParagraphStyle]):
    stripped = block.strip()
    if not stripped:
        return []
    if stripped.startswith("### "):
        return [Paragraph(markup_to_reportlab(stripped[4:].strip()), styles["h3"])]
    if stripped.startswith("## "):
        return [Paragraph(markup_to_reportlab(stripped[3:].strip()), styles["h2"])]
    if stripped.startswith("# "):
        return [Paragraph(markup_to_reportlab(stripped[2:].strip()), styles["h1"])]

    flowables = []
    for line in stripped.splitlines():
        if re.match(r"^\d+\.\s+", line):
            flowables.append(Paragraph(markup_to_reportlab(line), styles["bullet"]))
        elif line.startswith(("- ", "* ")):
            flowables.append(Paragraph(markup_to_reportlab("• " + line[2:].strip()), styles["bullet"]))
        else:
            flowables.append(Paragraph(markup_to_reportlab(line), styles["body"]))
    return flowables


def write_pdf(files: list[ProseFile], destination: Path, missing_weeks: list[int]) -> None:
    styles = build_pdf_styles()
    doc = SimpleDocTemplate(
        str(destination),
        pagesize=letter,
        topMargin=1.0 * inch,
        bottomMargin=1.0 * inch,
        leftMargin=1.0 * inch,
        rightMargin=1.0 * inch,
    )
    flowables = [
        Paragraph("FAMU Math Year Comic Timeline Prose", styles["title"]),
        Paragraph("Combined manuscript from story/timeline-weeks-prose", styles["meta"]),
    ]
    if missing_weeks:
        flowables.append(
            Paragraph(
                "Source note: GitHub did not currently include "
                + ", ".join(f"prose_{week}.md" for week in missing_weeks)
                + ".",
                styles["meta"],
            )
        )
    flowables.append(Spacer(1, 0.15 * inch))

    for index, prose in enumerate(files):
        if index > 0:
            flowables.append(PageBreak())
        blocks = re.split(r"\n\s*\n", prose.content.strip())
        for block in blocks:
            flowables.extend(pdf_block_to_flowables(block, styles))

    doc.build(flowables)


def save_source_files(files: list[ProseFile], destination_dir: Path) -> None:
    destination_dir.mkdir(parents=True, exist_ok=True)
    for prose in files:
        (destination_dir / prose.name).write_text(prose.content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="timeline-weeks-prose-output")
    parser.add_argument("--override-dir", default="famu-math-year-comic/story/timeline-weeks-prose")
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    source_dir = output_dir / "source-files"
    override_dir = Path(args.override_dir).resolve()

    file_entries = fetch_file_list()
    files_by_week = {
        week: ProseFile(week=week, name=name, content=fetch_file_content(name))
        for week, name in file_entries
    }
    files_by_week.update(load_local_overrides(override_dir))
    files = [files_by_week[week] for week in sorted(files_by_week)]
    missing_weeks = [week for week in EXPECTED_WEEKS if week not in {item.week for item in files}]

    save_source_files(files, source_dir)
    write_combined_markdown(files, output_dir / "timeline-weeks-prose-complete.md", missing_weeks)
    write_docx(files, output_dir / "timeline-weeks-prose-complete.docx", missing_weeks)
    write_pdf(files, output_dir / "timeline-weeks-prose-complete.pdf", missing_weeks)

    summary = {
        "file_count": len(files),
        "missing_weeks": missing_weeks,
        "output_dir": str(output_dir),
    }
    (output_dir / "export-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
