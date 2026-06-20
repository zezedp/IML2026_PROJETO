"""
Script para executar K-Fold e encontrar melhor n_sintetico
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from ml.kfold_optimizer import KFoldOptimizer
from ml.synthetic_data import balancear_treino

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

# ==================== TESTE DO PCA+QDA ====================
print("\n" + "="*70)
print("TESTANDO PCA+QDA COM DIFERENTES NÚMEROS DE COMPONENTES")
print("="*70)

from ml.models import PCA_QDA

# Testar diferentes números de componentes
n_components_list = [2, 3, 4, 5, 6, 7]

for n_comp in n_components_list:
    print(f"\n▶ Testando PCA+QDA com n_components={n_comp}")
    
    f1_scores = []
    acc_scores = []
    
    fold_num = 1
    for train_idx, val_idx in optimizer.skf.split(X_train, y_train):
        X_fold_train, X_fold_val = X_train[train_idx], X_train[val_idx]
        y_fold_train, y_fold_val = y_train[train_idx], y_train[val_idx]
        
        # Balancear treino do fold
        X_fold_train_bal, y_fold_train_bal = balancear_treino(
            X_fold_train, y_fold_train, melhor_n_sintetico
        )
        
        # Treinar PCA+QDA
        modelo_pca_qda = PCA_QDA(n_components=n_comp)
        modelo_pca_qda.treinar(X_fold_train_bal, y_fold_train_bal)
        
        # Predizer
        y_fold_pred = modelo_pca_qda.predizer(X_fold_val)
        metricas = modelo_pca_qda.calcular_metricas(y_fold_val, y_fold_pred)
        
        f1_scores.append(metricas['f1'])
        acc_scores.append(metricas['accuracy'])
        
        fold_num += 1
    
    # Médias
    f1_mean = np.mean(f1_scores)
    acc_mean = np.mean(acc_scores)
    
    print(f"  F1: {f1_mean:.4f}, Acc: {acc_mean:.4f}")

print("\n" + "="*70)
print("✓ Teste do PCA+QDA finalizado!")
print("="*70)
