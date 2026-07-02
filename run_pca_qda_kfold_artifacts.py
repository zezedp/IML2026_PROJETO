import json
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline


RANDOM_STATE = 4267
N_SPLITS = 5
N_SINTETICO = 146701
N_COMPONENTS = 3

MODEL_ID = "pca_qda"
MODEL_NAME = "PCA + QDA"
MODEL_FULL_NAME = f"PCA ({N_COMPONENTS} componentes) + Quadratic Discriminant Analysis"

DATASET_PATH = Path("dataset/card_transdata.csv")
METRICS_DIR = Path("app/data/artifacts/metrics")
MODELS_DIR = Path("app/data/artifacts/models")

COLUNAS_CONTINUAS = [
    "distance_from_home",
    "distance_from_last_transaction",
    "ratio_to_median_purchase_price",
]

COLUNAS_BINARIAS = [
    "repeat_retailer",
    "used_chip",
    "used_pin_number",
    "online_order",
]

TODAS_FEATURES = COLUNAS_CONTINUAS + COLUNAS_BINARIAS


def round_float(value, ndigits=6):
    return round(float(value), ndigits)


def gerar_continuas(df_fraud, n_sintetico):
    x_cont = df_fraud[COLUNAS_CONTINUAS].values
    mu = x_cont.mean(axis=0)
    sigma = np.cov(x_cont, rowvar=False)
    rng = np.random.default_rng(seed=RANDOM_STATE)
    return rng.multivariate_normal(mu, sigma, size=n_sintetico)


def gerar_binarias_multivariadas(df_fraud, n_sintetico):
    rng = np.random.default_rng(seed=RANDOM_STATE)
    combinacoes = (
        df_fraud[COLUNAS_BINARIAS]
        .value_counts(normalize=True)
        .reset_index(name="prob")
    )
    indices = rng.choice(
        combinacoes.index,
        size=n_sintetico,
        p=combinacoes["prob"],
    )
    amostras = combinacoes.loc[indices, COLUNAS_BINARIAS].reset_index(drop=True)
    return {col: amostras[col].to_numpy() for col in COLUNAS_BINARIAS}


def balance_train(x_train, y_train, n_sintetico):
    df_train = pd.DataFrame(x_train, columns=TODAS_FEATURES)
    df_train["fraud"] = y_train

    fraud_data = df_train[df_train["fraud"] == 1.0]

    df_sintetico = pd.DataFrame(
        gerar_continuas(fraud_data, n_sintetico),
        columns=COLUNAS_CONTINUAS,
    )
    binarias = gerar_binarias_multivariadas(fraud_data, n_sintetico)
    for col in COLUNAS_BINARIAS:
        df_sintetico[col] = binarias[col]
    df_sintetico["fraud"] = 1.0

    df_balanceado = pd.concat([df_train, df_sintetico], ignore_index=True)
    return df_balanceado[TODAS_FEATURES].values, df_balanceado["fraud"].values


def criar_pca_qda():
    return Pipeline(
        [
            ("pca", PCA(n_components=N_COMPONENTS)),
            ("qda", QuadraticDiscriminantAnalysis()),
        ]
    )


def read_json(path):
    if not path.exists() or path.stat().st_size == 0:
        return {"models": {}}
    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(f"{path.suffix}.tmp")
    with temp_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")
    temp_path.replace(path)


def sample_curve_points(x_values, y_values, x_key, y_key, max_points=500):
    if len(x_values) <= max_points:
        indexes = range(len(x_values))
    else:
        indexes = np.linspace(0, len(x_values) - 1, max_points, dtype=int)

    points = []
    seen = set()
    for index in indexes:
        point = {
            x_key: round_float(x_values[index]),
            y_key: round_float(y_values[index]),
        }
        point_key = (point[x_key], point[y_key])
        if point_key not in seen:
            points.append(point)
            seen.add(point_key)
    return points


