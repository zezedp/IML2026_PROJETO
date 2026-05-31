from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "dataset" / "card_transdata.csv"

ARTIFACTS_DIR = PROJECT_ROOT / "app" / "data" / "artifacts"
DATASET_ARTIFACTS_DIR = ARTIFACTS_DIR / "dataset"
METRICS_ARTIFACTS_DIR = ARTIFACTS_DIR / "metrics"
MODELS_ARTIFACTS_DIR = ARTIFACTS_DIR / "models"

API_PREFIX = "/api"

CONTINUOUS_FEATURES = [
    "distance_from_home",
    "distance_from_last_transaction",
    "ratio_to_median_purchase_price",
]

BINARY_FEATURES = [
    "repeat_retailer",
    "used_chip",
    "used_pin_number",
    "online_order",
]

FEATURES = CONTINUOUS_FEATURES + BINARY_FEATURES

TARGET = "fraud"

FEATURE_DISPLAY_NAMES = {
    "distance_from_home": "Distancia de Casa",
    "distance_from_last_transaction": "Dist. Ultima Transacao",
    "ratio_to_median_purchase_price": "Razao ao Preco Mediano",
    "repeat_retailer": "Varejista Frequente",
    "used_chip": "Usou Chip",
    "used_pin_number": "Usou PIN",
    "online_order": "Compra Online",
    "fraud": "Fraude",
}

CORRELATION_LABELS = {
    "distance_from_home": "d_home",
    "distance_from_last_transaction": "d_last",
    "ratio_to_median_purchase_price": "ratio",
    "repeat_retailer": "rep_ret",
    "used_chip": "chip",
    "used_pin_number": "pin",
    "online_order": "online",
    "fraud": "fraud",
}

MODEL_METADATA = {
    "lda": ("LDA", "Linear Discriminant Analysis"),
    "qda": ("QDA", "Quadratic Discriminant Analysis"),
    "lr": ("Reg. Logistica", "Logistic Regression"),
    "rf": ("Random Forest", "Random Forest Classifier"),
}

