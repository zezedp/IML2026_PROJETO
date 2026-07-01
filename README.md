# FraudShield - Analise e Predicao de Fraudes

Projeto realizado para a disciplina de Introdução ao Aprendizado de Máquina, ministrada pelo professor Paulo Mann na Universidade Federal do Rio de Janeiro. Nosso trabalho teve como objetivo explorar, treinar, comparar e usar de maneira interativa modelos de classificação com o intuito de detectar fraudes em transações com cartão de crédito. O trabalho foi realizado pelos alunos Gabriel Martins, Guilherme Cappelli, Matheus Avila, Matheus Magalhães e Rafael Chaffin.

A aplicação é composta por uma API em FastAPI e uma interface em React/Vite. O backend carrega o dataset que está dividido em json e os modelos treinados; o frontend consome esses endpoints para exibir 4 telas: Visão Geral, Exploração, Predição Interativa e Comparação de Modelos.

## Funcionalidades

- Visão geral do dataset: total de transações, proporção de fraudes, estatísticas descritivas e amostra de registros.
- Exploração de dados: histogramas, quartis, matriz de correlação e proporção das features binárias por classe.
- Predição interativa: simulação de uma transação e resposta dos modelos treinados.
- Comparação de modelos: métricas, curvas ROC/PR, validação cruzada, matrizes de confusão e importância das features.
- API documentada em `/docs`.

## Modelos

O projeto compara quatro modelos:

- LDA - Linear Discriminant Analysis
- QDA - Quadratic Discriminant Analysis
- Regressão Logística
- Random Forest

As features usadas pelos modelos são:

- `distance_from_home`
- `distance_from_last_transaction`
- `ratio_to_median_purchase_price`
- `repeat_retailer`
- `used_chip`
- `used_pin_number`
- `online_order`

A variável alvo é `fraude`, em que `1` representa fraude e `0` representa transação legítima.

## Estrutura

```text
.
+-- app/                         # Backend FastAPI
|   +-- main.py                  # Entrada da API
|   +-- routers/                 # Rotas HTTP
|   +-- services/                # Regras de aplicação
|   +-- repositories/            # Carregamento de dataset, metricas e modelos
|   +-- schemas/                 # Schemas Pydantic
|   +-- ml/                      # Gerenciador de modelos para predição
|   +-- data/artifacts/          # Artefatos JSON e modelos PKL usados pela API
+-- frontend/                    # Interface React/Vite
|   +-- src/
|   +-- package.json
+-- dataset/
|   +-- card_transdata.csv       # Dataset base
+-- ml/                          # Código auxiliar de treinamento/experimentos
+-- Projeto.ipynb                # Notebook principal com as análises do projeto
+-- run_kfold.py                 # Experimentos de K-Fold
+-- requirements.txt             # Dependencias Python
```

## Requisitos

- Python 3.10+
- Node.js 18+
- npm

## Como Executar

### 1. Backend

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No terminal, execute:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Inicie a API:

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em:

```text
http://localhost:8000
```

Documentação interativa:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/api/health
```

### 2. Frontend

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

A interface ficará disponivel em:

```text
http://localhost:5173
```

Por padrão, o frontend consome a API em `http://localhost:8000/api`. Para usar outra URL, defina a variável:

```bash
VITE_API_URL=http://localhost:8000/api
```

## Endpoints Principais

### Dataset

- `GET /api/dataset/overview`
- `GET /api/dataset/statistics`
- `GET /api/dataset/class-distribution`
- `GET /api/dataset/sample`

### Exploracao

- `GET /api/exploration/histogram?feature=distance_from_home`
- `GET /api/exploration/boxplot?feature=distance_from_home`
- `GET /api/exploration/binary-features`
- `GET /api/exploration/correlation`

As features contínuas aceitas em `histogram` e `boxplot` sao:

- `distance_from_home`
- `distance_from_last_transaction`
- `ratio_to_median_purchase_price`

### Predição

- `GET /api/prediction/scenarios`
- `POST /api/prediction/predict`

Exemplo de payload:

```json
{
  "distance_from_home": 20,
  "distance_from_last_transaction": 5,
  "ratio_to_median_purchase_price": 2.5,
  "repeat_retailer": 1,
  "used_chip": 0,
  "used_pin_number": 0,
  "online_order": 1
}
```

### Modelos

- `GET /api/models/metrics`
- `GET /api/models/roc-curves`
- `GET /api/models/pr-curves`
- `GET /api/models/cross-validation`
- `GET /api/models/confusion-matrices`
- `GET /api/models/feature-importance`

## Artefatos

Os artefatos usados pela API ficam em `app/data/artifacts/`:

- `dataset/*.json`: estatísticas, distribuições, histogramas, boxplots e correlação.
- `metrics/*.json`: métricas, curvas, validação cruzada, matrizes de confusão e importância de features.
- `models/*.pkl`: modelos treinados carregados pelo backend.