def sample_existing_points(points, x_key, y_key, max_points=500):
    if len(points) <= max_points:
        return [
            {x_key: round_float(point[x_key]), y_key: round_float(point[y_key])}
            for point in points
        ]

    indexes = np.linspace(0, len(points) - 1, max_points, dtype=int)
    sampled = []
    seen = set()
    for index in indexes:
        source = points[index]
        point = {
            x_key: round_float(source[x_key]),
            y_key: round_float(source[y_key]),
        }
        point_key = (point[x_key], point[y_key])
        if point_key not in seen:
            sampled.append(point)
            seen.add(point_key)
    return sampled


def compact_curve_models(data, x_key, y_key):
    for model in data.get("models", {}).values():
        model["points"] = sample_existing_points(model.get("points", []), x_key, y_key)


def save_model(model):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    path = MODELS_DIR / f"{MODEL_ID}_model.pkl"
    with path.open("wb") as file:
        pickle.dump(model, file)
    return path


def update_metrics_json(test_metrics):
    path = METRICS_DIR / "metrics.json"
    data = read_json(path)

    data["models"] = [model for model in data["models"] if model.get("id") != MODEL_ID]
    data["models"].append(
        {
            "id": MODEL_ID,
            "name": MODEL_NAME,
            "full_name": MODEL_FULL_NAME,
            "accuracy": round_float(test_metrics["accuracy"]),
            "precision": float(test_metrics["precision"]),
            "recall": float(test_metrics["recall"]),
            "f1_score": float(test_metrics["f1_score"]),
            "auc_roc": round_float(test_metrics["auc_roc"], 4),
            "pr_auc": round_float(test_metrics["pr_auc"], 4),
            "is_best": False,
            "n_sintetico": N_SINTETICO,
            "n_components": N_COMPONENTS,
        }
    )

    best_model = max(data["models"], key=lambda model: model["f1_score"])
    for model in data["models"]:
        model["is_best"] = model["id"] == best_model["id"]
    data["best_model"] = best_model["id"]

    write_json(path, data)


def update_cross_validation_json(fold_metrics):
    path = METRICS_DIR / "cross_validation.json"
    data = read_json(path)
    fold_df = pd.DataFrame(fold_metrics)

    data.setdefault("folds", list(range(1, N_SPLITS + 1)))
    data["models"][MODEL_ID] = {
        "scores": [round_float(value) for value in fold_df["f1"].tolist()],
        "mean": round_float(fold_df["f1"].mean()),
        "std": round_float(fold_df["f1"].std(ddof=1)),
        "metrics_by_fold": [
            {
                "fold": int(row["fold"]),
                "accuracy": round_float(row["accuracy"]),
                "precision": round_float(row["precision"]),
                "recall": round_float(row["recall"]),
                "f1": round_float(row["f1"]),
                "auc_roc": round_float(row["auc_roc"]),
                "pr_auc": round_float(row["pr_auc"]),
            }
            for _, row in fold_df.iterrows()
        ],
        "n_sintetico": N_SINTETICO,
        "n_components": N_COMPONENTS,
    }

    write_json(path, data)


def update_confusion_matrices_json(y_test, y_pred):
    path = METRICS_DIR / "confusion_matrices.json"
    data = read_json(path)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

    data["models"][MODEL_ID] = {
        "name": MODEL_NAME,
        "true_negative": int(tn),
        "false_positive": int(fp),
        "false_negative": int(fn),
        "true_positive": int(tp),
        "n_sintetico": N_SINTETICO,
        "n_components": N_COMPONENTS,
    }
    data["test_size"] = int(len(y_test))

    write_json(path, data)


def update_roc_curves_json(y_test, y_score, auc_roc):
    path = METRICS_DIR / "roc_curves.json"
    data = read_json(path)
    fpr, tpr, _ = roc_curve(y_test, y_score)

    data["models"][MODEL_ID] = {
        "label": f"{MODEL_NAME} (AUC={auc_roc:.3f})",
        "points": sample_curve_points(fpr, tpr, "fpr", "tpr"),
    }

    compact_curve_models(data, "fpr", "tpr")
    write_json(path, data)


