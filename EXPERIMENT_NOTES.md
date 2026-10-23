# Real-data experiment — preliminary results (2026-10-23)

Source: user-provided World Bank FAT microdata. Raw records are **not** published.

Target: `b7b >= 7`, exploratory classification of **self-rated** global technology sophistication, not future digital transformation readiness. Survey questionnaire describes `b7b` as 1–10 self-assessment against the world's most advanced firms.

Validation: 60% model training, 20% calibration, 20% random test (seed 42); additional Kenya-held-out test. Gradient boosting with or without two engineered interaction indicators (manager education and computers; zero computers), and with or without post-hoc sigmoid calibration.

| Test | Variant | AUROC | Brier |
|---|---|---:|---:|
| Random (n=4146) | Base | 0.797315 | 0.134879 |
| Random | Calibrated | 0.797315 | 0.134730 |
| Random | Rule-feature | 0.798543 | 0.134801 |
| Random | Rule-feature + calibrated | 0.798543 | 0.134555 |
| Kenya-held-out (n=1305) | Base | 0.684184 | 0.166155 |
| Kenya-held-out | Calibrated | 0.684184 | 0.166414 |
| Kenya-held-out | Rule-feature | 0.674070 | 0.167552 |
| Kenya-held-out | Rule-feature + calibrated | 0.674070 | 0.167870 |

**Interpretation:** The random-split gain is tiny, and the knowledge-feature variant degrades on the country-held-out test. These exploratory results **do not validate KGRI superiority**. Rule features are not enforced constraints; no confidence intervals, design weights, multi-country leave-one-out analysis, or decision-utility study yet.

The executable script and figures are available in the associated research conversation; they are not yet committed here. Do not present these results as publication-ready.
