import { useEffect, useMemo, useState } from 'react';
import {
  getConfusionMatrices,
  getCrossValidation,
  getFeatureImportance,
  getMetrics,
  getRocCurves,
} from '../api/modelsApi';
import LineChart from '../components/charts/LineChart';
import Card from '../components/common/Card';
import ErrorMessage from '../components/common/ErrorMessage';
import InsightBox from '../components/common/InsightBox';
import LoadingSpinner from '../components/common/LoadingSpinner';
import SectionHeader from '../components/common/SectionHeader';
import ConfusionMatrix from '../components/comparison/ConfusionMatrix';
import FeatureImportanceChart from '../components/comparison/FeatureImportanceChart';
import { MODEL_COLORS } from '../utils/constants';
import { formatDecimal, formatNumber, formatPercent } from '../utils/formatters';

const METRIC_KEYS = ['accuracy', 'precision', 'recall', 'f1_score', 'auc_roc'];
const METRIC_LABELS = {
  accuracy: 'Acurácia',
  precision: 'Precisão',
  recall: 'Recall',
  f1_score: 'F1-score',
  auc_roc: 'AUC-ROC',
};

export default function ComparisonPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    Promise.all([
      getMetrics(),
      getRocCurves(),
      getCrossValidation(),
      getConfusionMatrices(),
      getFeatureImportance(),
    ])
      .then(([metrics, roc, crossValidation, confusion, importance]) => {
        if (active) setData({ metrics, roc, crossValidation, confusion, importance });
      })
      .catch((err) => {
        if (active) setError(err);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  const metricRanks = useMemo(() => {
    if (!data?.metrics?.models) return {};
    return METRIC_KEYS.reduce((acc, metric) => {
      acc[metric] = [...data.metrics.models]
        .sort((a, b) => b[metric] - a[metric])
        .map((model) => model.id);
      return acc;
    }, {});
  }, [data]);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  const rocDatasets = Object.entries(data.roc.models).map(([id, model]) => ({
    label: model.label,
    data: model.points.map((point) => ({ x: point.fpr, y: point.tpr })),
    borderColor: MODEL_COLORS[id] || '#2563eb',
    backgroundColor: MODEL_COLORS[id] || '#2563eb',
    pointRadius: 0,
    borderWidth: id === data.metrics.best_model ? 3 : 2,
    tension: 0.15,
  }));

  const cvDatasets = Object.entries(data.crossValidation.models).map(([id, model]) => ({
    label: id.toUpperCase(),
    data: model.scores,
    borderColor: MODEL_COLORS[id] || '#2563eb',
    backgroundColor: MODEL_COLORS[id] || '#2563eb',
    pointRadius: 4,
    borderWidth: 2,
    tension: 0.25,
  }));

  return (
    <>
      <SectionHeader
        title="COMPARAÇÃO DE MODELOS"
        description="Métricas, estabilidade e leitura operacional dos quatro modelos treinados."
      />

      <Card title="Métricas Comparativas">
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Modelo</th>
                {METRIC_KEYS.map((metric) => <th key={metric}>{METRIC_LABELS[metric]}</th>)}
              </tr>
            </thead>
            <tbody>
              {data.metrics.models.map((model) => (
                <tr key={model.id} className={model.is_best ? 'is-best-row' : ''}>
                  <td>
                    <strong>{model.name}</strong>
                    <span className="subtle">{model.full_name}</span>
                  </td>
                  {METRIC_KEYS.map((metric) => {
                    const rank = metricRanks[metric]?.indexOf(model.id);
                    return (
                      <td key={metric} className={rank === 0 ? 'metric-best' : rank === 1 ? 'metric-second' : ''}>
                        {formatPercent(model[metric])}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      <div className="grid grid--two">
        <Card title="Curvas ROC">
          <LineChart
            datasets={rocDatasets}
            options={{
              parsing: false,
              scales: {
                x: { type: 'linear', min: 0, max: 1, title: { display: true, text: 'FPR' } },
                y: { min: 0, max: 1, title: { display: true, text: 'TPR' } },
              },
            }}
          />
        </Card>

        <Card title="Validação Cruzada">
          <LineChart labels={data.crossValidation.folds.map((fold) => `Fold ${fold}`)} datasets={cvDatasets} />
          <div className="table-wrap table-wrap--compact">
            <table>
              <thead>
                <tr>
                  <th>Modelo</th>
                  <th>Média</th>
                  <th>Desvio</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(data.crossValidation.models).map(([id, model]) => (
                  <tr key={id}>
                    <td>{id.toUpperCase()}</td>
                    <td>{formatDecimal(model.mean, 4)}</td>
                    <td>{formatDecimal(model.std, 4)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>

      <Card title={`Matrizes de Confusão | Teste com ${formatNumber(data.confusion.test_size)} transações`}>
        <div className="confusion-grid">
          {Object.entries(data.confusion.models).map(([id, model]) => (
            <ConfusionMatrix
              key={id}
              name={model.name}
              trueNegative={model.true_negative}
              falsePositive={model.false_positive}
              falseNegative={model.false_negative}
              truePositive={model.true_positive}
              isHighlighted={id === data.metrics.best_model}
            />
          ))}
        </div>
      </Card>

      <div className="grid grid--two">
        <Card title={`Importância das Features | ${data.importance.model}`}>
          <FeatureImportanceChart features={data.importance.features} />
        </Card>

        <Card title="Qualidade, Limitações e Ética">
          <div className="ethics">
            <h4>Qualidade</h4>
            <p>O Random Forest se destaca por capturar relações não lineares e interações entre features, especialmente razão de preço, compra online e uso de PIN.</p>
            <h4>Limitações</h4>
            <p>Modelos de fraude dependem de monitoramento contínuo. Mudanças de comportamento e novas estratégias de ataque podem reduzir desempenho com o tempo.</p>
            <h4>Reflexão Ética</h4>
            <p>A predição deve apoiar revisão e priorização, não substituir decisões finais. Falsos positivos afetam clientes legítimos; falsos negativos aumentam perdas financeiras.</p>
          </div>
        </Card>
      </div>
    </>
  );
}
