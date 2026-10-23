# KGRI research protocol (draft)

## Research question
Do predeclared organizational knowledge rules improve out-of-sample prediction calibration and decision-support utility beyond competitive data-driven models?

## Data and construct validity
Candidate: World Bank Firm Adoption of Technology (FAT) survey, https://microdata.worldbank.org/catalog/8209 . Inspect codebook, data permissions, waves, and firm linkage before finalizing a target. FAT measures technology adoption/sophistication, **not automatically prospective digital transformation readiness**.

Preferred target: independently observed future adoption/sophistication transition Y(t+1), predicted from earlier X(t). Exclude leakage from target-defining variables. If only cross-sectional observations exist, frame the task as contemporaneous technology adoption classification, not future readiness prediction.

## Knowledge rules
Specify from independent literature or expert elicitation before viewing test labels. Examine whether higher skills, stronger governance, and lower legacy burden imply defensible conditional monotonicity or interaction constraints; audit exceptions and subgroup fairness. Distinguish adding rule features from a genuine knowledge-regularized learning objective.

## Baselines and design
Logistic regression, random forest, tuned gradient boosting, rules-only model, calibrated baselines, and full knowledge-guided model. Fit preprocessing and calibration on training/validation partitions only. Prefer firm-disjoint, country/wave held-out testing where supported.

Primary metric: held-out Brier score. Secondary: AUROC, PR-AUC, ECE, decision-curve net benefit, knowledge-rule violation, and subgroup results. Report confidence intervals, paired model comparisons, repeated seeds, missingness/noise/shift sensitivity, and full sample sizes.

## Required paper assets
Exactly **two figures**: (1) vector architecture; (2) multi-panel held-out performance, calibration, and robustness.
Exactly **two tables**: (1) cohort and model comparison; (2) 2×2 knowledge × calibration ablation with uncertainty and decision utility.

## Integrity rules
No synthetic benchmark is external validation. Do not claim superiority without measured held-out results. No causal intervention claims from observational associations. Save split identifiers, raw predictions, config, seeds, and data provenance. Check data licensing before publishing any records.

Status: protocol only; real-data study not yet executed.
