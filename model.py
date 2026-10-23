"""KGRI synthetic feasibility benchmark — NOT real-world validation."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, brier_score_loss, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

FEATURES = ["rd_intensity", "innovation_spend", "employee_skills", "process_innovation",
            "collaboration", "leadership_support", "data_governance", "legacy_burden"]

def simulate(n, seed):
    rng = np.random.default_rng(seed)
    x = rng.beta(2.2, 2.2, (n, len(FEATURES)))
    df = pd.DataFrame(x, columns=FEATURES)
    z = (-2.8 + .8*x[:,0] + .65*x[:,1] + 1.2*x[:,2] + .7*x[:,3] +
         .5*x[:,4] + 1.1*x[:,5] + x[:,6] - 1.1*x[:,7] +
         1.6*(x[:,2]>.55)*(x[:,6]>.55) - (x[:,7]>.7)*(x[:,5]<.4))
    y = rng.binomial(1, 1/(1+np.exp(-z)))
    df = df.mask(rng.random(x.shape)<.035)
    return df, pd.Series(y, name="synthetic_label")

def rules(df):
    a = df.copy()
    a["complementarity_rule"] = ((a.employee_skills>.55)&(a.data_governance>.55)).astype(int)
    a["legacy_risk_rule"] = ((a.legacy_burden>.7)&(a.leadership_support<.4)).astype(int)
    a["innovation_capacity_rule"] = ((a.rd_intensity>.6)&(a.collaboration>.5)).astype(int)
    return a

def fit(x, y, linear, seed):
    if linear:
        base = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                             LogisticRegression(max_iter=2000, random_state=seed))
    else:
        base = make_pipeline(SimpleImputer(strategy="median"),
                             HistGradientBoostingClassifier(max_iter=120, learning_rate=.06,
                                                             l2_regularization=1., random_state=seed))
    return CalibratedClassifierCV(base, method="sigmoid", cv=3).fit(x, y)

def run(n, seed, output):
    if n<100:
        raise ValueError("n must be >= 100")
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)
    x, y = simulate(n, seed)
    tr, te = train_test_split(np.arange(n), test_size=.25, random_state=seed, stratify=y)
    med = x.iloc[tr].median()
    augmented = rules(x.fillna(med))
    variants = {"Logistic": (x, True), "Gradient boosting": (x, False),
                "KGRI prototype (boost + rules)": (augmented, False)}
    rows, predictions = [], {}
    for name, (data, linear) in variants.items():
        model = fit(data.iloc[tr], y.iloc[tr], linear, seed)
        p = model.predict_proba(data.iloc[te])[:,1]
        predictions[name] = p
        rows.append({"model": name, "auc": roc_auc_score(y.iloc[te], p),
                     "brier": brier_score_loss(y.iloc[te], p),
                     "accuracy_0.5": accuracy_score(y.iloc[te], p>=.5)})
    pd.DataFrame(rows).to_csv(out/"metrics.csv", index=False)
    fig, ax = plt.subplots(figsize=(7,4.4))
    ax.plot([0,1],[0,1],"--",color="gray",label="Perfect calibration")
    for name, p in predictions.items():
        bins = np.clip(np.digitize(p,np.linspace(0,1,11))-1,0,9)
        points = [(p[bins==b].mean(),y.iloc[te].to_numpy()[bins==b].mean())
                  for b in range(10) if (bins==b).sum()>=10]
        if points:
            ax.plot(*np.array(points).T,"o-",label=name)
    ax.set(xlabel="Predicted probability",ylabel="Observed synthetic-label frequency",
           title="Synthetic holdout: calibration",xlim=(0,1),ylim=(0,1))
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out/"figure2.png",dpi=220)
    plt.close(fig)
    demo = x.iloc[te].fillna(med)
    action = np.where(demo.data_governance<.45,"Assess data governance",
             np.where(demo.employee_skills<.45,"Assess workforce skills","Review roadmap"))
    pd.DataFrame({"synthetic_label_probability":predictions["KGRI prototype (boost + rules)"],
                  "non_causal_review_prompt":action}).to_csv(out/"decisions.csv",index=False)
    (out/"run_metadata.json").write_text(json.dumps({"seed":seed,"n_synthetic":n,
      "train_size":len(tr),"test_size":len(te),
      "warning":"SYNTHETIC ONLY; NO REAL-WORLD VALIDATION"},indent=2))
    print(pd.DataFrame(rows).to_string(index=False))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--n",type=int,default=2400)
    parser.add_argument("--seed",type=int,default=42)
    parser.add_argument("--output",default="outputs")
    args=parser.parse_args()
    run(args.n,args.seed,args.output)
