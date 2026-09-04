#!/usr/bin/env python3
"""Render a grading feedback report as a PDF.

Usage:
    python3 build_report.py feedback.json -o "Feedback - Paper Title.pdf"
    python3 build_report.py --schema      # print the expected JSON structure

Requires reportlab. If it is unavailable and cannot be installed, fall back to
delivering the same content as Markdown rather than dropping the deliverable.
"""

import argparse
import json
import sys

SCHEMA = r"""
{
  "paper_title": "Northwind Cycles: Entering the Portuguese Market",
  "course": "MGMT 540",
  "assignment": "Group market entry analysis, 15 pages",
  "rubric_used": "Professor rubric (uploaded)",
  "graded_on": "2026-08-31",
  "current_grade":   {"letter": "B",  "score": 84},
  "projected_grade": {"letter": "A-", "score": 91,
                      "condition": "if the three letter-grade findings are fixed"},
  "summary": "Two or three sentences in the professor's voice: what this paper does well, and the one thing keeping it out of the A range.",
  "rubric_scores": [
    {"category": "Problem definition", "weight": 15, "score": 88,
     "comment": "One line on what earned or cost points here."}
  ],
  "findings": [
    {"tier": "letter",
     "location": "Section 4, p. 9",
     "quote": "The Portuguese market presents significant opportunity for expansion.",
     "issue": "The recommendation is asserted rather than sized.",
     "why": "Evidence and quantification (20% of grade)",
     "fix": "Add the addressable market figure from your Exhibit 2 and state the revenue assumption behind it."}
  ],
  "priority_fixes": [
    "Highest-impact fix, stated as an instruction.",
    "Second one.",
    "Third one."
  ],
  "members": [
    {"name": "Dana Ellsworth",
     "sections": ["Risk Mitigation", "Appendix B"],
     "findings": [
       {"tier": "points",
        "location": "Risk Mitigation, p. 11",
        "quote": "Regulatory risk remains a concern.",
        "issue": "Risk named without a mitigation.",
        "why": "Risk and alternatives (10%)",
        "fix": "Pair each risk with a specific response and an owner."}
     ],
     "tasks": [
       {"task": "Add mitigations for the three named risks.", "time": "45 min"}
     ]}
  ],
  "team_items": [
    "Executive summary recommends a joint venture; Section 5 recommends direct entry."
  ]
}

Notes
-----
tier is one of: "letter" (costs a letter grade), "points", "polish".
Every key except paper_title, current_grade and findings is optional.
Omit "members" and "team_items" entirely for a single-author paper.
"""

TIERS = [
    ("letter", "Costing you a letter grade"),
    ("points", "Costing you points"),
    ("polish", "Polish"),
]


