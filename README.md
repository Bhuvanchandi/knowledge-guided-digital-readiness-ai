# KGRI — Knowledge-Guided Readiness Intelligence

Research-stage prototype for knowledge-guided AI decision support using enterprise innovation indicators.

**Scientific status:** The executable example uses synthetic data and synthetic labels. It is not real-world validation, does not establish predictive superiority, and must not be cited as evidence of enterprise digital transformation readiness.

## Reproduce

```bash
python -m pip install -r requirements.txt
python model.py --seed 42 --n 2400
```

Generated outputs: `outputs/metrics.csv`, `outputs/figure2.png`, `outputs/decisions.csv`, `outputs/run_metadata.json`.

Current methods: logistic regression, histogram gradient boosting, rule-feature-augmented gradient boosting, training-only cross-validated sigmoid calibration, AUROC, Brier score, accuracy, and a calibration plot.

**Not implemented yet:** independently observed readiness outcome, longitudinal validation, 2×2 ablations, bootstrap confidence intervals, uncertainty-aware decision optimization, Figure 1, final two manuscript tables, and publishable empirical conclusions.

See `RESEARCH_PROTOCOL.md` for the next-stage validation requirements.
