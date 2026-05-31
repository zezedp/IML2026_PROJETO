from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression as SklearnLogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class Model:    
    def __init__(self):
        self.modelo = None
    
    def treinar(self, X_train, y_train):
        self.modelo.fit(X_train, y_train)
    
    def predizer(self, X):
        return self.modelo.predict(X)
    
    def calcular_metricas(self, y_true, y_pred):
        return {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred),
            'recall': recall_score(y_true, y_pred),
            'f1': f1_score(y_true, y_pred),
        }


class LDA(Model):
    def __init__(self):
        super().__init__()
        self.modelo = LinearDiscriminantAnalysis()


class QDA(Model):
    def __init__(self):
        super().__init__()
        self.modelo = QuadraticDiscriminantAnalysis()


class RandomForest(Model):
    def __init__(self, n_estimators=100, max_depth=10):
        super().__init__()
        self.modelo = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=4267,
            n_jobs=-1
        )


class LogisticRegression(Model):
    def __init__(self, C=1.0, max_iter=1000):
        super().__init__()
        self.modelo = SklearnLogisticRegression(
            C=C,
            penalty='l2',
            solver='lbfgs',
            max_iter=max_iter,
            random_state=4267
        )


def criar_modelo(nome):
    """Factory"""
    modelos = {
        'LDA': LDA,
        'QDA': QDA,
        'Random Forest': RandomForest,
        'Logistic Regression': LogisticRegression,
    }
    
    return modelos[nome]()
