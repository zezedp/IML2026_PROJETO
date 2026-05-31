import json
import os
import pickle
import warnings
from pathlib import Path
import sys

from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    auc,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split

sys.path.append(str(Path(__file__).resolve().parents[3]))
from ml.models import criar_modelo
from ml.kfold_optimizer import KFoldOptimizer
from ml.synthetic_data import balancear_treino

from app.core.config import (
    BINARY_FEATURES,
    CONTINUOUS_FEATURES,
    CORRELATION_LABELS,
    DATASET_ARTIFACTS_DIR,
    DATASET_PATH,
    FEATURE_DISPLAY_NAMES,
    FEATURES,
    METRICS_ARTIFACTS_DIR,
    MODEL_METADATA,
    MODELS_ARTIFACTS_DIR,
    TARGET,
)


RANDOM_STATE = 42
DEFAULT_SAMPLE_SIZE = 250_000


def main() -> None:
    create_directories()
    df = pd.read_csv(DATASET_PATH)
    export_dataset_artifacts(df)
    export_model_artifacts(df)
    print("Artifacts exported to app/data/artifacts")


def create_directories() -> None:
    for directory in [DATASET_ARTIFACTS_DIR, METRICS_ARTIFACTS_DIR, MODELS_ARTIFACTS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def export_dataset_artifacts(df: pd.DataFrame) -> None:
    write_json(DATASET_ARTIFACTS_DIR / "overview.json", build_overview(df))
    write_json(DATASET_ARTIFACTS_DIR / "statistics.json", build_statistics(df))
    write_json(DATASET_ARTIFACTS_DIR / "class_distribution.json", build_class_distribution(df))
    write_json(DATASET_ARTIFACTS_DIR / "sample.json", build_sample(df))
    write_json(DATASET_ARTIFACTS_DIR / "histograms.json", build_histograms(df))
    write_json(DATASET_ARTIFACTS_DIR / "boxplots.json", build_boxplots(df))
    write_json(DATASET_ARTIFACTS_DIR / "binary_features.json", build_binary_features(df))
    write_json(DATASET_ARTIFACTS_DIR / "correlation.json", build_correlation(df))


def build_overview(df: pd.DataFrame) -> dict[str, Any]:
    total = int(len(df))
    fraud_count = int(df[TARGET].sum())
    legitimate_count = total - fraud_count
    fraud_rate = fraud_count / total
    return {
        "total_transactions": total,
        "legitimate_transactions": legitimate_count,
        "fraud_transactions": fraud_count,
        "legitimate_rate": round(legitimate_count / total, 6),
        "fraud_rate": round(fraud_rate, 6),
    }


def build_statistics(df: pd.DataFrame) -> dict[str, Any]:
    rows = []
    for feature in FEATURES:
        series = df[feature]
        rows.append(
            {
                "feature": feature,
                "display_name": FEATURE_DISPLAY_NAMES[feature],
                "min": round(float(series.min()), 6),
                "mean": round(float(series.mean()), 6),
                "max": round(float(series.max()), 6),
                "std": round(float(series.std()), 6),
            }
        )
    return {"statistics": rows}


def build_class_distribution(df: pd.DataFrame) -> dict[str, Any]:
    total = len(df)
    legitimate_count = int((df[TARGET] == 0).sum())
    fraud_count = int((df[TARGET] == 1).sum())
    return {
        "labels": ["Legitima", "Fraude"],
        "counts": [legitimate_count, fraud_count],
        "percentages": [
            round(100 * legitimate_count / total, 4),
            round(100 * fraud_count / total, 4),
        ],
    }


def build_sample(df: pd.DataFrame) -> dict[str, Any]:
    sample_rows = []
    for index, row in df.head(5).reset_index().iterrows():
        item = {"index": int(index)}
        for feature in FEATURES:
            item[feature] = round(float(row[feature]), 6)
        item[TARGET] = int(row[TARGET])
        sample_rows.append(item)
    return {"sample": sample_rows}


def build_histograms(df: pd.DataFrame) -> dict[str, Any]:
    bins_by_feature = {
        "distance_from_home": [0, 5, 15, 30, 50, 100, 200, np.inf],
        "distance_from_last_transaction": [0, 1, 2, 5, 10, 25, 50, 100, np.inf],
        "ratio_to_median_purchase_price": [0, 0.5, 1, 2, 3, 5, 10, np.inf],
    }

    histograms = {}
    for feature, bins in bins_by_feature.items():
        legitimate = df.loc[df[TARGET] == 0, feature]
        fraud = df.loc[df[TARGET] == 1, feature]
        legitimate_counts, _ = np.histogram(legitimate, bins=bins)
        fraud_counts, _ = np.histogram(fraud, bins=bins)
        histograms[feature] = {
            "feature": feature,
            "labels": format_bin_labels(bins),
            "legitimate": percentage_list(legitimate_counts),
            "fraud": percentage_list(fraud_counts),
            "insight": histogram_insight(feature),
        }
    return histograms


def build_boxplots(df: pd.DataFrame) -> dict[str, Any]:
    boxplots = {}
    for feature in CONTINUOUS_FEATURES:
        boxplots[feature] = {
            "feature": feature,
            "legitimate": quantiles(df.loc[df[TARGET] == 0, feature]),
            "fraud": quantiles(df.loc[df[TARGET] == 1, feature]),
        }
    return boxplots


def build_binary_features(df: pd.DataFrame) -> dict[str, Any]:
    legitimate = df[df[TARGET] == 0]
    fraud = df[df[TARGET] == 1]
    return {
        "features": BINARY_FEATURES,
        "display_names": [FEATURE_DISPLAY_NAMES[feature] for feature in BINARY_FEATURES],
        "legitimate": [round(float(legitimate[feature].mean() * 100), 4) for feature in BINARY_FEATURES],
        "fraud": [round(float(fraud[feature].mean() * 100), 4) for feature in BINARY_FEATURES],
    }


def build_correlation(df: pd.DataFrame) -> dict[str, Any]:
    columns = FEATURES + [TARGET]
    corr = df[columns].corr(numeric_only=True).round(6)
    return {
        "labels": [CORRELATION_LABELS[column] for column in columns],
        "matrix": corr.values.tolist(),
    }


def export_model_artifacts(df: pd.DataFrame) -> None:
    sample_df = stratified_sample(df, get_sample_size(len(df)))
    x = sample_df[FEATURES]
    y = sample_df[TARGET].astype(int)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    models_mapping = {
        "lda": "LDA",
        "qda": "QDA",
        "lr": "Logistic Regression",
        "rf": "Random Forest",
    }
    
    optimizer = KFoldOptimizer(x_train.values, y_train.values, n_splits=5)
    resultados_kfold = optimizer.executar(list(models_mapping.values()))

    best_n_sint_by_model = {}
    for short_key, ml_name in models_mapping.items():
        res_modelo = {k: v for k, v in resultados_kfold.items() if k[0] == ml_name}
        melhor_chave = max(res_modelo.keys(), key=lambda k: res_modelo[k]['f1_mean'])
        best_n_sint_by_model[short_key] = melhor_chave[1]

    metrics_rows = []
    confusion_payload = {"models": {}, "test_size": int(len(y_test))}
    roc_payload = {"models": {}}
    cv_payload = {"folds": [1, 2, 3, 4, 5], "models": {}}

    rf_raw_model = None

    for key, ml_name in models_mapping.items():
        short_name, full_name = MODEL_METADATA[key]
        n_sint = best_n_sint_by_model[key]
        
        X_train_bal, y_train_bal = balancear_treino(x_train.values, y_train.values, n_sint)

        modelo_wrapper = criar_modelo(ml_name)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            modelo_wrapper.treinar(X_train_bal, y_train_bal)

        model = modelo_wrapper.modelo
        if key == "rf":
            rf_raw_model = model

        with (MODELS_ARTIFACTS_DIR / f"{key}_model.pkl").open("wb") as file:
            pickle.dump(model, file)

        y_pred = model.predict(x_test.values)
        y_score = fraud_scores(model, x_test.values)
        model_metrics = calculate_metrics(y_test, y_pred, y_score)
        metrics_rows.append(
            {
                "id": key,
                "name": short_name,
                "full_name": full_name,
                **model_metrics,
                "is_best": False,
            }
        )

        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        confusion_payload["models"][key] = {
            "name": short_name,
            "true_negative": int(tn),
            "false_positive": int(fp),
            "false_negative": int(fn),
            "true_positive": int(tp),
        }

        fpr, tpr, _ = roc_curve(y_test, y_score)
        roc_payload["models"][key] = {
            "label": f"{short_name} (AUC={auc(fpr, tpr):.3f})",
            "points": sample_roc_points(fpr, tpr),
        }

        kfold_data = resultados_kfold[(ml_name, n_sint)]
        cv_payload["models"][key] = {
            "scores": [round(float(s), 6) for s in kfold_data['f1_scores']],
            "mean": round(float(kfold_data['f1_mean']), 6),
            "std": round(float(np.std(kfold_data['f1_scores'])), 6),
        }

    best_model = max(metrics_rows, key=lambda row: row["f1_score"])
    best_model["is_best"] = True
    write_json(METRICS_ARTIFACTS_DIR / "metrics.json", {"models": metrics_rows, "best_model": best_model["id"]})
    write_json(METRICS_ARTIFACTS_DIR / "confusion_matrices.json", confusion_payload)
    write_json(METRICS_ARTIFACTS_DIR / "roc_curves.json", roc_payload)
    write_json(METRICS_ARTIFACTS_DIR / "cross_validation.json", cv_payload)
    write_json(METRICS_ARTIFACTS_DIR / "feature_importance.json", feature_importance_payload(rf_raw_model))


def calculate_metrics(y_true: pd.Series, y_pred: np.ndarray, y_score: np.ndarray) -> dict[str, float]:
    return {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 6),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 6),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 6),
        "f1_score": round(float(f1_score(y_true, y_pred, zero_division=0)), 6),
        "auc_roc": round(float(roc_auc_score(y_true, y_score)), 6),
    }


