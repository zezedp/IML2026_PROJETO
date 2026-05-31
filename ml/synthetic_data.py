"""
Geração de dados sintéticos para balanceamento de classes
"""
import numpy as np
import pandas as pd

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


def gerar_continuas(df_fraud, n_sintetico):
    """Gera features contínuas sintéticas"""
    X_cont = df_fraud[COLUNAS_CONTINUAS].values
    mu = X_cont.mean(axis=0)
    sigma = np.cov(X_cont, rowvar=False)
    
    rng = np.random.default_rng(seed=4267)
    X_cont_sintetico = rng.multivariate_normal(mu, sigma, size=n_sintetico)
    
    return X_cont_sintetico


def gerar_binarias(df_fraud, n_sintetico):
    """Gera features binárias sintéticas"""
    rng = np.random.default_rng(seed=4267)
    
    binarias_sinteticas = {}
    for col in COLUNAS_BINARIAS:
        p = df_fraud[col].mean()
        binarias_sinteticas[col] = rng.binomial(1, p, size=n_sintetico)
    
    return binarias_sinteticas


def balancear_treino(X_train, y_train, n_sintetico):
    """Balanceia treino com dados sintéticos"""
    todas_features = COLUNAS_CONTINUAS + COLUNAS_BINARIAS
    
    df_train = pd.DataFrame(X_train, columns=todas_features)
    df_train['fraud'] = y_train
    
    # Fraudulentos
    fraud_data = df_train[df_train['fraud'] == 1.0]
    
    # Gerar sintéticos
    X_cont_sint = gerar_continuas(fraud_data, n_sintetico)
    X_bin_sint = gerar_binarias(fraud_data, n_sintetico)
    
    # Montar DataFrame sintético
    df_sint = pd.DataFrame(X_cont_sint, columns=COLUNAS_CONTINUAS)
    for col in COLUNAS_BINARIAS:
        df_sint[col] = X_bin_sint[col]
    df_sint['fraud'] = 1.0
    
    # Concatenar
    df_balanceado = pd.concat([df_train, df_sint], ignore_index=True)
    
    X_balanceado = df_balanceado[todas_features].values
    y_balanceado = df_balanceado['fraud'].values
    
    return X_balanceado, y_balanceado
