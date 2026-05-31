import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold

from ml.synthetic_data import balancear_treino
from ml.models import criar_modelo


class KFoldOptimizer:    
    def __init__(self, X_train, y_train, n_splits=5):
        self.X_train = X_train
        self.y_train = y_train
        self.skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=4267)
        
        # Calcular candidatos de n_sintetico
        n_fraudes = (y_train == 1).sum()
        n_legitimas = (y_train == 0).sum()
        n_desequilibrio = abs(n_legitimas - n_fraudes)
        
        self.n_sintetico_candidates = [
            int(n_desequilibrio // div) for div in [1.0, 1.5, 2.0, 2.5, 3.0]
        ]
        
        print(f"Candidatos de n_sintetico: {self.n_sintetico_candidates}\n")
    
    def executar(self, modelos_nomes):
        resultados = {}
        
        for modelo_nome in modelos_nomes:
            print(f"MODELO: {modelo_nome}")
            
            for n_sint in self.n_sintetico_candidates:
                print(f"\n  n_sintetico = {n_sint}")
                
                # K-Fold para esta comb
                f1_scores = []
                acc_scores = []
                
                fold_num = 1
                for train_idx, val_idx in self.skf.split(self.X_train, self.y_train):
                    X_fold_train, X_fold_val = self.X_train[train_idx], self.X_train[val_idx]
                    y_fold_train, y_fold_val = self.y_train[train_idx], self.y_train[val_idx]
                    
                    # Balancear treino do fold
                    X_fold_train_bal, y_fold_train_bal = balancear_treino(
                        X_fold_train, y_fold_train, n_sint
                    )
                    
                    # Treinar modelo
                    modelo = criar_modelo(modelo_nome)
                    modelo.treinar(X_fold_train_bal, y_fold_train_bal)
                    
                    # Predizer
                    y_fold_pred = modelo.predizer(X_fold_val)
                    metricas = modelo.calcular_metricas(y_fold_val, y_fold_pred)
                    
                    f1_scores.append(metricas['f1'])
                    acc_scores.append(metricas['accuracy'])
                    
                    fold_num += 1
                
                # Médias
                f1_mean = np.mean(f1_scores)
                acc_mean = np.mean(acc_scores)
                
                chave = (modelo_nome, n_sint)
                resultados[chave] = {
                    'f1_scores': f1_scores,
                    'acc_scores': acc_scores,
                    'f1_mean': f1_mean,
                    'acc_mean': acc_mean,
                }
                
                print(f"    F1: {f1_mean:.4f}, Acc: {acc_mean:.4f}")
        
        return resultados
    
    def encontrar_melhor(self, resultados):
        melhor_chave = max(resultados.keys(), key=lambda k: resultados[k]['f1_mean'])
        modelo_nome, n_sint = melhor_chave
        
        print(f"\n\n{' '*70}")
        print(f"MELHOR CONFIGURAÇÃO:")
        print(f"  Modelo: {modelo_nome}")
        print(f"  n_sintetico: {n_sint}")
        print(f"  F1-Score: {resultados[melhor_chave]['f1_mean']:.4f}")
        print(f"{' '*70}")
        
        return modelo_nome, n_sint