def build(data, out_path):
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        HRFlowable, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,
        Spacer, Table, TableStyle,
    )

    ink = colors.HexColor("#1A1A1A")
    muted = colors.HexColor("#6B6B6B")
    rule = colors.HexColor("#D8D4CC")
    accent = colors.HexColor("#2F5D50")

    ss = getSampleStyleSheet()
    S = {
        "title": ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold",
                                fontSize=19, leading=23, textColor=ink, spaceAfter=4),
        "meta": ParagraphStyle("m", parent=ss["Normal"], fontName="Helvetica",
                               fontSize=9, leading=13, textColor=muted),
        "h2": ParagraphStyle("h2", parent=ss["Normal"], fontName="Helvetica-Bold",
                             fontSize=13, leading=16, textColor=ink,
                             spaceBefore=18, spaceAfter=7),
        "tier": ParagraphStyle("tr", parent=ss["Normal"], fontName="Helvetica-Bold",
                               fontSize=11, leading=14, textColor=ink,
                               spaceBefore=13, spaceAfter=4),
        "h3": ParagraphStyle("h3", parent=ss["Normal"], fontName="Helvetica-Bold",
                             fontSize=10.5, leading=14, textColor=accent,
                             spaceBefore=11, spaceAfter=4),
        "body": ParagraphStyle("b", parent=ss["Normal"], fontName="Times-Roman",
                               fontSize=10.5, leading=15, textColor=ink,
                               alignment=TA_LEFT, spaceAfter=6),
        "quote": ParagraphStyle("q", parent=ss["Normal"], fontName="Times-Italic",
                                fontSize=10, leading=14, textColor=muted,
                                leftIndent=14, spaceAfter=5),
        "label": ParagraphStyle("l", parent=ss["Normal"], fontName="Helvetica-Bold",
                                fontSize=9, leading=13, textColor=muted),
        "grade": ParagraphStyle("g", parent=ss["Normal"], fontName="Helvetica-Bold",
                                fontSize=30, leading=32, textColor=ink),
        "gradelab": ParagraphStyle("gl", parent=ss["Normal"], fontName="Helvetica",
                                   fontSize=8.5, leading=12, textColor=muted),
    }

    def P(text, style="body"):
        return Paragraph(str(text), S[style])

    story = []
    story.append(P(data.get("paper_title", "Paper feedback"), "title"))

    meta_bits = [data.get(k) for k in ("course", "assignment", "rubric_used", "graded_on")]
    meta = "<br/>".join(str(b) for b in meta_bits if b)
    if meta:
        story.append(P(meta, "meta"))
    story.append(Spacer(1, 14))

    # Grade block
    cur = data.get("current_grade", {})
    proj = data.get("projected_grade") or {}

    def grade_cell(g, label):
        letter = str(g.get("letter", "\u2014"))
        score = g.get("score")
        sub = f"{score}/100" if score is not None else ""
        inner = [[P(letter, "grade")], [P(label, "gradelab")]]
        if sub:
            inner.append([P(sub, "gradelab")])
        t = Table(inner, colWidths=[2.6 * inch])
        t.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ]))
        return t

    cells = [grade_cell(cur, "Grade as submitted")]
    if proj:
        cells.append(grade_cell(proj, "Projected after fixes"))
    gt = Table([cells], colWidths=[2.9 * inch] * len(cells))
    gt.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(gt)

    if proj.get("condition"):
        story.append(P(proj["condition"], "meta"))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", color=rule, thickness=0.7))

    if data.get("summary"):
        story.append(P("Overall", "h2"))
        story.append(P(data["summary"]))

    # Rubric table
    rows = data.get("rubric_scores") or []
    if rows:
        story.append(P("Score by category", "h2"))
        tdata = [[P("<b>Category</b>", "meta"), P("<b>Weight</b>", "meta"),
                  P("<b>Score</b>", "meta"), P("<b>Note</b>", "meta")]]
        for r in rows:
            w = r.get("weight")
            tdata.append([
                P(r.get("category", ""), "meta"),
                P(f"{w}%" if w is not None else "", "meta"),
                P(r.get("score", ""), "meta"),
                P(r.get("comment", ""), "meta"),
            ])
        t = Table(tdata, colWidths=[1.55 * inch, .6 * inch, .55 * inch, 3.8 * inch],
                  repeatRows=1)
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LINEBELOW", (0, 0), (-1, 0), 0.7, rule),
            ("LINEBELOW", (0, 1), (-1, -2), 0.35, colors.HexColor("#EDEAE4")),
            ("LEFTPADDING", (0, 0), (0, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(t)

    if data.get("priority_fixes"):
        story.append(P("Fix these first", "h2"))
        for i, f in enumerate(data["priority_fixes"], 1):
            story.append(P(f"{i}. {f}"))

    def render_findings(findings, heading_style="tier"):
        known = {k for k, _ in TIERS}
        by_tier = {k: [] for k, _ in TIERS}
        for f in findings:
            tier = f.get("tier", "points")
            # anything unrecognized lands in "points" rather than vanishing
            by_tier[tier if tier in known else "points"].append(f)
        for key, label in TIERS:
            items = by_tier.get(key) or []
            if not items:
                continue
            story.append(P(label, heading_style))
            for f in items:
                block = []
                loc = f.get("location")
                block.append(P(f"{loc} \u2014 {f.get('issue','')}" if loc else f.get("issue", ""),
                               "h3"))
                if f.get("quote"):
                    block.append(P(f"&ldquo;{f['quote']}&rdquo;", "quote"))
                if f.get("why"):
                    block.append(P(f"<b>Costs points under:</b> {f['why']}"))
                if f.get("fix"):
                    block.append(P(f"<b>Fix:</b> {f['fix']}"))
                block.append(Spacer(1, 3))
                story.append(KeepTogether(block))

    if data.get("findings"):
        story.append(P("What needs fixing", "h2"))
        render_findings(data["findings"])

    members = data.get("members") or []
    if members:
        story.append(PageBreak())
        story.append(P("Individual assignments", "title"))
        story.append(P("Each person's items, based on the sections they wrote.", "meta"))
        for m in members:
            story.append(Spacer(1, 10))
            story.append(HRFlowable(width="100%", color=rule, thickness=0.7))
            story.append(P(m.get("name", "Unassigned"), "h2"))
            if m.get("sections"):
                story.append(P("Sections: " + ", ".join(m["sections"]), "meta"))
                story.append(Spacer(1, 4))
            if m.get("findings"):
                render_findings(m["findings"], heading_style="h3")
            if m.get("tasks"):
                story.append(P("Task list", "h3"))
                for t in m["tasks"]:
                    if isinstance(t, dict):
                        est = f"  <font color='#6B6B6B'>({t['time']})</font>" if t.get("time") else ""
                        story.append(P(f"<font name='Courier'>[ ]</font>&nbsp; {t.get('task','')}{est}"))
                    else:
                        story.append(P(f"<font name='Courier'>[ ]</font>&nbsp; {t}"))

    if data.get("team_items"):
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", color=rule, thickness=0.7))
        story.append(P("Whole-team items", "h2"))
        story.append(P("Nobody owns these individually, which is why they get missed.", "meta"))
        story.append(Spacer(1, 4))
        for item in data["team_items"]:
            story.append(P(f"<font name='Courier'>[ ]</font>&nbsp; {item}"))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(muted)
        canvas.drawString(0.9 * inch, 0.55 * inch,
                          "Predicted feedback, not an official grade.")
        canvas.drawRightString(LETTER[0] - 0.9 * inch, 0.55 * inch, str(doc.page))
        canvas.restoreState()

    doc = SimpleDocTemplate(
        out_path, pagesize=LETTER,
        leftMargin=0.9 * inch, rightMargin=0.9 * inch,
        topMargin=0.85 * inch, bottomMargin=0.85 * inch,
        title=data.get("paper_title", "Paper feedback"), author="paper-grader",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return out_path


def main():
    ap = argparse.ArgumentParser(description="Render a grading feedback PDF.")
    ap.add_argument("json_file", nargs="?", help="path to the feedback JSON")
    ap.add_argument("-o", "--out", default="feedback-report.pdf", help="output PDF path")
    ap.add_argument("--schema", action="store_true", help="print the expected JSON structure")
    args = ap.parse_args()

    if args.schema:
        print(SCHEMA)
        return
    if not args.json_file:
        ap.error("give a JSON file, or pass --schema")

    try:
        with open(args.json_file, encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        sys.exit(f"No such file: {args.json_file}")
    except json.JSONDecodeError as err:
        sys.exit(f"{args.json_file} is not valid JSON (line {err.lineno}, "
                 f"column {err.colno}): {err.msg}")

    if not isinstance(data, dict):
        sys.exit("The feedback file must contain a JSON object. Run --schema to see the structure.")
    missing = [k for k in ("paper_title", "current_grade") if k not in data]
    if missing:
        sys.exit("Missing required field(s): " + ", ".join(missing) +
                 ". Run --schema to see the structure.")

    try:
        path = build(data, args.out)
    except ImportError:
        sys.exit("reportlab is not installed. Run: pip install reportlab "
                 "(or deliver the report as Markdown instead).")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
