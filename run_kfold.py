"""
Script para executar K-Fold e encontrar melhor n_sintetico
"""
import pandas as pd
from sklearn.model_selection import train_test_split

from ml.kfold_optimizer import KFoldOptimizer

# Carregar dados
print("Load Dataset")
df = pd.read_csv("dataset/card_transdata.csv")

# Features e target
COLUNAS_CONTINUAS = [
    "distance_from_home",
    "distance_from_last_transaction",
    "ratio_to_median_purchase_price"
]
COLUNAS_BINARIAS = [
    "repeat_retailer",
    "used_chip",
    "used_pin_number",
    "online_order"
]
TODAS_FEATURES = COLUNAS_CONTINUAS + COLUNAS_BINARIAS

# Train/Test split
X = df[TODAS_FEATURES].values
y = df["fraud"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=4267, stratify=y
)

print(f"Train: {X_train.shape[0]}, Test: {X_test.shape[0]}\n")

# K-Fold
modelos = ['LDA', 'QDA', 'Random Forest', 'Logistic Regression']
optimizer = KFoldOptimizer(X_train, y_train, n_splits=5)
resultados = optimizer.executar(modelos)
melhor_modelo, melhor_n_sintetico = optimizer.encontrar_melhor(resultados)

# Salvar resultado
print(f"Melhor config: {melhor_modelo} com n_sintetico={melhor_n_sintetico}")
