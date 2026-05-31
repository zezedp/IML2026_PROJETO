# Interface Visual — Dashboard de Detecção de Fraude em Cartão de Crédito

---

## Tela 1 — Visão Geral do Dataset

### Propósito
Dar ao usuário uma fotografia instantânea do problema. Em segundos, qualquer pessoa — técnica ou não — deve entender a escala do dataset e a gravidade do desbalanceamento entre transações legítimas e fraudulentas.

### O que é exibido

**Indicadores principais (topo da tela)**
Quatro números de destaque: o total de transações no dataset, a quantidade de transações legítimas, a quantidade de transações fraudulentas, e a taxa percentual de fraude. Esses números comunicam imediatamente que o problema é desbalanceado — fraudes representam uma minoria pequena do total.

**Distribuição das classes**
Um gráfico de pizza ou rosca mostrando visualmente a proporção entre transações legítimas e fraudulentas. O objetivo é evidenciar o desbalanceamento de forma intuitiva — a fatia das fraudes é pequena, o que justifica toda a estratégia de balanceamento aplicada no projeto.

**Estatísticas descritivas das features**
Uma tabela resumindo as características de cada variável do dataset: valores mínimos, máximos, médias e desvios padrão. Isso permite ao usuário entender a natureza de cada feature antes de explorá-las em profundidade.

**Amostra dos dados**
Uma prévia das primeiras linhas do dataset, mostrando como os dados brutos se parecem — cada transação com seus 7 atributos e o rótulo de fraude ou não fraude.

---

## Tela 2 — Exploração de Dados

### Propósito
Deixar o usuário investigar cada feature individualmente e entender como ela se relaciona com a presença de fraude. A ideia central é revelar os **padrões que os modelos aprendem** — tornando o problema mais tangível e compreensível antes de apresentar os resultados dos classificadores.

### O que é exibido

**Seletor de feature**
Um menu dropdown no topo da tela. Ao selecionar qualquer uma das 7 features, todos os gráficos abaixo se atualizam automaticamente para mostrar informações sobre aquela feature específica.

**Distribuição por classe**
Para features contínuas, um histograma mostrando, em sobreposição, a distribuição dos valores para transações legítimas (verde) e fraudulentas (vermelho). O insight esperado é que fraudes tendem a ocorrer com distâncias maiores de casa e valores de compra fora do padrão do cliente.

**Boxplot por classe**
Um boxplot comparando os quartis da feature selecionada entre as duas classes. Permite identificar visualmente onde estão os outliers de cada grupo e como as medianas diferem.

**Proporção das features binárias**
Para as quatro features binárias do dataset, um gráfico de barras agrupadas mostrando a taxa de ocorrência de cada feature (ex.: "usou chip", "compra online") separada por classe. O padrão esperado é que fraudes concentrem-se em transações online, sem uso de chip e sem uso de PIN.

**Matriz de correlação**
Um mapa de calor mostrando a correlação entre todas as features e o alvo. Permite identificar rapidamente quais variáveis têm relação mais forte com fraude — e quais são redundantes entre si.

---

## Tela 3 — Predição Interativa

### Propósito
Ser a tela mais impactante do dashboard. O usuário simula uma transação do zero, ajustando os valores de cada atributo, e vê **em tempo real** o que cada modelo prediz. O objetivo é tornar o comportamento dos classificadores concreto e demonstrável — ideal para apresentações.

### O que é exibido

**Formulário de entrada (lado esquerdo)**
Controles para cada uma das 7 features:

- *Distância de casa*: um slider deslizante representando quantos quilômetros a transação ocorreu longe da residência do cliente.
- *Distância da última transação*: slider representando a distância geográfica em relação à transação anterior do cliente.
- *Razão ao preço mediano*: slider representando se o valor da compra é maior ou menor que o padrão histórico do cliente. Valores acima de 1 significam compras mais caras que o habitual.
- *Varejista frequente*: toggle (ligado/desligado) indicando se o cliente já comprou nesse estabelecimento antes.
- *Usou chip*: toggle indicando se a transação foi feita com o chip físico do cartão.
- *Usou PIN*: toggle indicando se a senha numérica foi digitada.
- *Compra online*: toggle indicando se a transação foi realizada pela internet.

**Cenários pré-definidos**
Três botões de atalho que preenchem automaticamente o formulário com situações típicas: uma transação claramente legítima, uma fraude óbvia, e um caso ambíguo. Isso facilita demonstrações e permite comparar rapidamente como os modelos se comportam em extremos e em situações de incerteza.

**Resultados dos modelos (lado direito)**
Quatro cartões de resultado — um para cada modelo (LDA, QDA, Regressão Logística e Random Forest). Cada cartão mostra:
- O nome do modelo
- A predição: "FRAUDE" (em vermelho, com alerta) ou "LEGÍTIMA" (em verde, com confirmação)
- O percentual de confiança naquela predição
- Uma barra visual indicando o nível de risco de 0% a 100%

Os resultados atualizam instantaneamente a cada ajuste feito no formulário, tornando a interação fluida e educativa.

---

## Tela 4 — Comparação de Modelos

### Propósito
Apresentar a avaliação rigorosa e científica dos modelos treinados. Aqui o foco sai da interatividade e vai para a **análise de desempenho** — respondendo à pergunta: qual modelo é melhor, em que contexto, e por quê?

### O que é exibido

**Tabela de métricas**
Uma tabela comparando os 4 modelos em 5 métricas: acurácia, precisão, recall, F1-Score e AUC-ROC. O melhor valor em cada coluna é destacado visualmente. Essa tabela é o ponto de partida para toda a discussão sobre qual modelo escolher — dependendo se o objetivo é minimizar falsos positivos (bloquear cartões indevidamente) ou falsos negativos (deixar fraudes passarem).

**Curvas ROC**
Um único gráfico com as 4 curvas ROC sobrepostas, cada uma em uma cor diferente, com o valor de AUC na legenda. Quanto mais próxima a curva do canto superior esquerdo, melhor o modelo. A linha diagonal de referência representa um classificador aleatório. Esse gráfico revela o desempenho em **todos os thresholds possíveis** — não apenas no threshold padrão de 50%.

**Matrizes de confusão**
Quatro matrizes lado a lado, uma por modelo. Cada matriz é um quadrado 2×2 mostrando: quantas transações legítimas foram corretamente identificadas (verdadeiros negativos), quantas fraudes foram corretamente detectadas (verdadeiros positivos), quantas legítimas foram incorretamente bloqueadas como fraude (falsos positivos), e quantas fraudes passaram despercebidas (falsos negativos). Essa visualização conecta diretamente as métricas ao impacto real no mundo: um falso positivo é um cliente com cartão bloqueado sem motivo; um falso negativo é uma fraude que custou dinheiro.

**Importância das features**
Um gráfico de barras horizontais mostrando quais das 7 features mais influenciaram as predições do modelo de Random Forest. As barras são ordenadas da feature mais importante para a menos importante. Isso responde à pergunta: **o que mais importa para detectar uma fraude?** — e abre espaço para a discussão sobre interpretabilidade e viés.

**Resultados da validação cruzada**
Um boxplot mostrando a variação do F1-Score em 5 rodadas de validação cruzada para cada modelo. Indica se os modelos são estáveis ou se performam bem apenas em condições específicas.
