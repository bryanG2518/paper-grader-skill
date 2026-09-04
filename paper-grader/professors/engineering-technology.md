# Engineering & Technology

## How this professor reads

Engineering work is graded on whether it would survive contact with reality. A
beautifully written report with an unstated assumption, a missing safety factor, or
an unverified result is a failing report in practice, and marked accordingly.

Shared standards across the area:

- **Assumptions are explicit or the analysis is worthless.** Every simplification, whether
  steady state, ideal gas, linear elastic, or no losses, gets stated and justified.
  An unstated assumption is the single most common serious finding in this area.
- **Units and dimensional consistency, everywhere:** a dimensionally inconsistent
  equation is an error of the first order, not a typo. SI unless the field convention
  says otherwise, and consistent throughout.
- **Significant figures reflect the precision of the measurement.** Six decimal places from a
  measurement good to two is a claim the data can't support.
- **Verification and validation:** does the result pass a sanity check? Order of
  magnitude, limiting cases, conservation. A model with no validation section is
  incomplete regardless of how sophisticated it is.
- **Design work needs constraints.** Codes, standards, safety factors, tolerances,
  cost, manufacturability. A design that ignores its constraints isn't a design.
- **Figures and tables carry the argument.** Every one needs axis labels with units,
  a caption, and a reference in the body. An uncited figure is cut.
- **Reproducibility:** enough detail that a competent reader could repeat the work.

**Typical weight shift** from `rubrics/default-academic.md`: raise Evidence and
analysis to 35%, add a Method and reproducibility category at 15%, cut Thesis to 10%.
IEEE citation style unless the course says otherwise.

---

### Chemical Engineering
- **Reads for:** mass and energy balances that close, and process reasoning that accounts for the conditions the plant will actually run under.
- **Evidence:** balance tables, thermodynamic property sources named, kinetics or transport correlations with their validity ranges.
- **Loses points for:** balances that don't close and aren't reconciled; correlations used outside their stated range; no consideration of safety, runaway, or waste streams; economics ignored in a design problem.

### Civil and Structural Engineering
- **Reads for:** load paths, limit states, and compliance with the governing code.
- **Evidence:** load combinations shown, code clauses cited by number, calculations traceable from actions to capacity check, factors of safety stated.
- **Loses points for:** naming a code without citing the clause; skipping serviceability after checking strength; ignoring foundations, drainage, construction sequence, or durability; no consideration of failure mode.

### Computer Science and Information Systems
- **Reads for:** correctness first, then complexity, then the empirical claim.
- **Evidence:** algorithm stated precisely, complexity derived not asserted, benchmarks with the environment specified, baselines that are actually competitive.
- **Loses points for:** performance claims with no baseline or no variance across runs; complexity given without derivation; ignoring edge cases and failure modes; a system paper with no evaluation section; unreleased code where the course expects it.

### Data Science and Artificial Intelligence
- **Reads for:** whether the result would survive someone trying to break it.
- **Evidence:** train/validation/test split described, hyperparameter search reported, appropriate metrics for the class balance, error bars or seeds across runs, ablations that isolate the contribution.
- **Loses points for:** any leakage between splits; accuracy on imbalanced data; a single run with no seed variance; no baseline; claiming causation from a predictive model; no discussion of dataset bias or deployment risk.

### Electrical and Electronic Engineering
- **Reads for:** circuit or system analysis that accounts for component non-idealities rather than ideal blocks.
- **Evidence:** schematics with values, derivations shown, simulation and measurement compared against each other, tolerance and noise considered.
- **Loses points for:** ideal-component assumptions carried into conclusions; simulation presented without measurement or vice versa where both were expected; no power, thermal, or EMC consideration; Bode plots with unlabeled axes.

### Mechanical and Aerospace Engineering
- **Reads for:** free-body reasoning, correct governing equations, and results checked against physical intuition.
- **Evidence:** FBDs, boundary conditions stated, material properties sourced, mesh convergence for any FEA/CFD, safety factors justified.
- **Loses points for:** FEA results with no mesh study or no validation; boundary conditions that don't match the physical situation; fatigue, vibration, or thermal expansion ignored where they govern; a result that fails an order-of-magnitude check and isn't questioned.

### Mineral and Mining Engineering
- **Reads for:** resource and reserve reasoning that respects geological uncertainty, and a plan that is operable and safe.
- **Evidence:** classification per a recognized code, grade-tonnage data, geotechnical parameters, recovery assumptions stated with basis.
- **Loses points for:** conflating resources with reserves; single-point estimates where a range is required; ventilation, ground control, or water management left out; closure and rehabilitation treated as an afterthought.

### Petroleum Engineering
- **Reads for:** reservoir and production reasoning grounded in the data available, with uncertainty carried through to the recommendation.
- **Evidence:** PVT and rock properties with sources, decline or material-balance analysis shown, sensitivity to the key uncertain parameters.
- **Loses points for:** deterministic forecasts presented without ranges; correlations applied outside their basis; well integrity, HSE, or emissions omitted; economics with no price sensitivity.
