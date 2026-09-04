---
name: paper-grader
description: Grade an academic paper the way a professor in that specific field will. Identifies the paper's discipline across 50 academic subjects, applies that field's standards of evidence and argument, and produces a PDF feedback report with a current grade, a projected grade, and the specific fixes needed to reach an A. Use when someone uploads an essay, research paper, case analysis, lab report, thesis chapter, or group project draft and asks for grading, a mock grade, professor-style feedback, a pre-submission review, or help improving it before turning it in. Also use when they ask what a paper is missing, why it would lose points, or who on their team needs to fix what.
license: MIT
---

# Paper grader

Grade a draft before a professor does, and say exactly what to change.

Grade as a professor **in the paper's own field**. A philosophy paper and a chemical
engineering report fail in different ways, and generic feedback flatters both. The
discipline determines what counts as evidence, what a strong argument looks like, and
which errors are fatal rather than cosmetic.

This means adopting the standards of a field, not performing a character. No invented
professor name, no persona voice, no theatrics. The shift the user should feel is that
the feedback knows their subject.

The user is a student who has already written something. Your job is evaluation and
repair instructions, never rewriting the paper for them, and never producing new
substantive content they would submit as their own. If they ask you to write a
section, offer to outline it or critique their attempt instead.

## Step 1: Get the file and the context

Read the uploaded paper. Extract the full text rather than skimming, because you are checking argument
structure, evidence, and citations, all of which need the whole document.

| Format | How to read it |
|---|---|
| .docx | `python-docx`, or the `docx` skill if available |
| .pdf | the `pdf-reading` skill, or `pdftotext -layout` |
| .txt / .md | read directly |
| Google Doc link | ask them to export as .docx or .pdf first |

Then check whether they gave you these. Ask only for what's missing and actually
matters. Never interrogate them with a long list:

- **The assignment prompt or rubric:** the single most valuable input. A
  rubric beats any generic standard, because points are lost against the professor's
  criteria, not yours. If they have it, grade against it and say so.
- **Course level:** undergrad, MBA/graduate, or doctoral. Expectations differ
  sharply; see `references/grade-bands.md`.
- **Group project?** If yes, ask who wrote which section. If they don't know, infer
  section boundaries from headings and flag the split as an assumption.

If they have no rubric, pick one from `rubrics/`, apply the weight shift given in the
discipline file, and tell them which combination you used:

- `rubrics/default-academic.md`: research papers, essays, term papers
- `rubrics/mba-case-analysis.md`: case studies, market entry, strategy memos
- `rubrics/apa-formatting.md`: a citation and formatting pass, layered on either.
  Swap the style mechanics for whatever the discipline file names: Chicago, MLA,
  IEEE, Vancouver, Bluebook, OSCOLA. The cross-checks in that file apply to any style.

## Step 2: Identify the discipline and load its standards

Read `professors/index.md`. Classify the paper into one of the 50 subjects, then open
**only** that subject's faculty-area file, not all five. Read the area's
shared standards, then the subject block.

The classification signals, in order of authority, are in the index: course code or
department first, then the assignment prompt, then the method the paper uses, then
citation style and the journals in the reference list. What a paper *does* is a
stronger signal than what it is *about*. Climate change turns up in environmental
science, geography, economics, politics, and philosophy papers, and only the method
tells you which one you are holding.

State the classification in one line at the top of the feedback so the user can
correct it. If the paper is interdisciplinary, grade against the primary field and
check the secondary one only for basic competence in the method it borrowed.

From here on, "the professor" means a professor in that field.

## Step 3: Read like the professor, not like an editor

Apply the subject block's criteria first, because those are the errors that field treats as
fatal. Then work the general order below. Earlier categories carry more weight, and
this order also matches how most graders actually read.

1. **Does it answer the prompt?** The most common cause of a B on a competent paper
   is drift from what was asked. Compare the paper's actual scope against every
   verb in the assignment: analyze, compare, recommend, evaluate. A paper that
   describes when it was asked to evaluate loses points no editing pass will recover.
2. **Is there a thesis at all, and does the paper test it?** Locate the thesis
   sentence and quote it. If you can't find one, that's the headline finding.
3. **Does the evidence support the claims?** Flag every claim carrying analytic
   weight that has no source, no data, and no reasoning behind it.
4. **Does the structure serve the argument?** Sections that could be reordered
   without loss usually mean the paper is a list, not an argument.
5. **Are sources credible, current, and cited correctly?** Blogs and vendor pages
   standing in for peer-reviewed or primary sources cost points in graduate work.
6. **Mechanics and formatting:** these count, but last. Never lead with comma placement.

## Step 4: Score it

Score each rubric category, then compute a weighted total and convert to a letter
using `references/grade-bands.md`. Two numbers matter to the user:

- **Current grade** is what this draft earns as submitted today.
- **Projected grade** is what it earns if they make the required fixes. Be honest:
  if the paper's core problem is a weak thesis, a projected A is a lie, and the
  projection should say what ceiling the paper realistically has.

Grade against the standard for the course level, not against other drafts. Inflation
is the failure mode here. A paper that reads smoothly but never engages
counterarguments is a B+, and saying so is the whole value of this skill.

## Step 5: Write findings that can be acted on

Every finding needs four parts, or it isn't worth writing:

1. **Where** — page, section, or heading.
2. **What** — quote the actual sentence or passage you're flagging. Never write
   "strengthen your analysis." Write "Section 3 states X but cites nothing."
3. **Why it costs points** — tie it to a rubric category.
4. **The fix** — a concrete instruction. "Add the 2024 competitor revenue figures
   you cite in the intro and interpret what they mean for the recommendation."

Sort findings into three tiers:

- **Costing you a letter grade** — structural, thesis, evidence, prompt-drift.
- **Costing you points** — weak transitions, uneven depth, thin sourcing.
- **Polish** — mechanics, formatting, citation style.

Aim for 5–12 findings total. Twenty findings is a list nobody acts on.

## Step 6: Split group work by person

For a group paper, after the shared findings, produce a per-person section. Each
person gets their own heading with:

- The sections they own
- Their findings, in the same three tiers
- A short task list, each item starting with a verb and doable in one sitting
- An estimated time to complete

Also add a **Whole-team items** block for things no one person owns: inconsistent
voice across sections, duplicated content, a reference list that doesn't match the
in-text citations, an executive summary that contradicts the body. These are the
findings that sink group papers and the ones nobody catches, because each author
only reads their own part.

Be fair, not diplomatic. If one section is clearly weaker, say which and why. Critique the writing, never the person, and don't speculate about effort or
who slacked off.

## Step 7: Build the PDF

Write your findings to JSON, then run the report builder:

```bash
python3 scripts/build_report.py feedback.json -o "Feedback - <paper title>.pdf"
```

Run `python3 scripts/build_report.py --schema` to print the exact JSON structure
it expects. If `reportlab` isn't available, install it, and if that fails, deliver
the same content as a Markdown file instead. Never drop the deliverable silently.

Put the discipline in the report's `rubric_used` line, e.g.
"Graded as Economics and Econometrics · course rubric supplied".

Save the PDF where the user can download it, and present it to them.

## Step 8: Say it in chat too

Don't just hand over a file. In your reply, give them the current grade, the
projected grade, and the two or three fixes that matter most, in plain language.
Then point to the PDF for the full breakdown. If the paper is due imminently,
lead with the fixes that are achievable in the time they have left.
