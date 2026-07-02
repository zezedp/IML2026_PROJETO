import { useEffect, useMemo, useState } from 'react';
import {
  getConfusionMatrices,
  getCrossValidation,
  getFeatureImportance,
  getMetrics,
  getPrCurves,
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

const CURVE_LINE_STYLES = {
  lda: [],
  qda: [8, 5],
  pca_qda: [2, 4],
  lr: [3, 4],
  rf: [12, 5, 3, 5],
};

const CURVE_DRAW_ORDER = {
  pca_qda: 2,
  qda: 1,
};

const MODEL_LEGEND_ORDER = ['lda', 'qda', 'pca_qda', 'rf', 'lr'];

const CURVE_ID_ALIASES = {
  random_forest: 'rf',
  'reg._logística': 'lr',
};

const normalizeCurveId = (id) => CURVE_ID_ALIASES[id] || id;

const getCurveColor = (id) => MODEL_COLORS[id] || MODEL_COLORS[normalizeCurveId(id)] || '#2563eb';

const getModelOrder = (id) => {
  const order = MODEL_LEGEND_ORDER.indexOf(normalizeCurveId(id));
  return order === -1 ? MODEL_LEGEND_ORDER.length : order;
};

const formatCurveLabel = (label) => label.replace(/\s*\((?:AUC|AP)=[^)]+\)/g, '');

const buildCurveDatasets = ({ models, metrics, xKey, yKey }) => (
  Object.entries(models).map(([id, model]) => {
    const normalizedId = normalizeCurveId(id);
    const color = getCurveColor(id);

    return {
      label: formatCurveLabel(model.label),
      data: model.points
        .map((point) => ({ x: point[xKey], y: point[yKey] }))
        .sort((a, b) => a.x - b.x),
      borderColor: color,
      backgroundColor: color,
      borderDash: CURVE_LINE_STYLES[normalizedId] || [],
      borderWidth: normalizedId === 'pca_qda' ? 5 : normalizedId === metrics.best_model ? 3.25 : 2.25,
      order: CURVE_DRAW_ORDER[normalizedId] || 0,
      pointRadius: 0,
      stepped: true,
      tension: 0,
    };
  })
);

export default function ComparisonPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    Promise.all([
      getMetrics(),
      getRocCurves(),
      getPrCurves(),
      getCrossValidation(),
      getConfusionMatrices(),
      getFeatureImportance(),
    ])
      .then(([metrics, roc, pr, crossValidation, confusion, importance]) => {
        if (active) setData({ metrics, roc, pr, crossValidation, confusion, importance });
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

  const rocDatasets = buildCurveDatasets({
    models: data.roc.models,
    metrics: data.metrics,
    xKey: 'fpr',
    yKey: 'tpr',
  });

  const prDatasets = buildCurveDatasets({
    models: data.pr.models,
    metrics: data.metrics,
    xKey: 'recall',
    yKey: 'precision',
  });

  const curveLabels = Object.entries(data.roc.models).reduce((acc, [id, model]) => {
    acc[normalizeCurveId(id)] = formatCurveLabel(model.label);
    return acc;
  }, {});

  const cvDatasets = Object.entries(data.crossValidation.models)
    .sort(([firstId], [secondId]) => (
      getModelOrder(firstId) - getModelOrder(secondId)
    ))
    .map(([id, model]) => ({
      label: curveLabels[normalizeCurveId(id)] || id.toUpperCase(),
      data: model.scores,
      borderColor: getCurveColor(id),
      backgroundColor: getCurveColor(id),
      pointRadius: 4,
      borderWidth: 2,
      tension: 0.25,
    }));

  return (
    <>
      <SectionHeader
        title="COMPARAÇÃO DE MODELOS"
        description="Métricas, estabilidade e leitura operacional dos modelos treinados."
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

      <div className="grid grid--two comparison-curves">
        <Card title="Curvas ROC">
          <LineChart
            datasets={rocDatasets}
            options={{
              parsing: false,
              interaction: { mode: 'nearest', intersect: false },
              scales: {
                x: { type: 'linear', min: 0, max: 0.08, title: { display: true, text: 'FPR' } },
                y: { min: 0.65, max: 1, title: { display: true, text: 'TPR' } },
              },
            }}
          />
        </Card>

        <Card title="Curvas PR">
          <LineChart
            datasets={prDatasets}
            options={{
              parsing: false,
              interaction: { mode: 'nearest', intersect: false },
              scales: {
                x: { type: 'linear', min: 0, max: 1, title: { display: true, text: 'Recall' } },
                y: { min: 0, max: 1, title: { display: true, text: 'Precision' } },
              },
            }}
          />
        </Card>

      </div>

      <div className="grid grid--two">

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

        <Card title={`Importância das Features | ${data.importance.model}`}>
          <FeatureImportanceChart features={data.importance.features} />
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

    </>
  );
}
