"""Inspect local FAT files without publishing confidential microdata.

Usage: python audit_data.py path/to/downloaded/file.csv
       python audit_data.py path/to/downloaded/file.dta --target TARGET_COLUMN
Outputs metadata-only JSON; no row-level data are exported.
"""
import argparse
import json
from pathlib import Path
import pandas as pd

def main():
    p = argparse.ArgumentParser()
    p.add_argument("path", type=Path)
    p.add_argument("--target", default=None, help="Candidate outcome to inspect, not validate")
    p.add_argument("--out", type=Path, default=Path("outputs/data_audit.json"))
    a = p.parse_args()
    if not a.path.is_file():
        raise SystemExit(f"Missing input file: {a.path}")
    ext = a.path.suffix.lower()
    if ext == ".csv":
        df = pd.read_csv(a.path, low_memory=False)
    elif ext == ".dta":
        df = pd.read_stata(a.path, convert_categoricals=False)
    elif ext in {".xlsx", ".xls"}:
        df = pd.read_excel(a.path)
    elif ext == ".parquet":
        df = pd.read_parquet(a.path)
    else:
        raise SystemExit("Supported formats: CSV, Stata DTA, Excel, Parquet")
    if df.empty:
        raise SystemExit("Dataset has no rows")
    report = {
        "source_file_name": a.path.name,
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "duplicate_rows": int(df.duplicated().sum()),
        "column_profiles": [{
            "name": str(c), "dtype": str(df[c].dtype),
            "missing_pct": round(float(df[c].isna().mean()*100), 2),
            "unique_count": int(df[c].nunique(dropna=True))
        } for c in df.columns],
        "candidate_target": a.target,
        "target_review": None,
        "warnings": [
            "This is a descriptive audit only, not a validated readiness label.",
            "Check the FAT dictionary for survey codes, special missing values and design weights.",
            "Determine whether firm IDs link actual longitudinal observations.",
            "Do not use target-defining survey items as predictors."
        ]
    }
    if a.target:
        if a.target not in df:
            raise SystemExit(f"Target not found: {a.target}")
        s = df[a.target]
        report["target_review"] = {
            "nonmissing": int(s.notna().sum()),
            "unique_nonmissing": int(s.nunique(dropna=True)),
            "value_counts_top10": {str(k): int(v) for k,v in
                s.value_counts(dropna=False).head(10).items()}
        }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(f"Saved metadata-only audit: {a.out}")

if __name__ == "__main__":
    main()
