# paper-grader

An Agent Skill that grades an academic paper the way a professor **in that specific
field** will. It reads the paper, works out which of 50 academic disciplines it
belongs to, applies that field's standards, and hands back a PDF: a current grade, a
projected grade if the fixes are made, findings tied to specific passages, and, for
group projects, a per-person task list.

Works in Claude and ChatGPT. Both read the same `SKILL.md` format.

## Watch the walkthrough

[![Watch the paper-grader walkthrough on YouTube](https://img.youtube.com/vi/DlYI6o8cnS8/maxresdefault.jpg)](https://youtu.be/DlYI6o8cnS8 "paper-grader: 40-second walkthrough")

**▶ [paper-grader in 40 seconds](https://youtu.be/DlYI6o8cnS8)** covers the whole loop:
point it at a draft, run one command, read the report. No voiceover, no setup footage.

## What it does

Upload a draft. The skill reads it end to end, grades it against the professor's
rubric if you have one (or a built-in rubric if you don't), and reports back:

- **A grade as submitted**, scored by category with weights.
- **A projected grade** after the listed fixes, with the arithmetic shown. It won't
  promise an A the paper can't reach.
- **Findings in three tiers** — costing you a letter grade, costing you points, and
  polish. Each one quotes the passage it's flagging and gives a specific instruction,
  not "strengthen your analysis."
- **Per-person breakdowns** for group papers, plus the whole-team items that get
  missed because each author only reads their own section.

## Why the discipline matters

A philosophy paper and a chemical engineering report fail in completely different
ways. Generic feedback flatters both.

The skill classifies the paper first, from the course code, the assignment prompt, the
method it uses, and the sources it cites. Then it grades by that field's standards.
An economics paper gets marked on identification strategy. A history paper gets marked
on whether it argues from primary sources or narrates from secondary ones. A machine
learning paper gets checked for train/test leakage. A law paper gets marked down for
ignoring adverse authority.

Fifty subjects across five faculty areas, following the QS subject taxonomy:

| Area | Subjects |
|---|---|
| Arts & Humanities | Architecture · Art and Design · Archaeology · Classics · English · History · Linguistics · Modern Languages · Performing Arts · Philosophy · Theology |
| Engineering & Technology | Chemical · Civil and Structural · Computer Science · Data Science and AI · Electrical · Mechanical and Aerospace · Mineral and Mining · Petroleum |
| Life Sciences & Medicine | Agriculture and Forestry · Anatomy and Physiology · Biological Sciences · Dentistry · Medicine · Nursing · Pharmacy · Psychology · Veterinary |
| Natural Sciences | Chemistry · Earth and Marine · Environmental · Geography · Geology · Geophysics · Materials · Mathematics · Physics and Astronomy |
| Social Sciences & Management | Accounting and Finance · Anthropology · Business and Management · Communication and Media · Economics · Education · Hospitality and Leisure · Law · Marketing · Politics · Social Policy · Sociology · Statistics and OR |

It states its classification at the top of the report so you can correct it, and it
grades interdisciplinary papers against the primary field while checking the borrowed
method for competence.

The professor is a set of standards, not a character. No invented names, no persona
voice. The only thing you should notice is that the feedback knows your subject.

It evaluates and gives repair instructions. It does not write the paper.

## Install

**Claude:** zip the `paper-grader/` folder so the folder itself sits at the root of
the zip, then upload it in Settings under Skills. Requires a Pro, Max, Team, or
Enterprise plan with code execution enabled (the PDF step needs it). A ready-made
`paper-grader.zip` is in the releases if you'd rather not zip it yourself.

```bash
zip -r paper-grader.zip paper-grader/
```

**Claude Code:** drop the folder in `~/.claude/skills/` for every project, or
`.claude/skills/` for one repo.

**ChatGPT:** Sidebar → Plugins → Skills tab → upload. Personal Skills are documented
as available on Business, Enterprise, Healthcare, and Edu accounts, not Free or Plus.

Skills don't sync between surfaces. Upload separately wherever you want it.

## Use

Start a chat, attach the paper, and say what you want:

```
Grade this before I submit it. Rubric is attached too.
```

```
Group project, due Thursday. I wrote the risk section, my two teammates did
financials and market analysis. What does each of us need to fix?
```

The skill asks for the assignment prompt if you didn't attach one, since the professor's own rubric
beats a generic standard every time. You can also name the field directly if you want
to override its guess: *"grade this as a sociology paper, not a stats paper."*

## Layout

```
.
├── README.md
├── ABOUT.md                        repo description, topics, social preview
├── LICENSE
├── .gitignore
├── example-report.pdf              a rendered sample, fictional paper
├── social-preview.jpg              1280x640 card for GitHub's Settings panel
├── demo/                           the demo video and its source
└── paper-grader/                   ← the skill itself; this is what you zip
```

Inside the skill:

```
paper-grader/
├── SKILL.md                        the grading process
├── professors/
│   ├── index.md                    classification rules and the subject list
│   ├── arts-humanities.md          11 subjects
│   ├── engineering-technology.md   8 subjects
│   ├── life-sciences-medicine.md   9 subjects
│   ├── natural-sciences.md         9 subjects
│   └── social-sciences-management.md  13 subjects
├── rubrics/
│   ├── default-academic.md         research papers and essays
│   ├── mba-case-analysis.md        case studies and strategy memos
│   └── apa-formatting.md           citation and formatting pass
├── references/
│   └── grade-bands.md              score-to-letter, and what each level expects
└── scripts/
    └── build_report.py             renders the feedback PDF
```

## Customizing it

The rubrics are plain Markdown tables. Edit the weights to match your program, or
drop in a rubric file per course. The discipline files are plain Markdown too: if your
field's standards differ from what's written there, edit the subject block, and to add
a subject, add a block plus a line in `professors/index.md`. If a professor hands out a rubric you'll reuse all
semester, save it in `rubrics/` and name it in `SKILL.md` so it gets picked
automatically.

To see the JSON the report builder expects:

```bash
python3 paper-grader/scripts/build_report.py --schema
```

## A note on academic integrity

This is a feedback tool for work you already wrote, in the same category as a writing
center appointment or a peer review. It's built to refuse to draft submittable
content. Check your institution's policy on AI assistance before using it, and
disclose it where your program requires disclosure.

## License

MIT