def feature_importance_payload(model: Any) -> dict[str, Any]:
    importances = model.feature_importances_
    rows = [
        {
            "name": feature,
            "display_name": FEATURE_DISPLAY_NAMES[feature],
            "importance": round(float(importance * 100), 4),
        }
        for feature, importance in zip(FEATURES, importances)
    ]
    rows.sort(key=lambda row: row["importance"], reverse=True)
    return {"model": "Random Forest", "features": rows}


def fraud_scores(model: Any, x: pd.DataFrame) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(x)
        classes = list(getattr(model, "classes_", [0, 1]))
        class_index = classes.index(1) if 1 in classes else probabilities.shape[1] - 1
        return probabilities[:, class_index]
    return model.decision_function(x)


def stratified_sample(df: pd.DataFrame, sample_size: int) -> pd.DataFrame:
    if sample_size >= len(df):
        return df
    sampled_groups = []
    for _, group in df.groupby(TARGET):
        group_size = max(1, round(len(group) * sample_size / len(df)))
        sampled_groups.append(group.sample(n=group_size, random_state=RANDOM_STATE))
    return pd.concat(sampled_groups).sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)


def get_sample_size(total_rows: int) -> int:
    raw = os.getenv("FRAUDSHIELD_EXPORT_SAMPLE_SIZE", str(DEFAULT_SAMPLE_SIZE))
    sample_size = int(raw)
    if sample_size <= 0:
        raise ValueError("FRAUDSHIELD_EXPORT_SAMPLE_SIZE must be positive.")
    return min(sample_size, total_rows)


