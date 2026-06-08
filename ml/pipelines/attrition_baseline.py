from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


@dataclass(frozen=True)
class TrainingResult:
    roc_auc: float
    feature_names: list[str]


def train_attrition_baseline(random_state: int = 42) -> TrainingResult:
    rng = np.random.default_rng(random_state)
    attendance_rate = rng.uniform(60, 100, 500)
    productivity = rng.uniform(45, 100, 500)
    tenure_months = rng.integers(1, 96, 500)
    manager_change_count = rng.integers(0, 5, 500)

    risk_signal = (
        (attendance_rate < 82).astype(int)
        + (productivity < 70).astype(int)
        + (tenure_months < 9).astype(int)
        + (manager_change_count > 2).astype(int)
    )
    attrition = (risk_signal >= 2).astype(int)

    features = np.column_stack([attendance_rate, productivity, tenure_months, manager_change_count])
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        attrition,
        test_size=0.25,
        random_state=random_state,
        stratify=attrition,
    )
    model = RandomForestClassifier(n_estimators=80, max_depth=6, random_state=random_state)
    model.fit(x_train, y_train)
    probabilities = model.predict_proba(x_test)[:, 1]
    return TrainingResult(
        roc_auc=round(float(roc_auc_score(y_test, probabilities)), 3),
        feature_names=["attendance_rate", "productivity", "tenure_months", "manager_change_count"],
    )


if __name__ == "__main__":
    result = train_attrition_baseline()
    print(result)
