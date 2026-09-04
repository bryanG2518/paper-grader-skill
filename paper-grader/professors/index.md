# Discipline routing

Classify the paper into one subject, then open **only** that subject's faculty-area
file. Read the area's shared standards first, then the subject block.

| Faculty area | File |
|---|---|
| Arts & Humanities | `professors/arts-humanities.md` |
| Engineering & Technology | `professors/engineering-technology.md` |
| Life Sciences & Medicine | `professors/life-sciences-medicine.md` |
| Natural Sciences | `professors/natural-sciences.md` |
| Social Sciences & Management | `professors/social-sciences-management.md` |

## How to classify

Use evidence from the paper itself, in this order of authority:

1. **The course code or department** on the title page. This beats everything. A
   paper on renewable energy filed under ECON is an economics paper and gets graded
   as one, no matter how much chemistry is in it.
2. **The assignment prompt**, if supplied.
3. **The method:** what the paper *does* is a stronger signal than what it's about.
   Regression on survey data is social science; a titration write-up is chemistry;
   close reading of a primary text is humanities. Climate change appears in
   Environmental Sciences, Geography, Economics, Politics, and Philosophy papers,
   and the method tells you which one you're holding.
4. **Citation style:** APA suggests psychology, education, or business. MLA suggests
   literature or languages. Chicago notes suggest history. IEEE suggests engineering.
   Vancouver suggests medicine. Bluebook means law. Weak signal alone, useful as a tiebreaker.
5. **The sources cited:** the journals in the reference list usually settle it.

State your classification in one line at the top of the feedback, so the user can
correct you: *"Graded as Politics and International Studies. Say the word if this is
for a Sociology course; the standards differ."*

## Interdisciplinary papers

Pick the **primary** discipline, the one whose standards the professor will apply,
and grade against it. Then check the secondary discipline for one thing only:
whether the paper meets that field's basic competence bar, because borrowed methods
applied badly are where interdisciplinary work loses the most points. A politics
paper running a regression is graded as politics, but the regression still has to be
defensible, and misspecification is a finding.

If two disciplines are equally central and no course code settles it, say so, grade
against the stricter evidence standard of the two, and tell the user which you chose.

## Subject list

**Arts & Humanities:** Architecture and Built Environment · Art and Design ·
Archaeology · Classics and Ancient History · English Language and Literature ·
History · Linguistics · Modern Languages · Performing Arts · Philosophy ·
Theology and Religious Studies

**Engineering & Technology:** Chemical Engineering · Civil and Structural
Engineering · Computer Science and Information Systems · Data Science and Artificial
Intelligence · Electrical and Electronic Engineering · Mechanical and Aerospace
Engineering · Mineral and Mining Engineering · Petroleum Engineering

**Life Sciences & Medicine:** Agriculture and Forestry · Anatomy and Physiology ·
Biological Sciences · Dentistry · Medicine · Nursing · Pharmacy and Pharmacology ·
Psychology · Veterinary Science

**Natural Sciences:** Chemistry · Earth and Marine Sciences · Environmental Sciences ·
Geography · Geology · Geophysics · Materials Sciences · Mathematics ·
Physics and Astronomy

**Social Sciences & Management:** Accounting and Finance · Anthropology ·
Business and Management Studies · Communication and Media Studies · Economics and
Econometrics · Education and Training · Hospitality and Leisure Management ·
Law and Legal Studies · Marketing · Politics and International Studies ·
Social Policy and Administration · Sociology · Statistics and Operational Research

## If nothing fits

Some papers won't land cleanly: an interdisciplinary studies capstone, a personal
statement, a grant proposal. Say that no subject file applies, grade against
`rubrics/default-academic.md`, and ask the user which department is marking it.
Never force a bad classification; grading a theology paper by engineering standards
produces confident, useless feedback.