def quantiles(series: pd.Series) -> dict[str, float]:
    return {
        "q1": round(float(series.quantile(0.25)), 6),
        "median": round(float(series.quantile(0.5)), 6),
        "q3": round(float(series.quantile(0.75)), 6),
    }


def percentage_list(counts: np.ndarray) -> list[float]:
    total = counts.sum()
    if total == 0:
        return [0.0 for _ in counts]
    return [round(float(count / total * 100), 4) for count in counts]


def format_bin_labels(bins: list[float]) -> list[str]:
    labels = []
    for start, end in zip(bins[:-1], bins[1:]):
        if np.isinf(end):
            labels.append(f"{format_bin_value(start)}+")
        else:
            labels.append(f"{format_bin_value(start)}-{format_bin_value(end)}")
    return labels


def format_bin_value(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else str(value)


def histogram_insight(feature: str) -> str:
    insights = {
        "distance_from_home": "Fraudes tendem a aparecer com maior frequencia em distancias maiores da residencia.",
        "distance_from_last_transaction": "Saltos grandes desde a ultima transacao elevam o risco observado.",
        "ratio_to_median_purchase_price": "Compras muito acima do padrao mediano historico concentram mais fraudes.",
    }
    return insights[feature]


def sample_roc_points(fpr: np.ndarray, tpr: np.ndarray, max_points: int = 120) -> list[dict[str, float]]:
    if len(fpr) <= max_points:
        indexes = range(len(fpr))
    else:
        indexes = np.linspace(0, len(fpr) - 1, max_points, dtype=int)
    points = [{"fpr": round(float(fpr[index]), 6), "tpr": round(float(tpr[index]), 6)} for index in indexes]
    if points[0] != {"fpr": 0.0, "tpr": 0.0}:
        points.insert(0, {"fpr": 0.0, "tpr": 0.0})
    if points[-1] != {"fpr": 1.0, "tpr": 1.0}:
        points.append({"fpr": 1.0, "tpr": 1.0})
    return points


def write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=True, indent=2)


if __name__ == "__main__":
    main()