def update_pr_curves_json(y_test, y_score, pr_auc):
    path = METRICS_DIR / "pr_curves.json"
    data = read_json(path)
    precision, recall, _ = precision_recall_curve(y_test, y_score)

    data["models"][MODEL_ID] = {
        "label": f"{MODEL_NAME} (AP={pr_auc:.3f})",
        "points": sample_curve_points(recall, precision, "recall", "precision"),
    }

    compact_curve_models(data, "recall", "precision")
    write_json(path, data)


def main():
    print("Carregando dataset...")
    df = pd.read_csv(DATASET_PATH)
    x = df[TODAS_FEATURES].values
    y = df["fraud"].values

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    print(
        f"Treino={len(y_train)} | Teste={len(y_test)} | "
        f"n_sintetico={N_SINTETICO} | componentes={N_COMPONENTS}"
    )

    skf = StratifiedKFold(
        n_splits=N_SPLITS,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    fold_metrics = []
    for fold, (train_idx, val_idx) in enumerate(skf.split(x_train, y_train), start=1):
        x_tr, x_val = x_train[train_idx], x_train[val_idx]
        y_tr, y_val = y_train[train_idx], y_train[val_idx]

        x_tr_bal, y_tr_bal = balance_train(x_tr, y_tr, N_SINTETICO)
        model = criar_pca_qda()
        model.fit(x_tr_bal, y_tr_bal)

        y_pred = model.predict(x_val)
        y_score = model.predict_proba(x_val)[:, 1]

        metrics = {
            "fold": fold,
            "accuracy": accuracy_score(y_val, y_pred),
            "precision": precision_score(y_val, y_pred, zero_division=0),
            "recall": recall_score(y_val, y_pred, zero_division=0),
            "f1": f1_score(y_val, y_pred, zero_division=0),
            "auc_roc": roc_auc_score(y_val, y_score),
            "pr_auc": average_precision_score(y_val, y_score),
        }
        fold_metrics.append(metrics)
        print(
            f"Fold {fold}: "
            f"f1={metrics['f1']:.6f}, "
            f"accuracy={metrics['accuracy']:.6f}, "
            f"recall={metrics['recall']:.6f}"
        )

    print("Treinando modelo final no treino completo balanceado...")
    x_train_bal, y_train_bal = balance_train(x_train, y_train, N_SINTETICO)
    final_model = criar_pca_qda()
    final_model.fit(x_train_bal, y_train_bal)

    y_pred_test = final_model.predict(x_test)
    y_score_test = final_model.predict_proba(x_test)[:, 1]

    test_metrics = {
        "accuracy": accuracy_score(y_test, y_pred_test),
        "precision": precision_score(y_test, y_pred_test, zero_division=0),
        "recall": recall_score(y_test, y_pred_test, zero_division=0),
        "f1_score": f1_score(y_test, y_pred_test, zero_division=0),
        "auc_roc": roc_auc_score(y_test, y_score_test),
        "pr_auc": average_precision_score(y_test, y_score_test),
    }

    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    update_metrics_json(test_metrics)
    update_cross_validation_json(fold_metrics)
    update_confusion_matrices_json(y_test, y_pred_test)
    update_roc_curves_json(y_test, y_score_test, test_metrics["auc_roc"])
    update_pr_curves_json(y_test, y_score_test, test_metrics["pr_auc"])
    model_path = save_model(final_model)

    print("Metricas de teste:")
    for key, value in test_metrics.items():
        print(f"  {key}: {value:.6f}")
    print("Artefatos atualizados em app/data/artifacts/metrics")
    print(f"Modelo salvo em {model_path}")


if __name__ == "__main__":
    main()
