import { useEffect, useState } from 'react';
import { getBinaryFeatures, getBoxplot, getCorrelation, getHistogram } from '../api/explorationApi';
import BarChart from '../components/charts/BarChart';
import CorrelationMatrix from '../components/charts/CorrelationMatrix';
import Card from '../components/common/Card';
import ErrorMessage from '../components/common/ErrorMessage';
import InsightBox from '../components/common/InsightBox';
import LoadingSpinner from '../components/common/LoadingSpinner';
import SectionHeader from '../components/common/SectionHeader';
import { CONTINUOUS_FEATURES, FEATURE_DISPLAY_NAMES } from '../utils/constants';

export default function ExplorationPage() {
  const [selectedFeature, setSelectedFeature] = useState(CONTINUOUS_FEATURES[0]);
  const [staticData, setStaticData] = useState(null);
  const [dynamicData, setDynamicData] = useState(null);
  const [loadingStatic, setLoadingStatic] = useState(true);
  const [loadingDynamic, setLoadingDynamic] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    Promise.all([getBinaryFeatures(), getCorrelation()])
      .then(([binary, correlation]) => {
        if (active) setStaticData({ binary, correlation });
      })
      .catch((err) => {
        if (active) setError(err);
      })
      .finally(() => {
        if (active) setLoadingStatic(false);
      });
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    let active = true;
    setLoadingDynamic(true);
    Promise.all([getHistogram(selectedFeature), getBoxplot(selectedFeature)])
      .then(([histogram, boxplot]) => {
        if (active) setDynamicData({ histogram, boxplot });
      })
      .catch((err) => {
        if (active) setError(err);
      })
      .finally(() => {
        if (active) setLoadingDynamic(false);
      });
    return () => {
      active = false;
    };
  }, [selectedFeature]);

  if (loadingStatic && !staticData) return <LoadingSpinner />;
  if (error && !staticData && !dynamicData) return <ErrorMessage error={error} />;

  const histogram = dynamicData?.histogram;
  const boxplot = dynamicData?.boxplot;
  const binary = staticData?.binary;
  const correlation = staticData?.correlation;

  return (
    <>
      <SectionHeader
        title="EXPLORAÇÃO DE DADOS"
        description="Comparação visual entre transações legítimas e fraudulentas para entender padrões discriminativos."
      />

      <div className="grid grid--two">
        <Card title="Features Binárias">
          <BarChart
            labels={binary.display_names}
            datasets={[
              { label: 'Legítimas (%)', data: binary.legitimate, backgroundColor: 'rgba(37, 99, 235, 0.72)', borderRadius: 6 },
              { label: 'Fraudes (%)', data: binary.fraud, backgroundColor: 'rgba(220, 38, 38, 0.72)', borderRadius: 6 },
            ]}
          />
          <InsightBox variant="green">Compra online e uso de PIN apresentam forte separação entre as classes.</InsightBox>
        </Card>

        <Card title="Matriz de Correlação">
          <CorrelationMatrix labels={correlation.labels} matrix={correlation.matrix} />
          <InsightBox variant="primary">Células azuis indicam correlação positiva; vermelhas indicam correlação negativa.</InsightBox>
        </Card>
      </div>

      <div className="feature-selector">
        {CONTINUOUS_FEATURES.map((feature) => (
          <button
            key={feature}
            type="button"
            className={selectedFeature === feature ? 'is-active' : ''}
            onClick={() => setSelectedFeature(feature)}
          >
            {FEATURE_DISPLAY_NAMES[feature]}
          </button>
        ))}
      </div>

      {!loadingDynamic && histogram && (
        <InsightBox variant="primary">{histogram.insight}</InsightBox>
      )}

      <div className="grid grid--two">
        <Card title={`Histograma | ${FEATURE_DISPLAY_NAMES[selectedFeature]}`}>
          {loadingDynamic ? (
            <LoadingSpinner label="Atualizando gráfico..." />
          ) : (
            <BarChart
              labels={histogram.labels}
              datasets={[
                { label: 'Legítimas (%)', data: histogram.legitimate, backgroundColor: 'rgba(22, 163, 74, 0.75)', borderRadius: 6 },
                { label: 'Fraudes (%)', data: histogram.fraud, backgroundColor: 'rgba(220, 38, 38, 0.75)', borderRadius: 6 },
              ]}
            />
          )}
        </Card>

        <Card title={`Resumo por Quartis | ${FEATURE_DISPLAY_NAMES[selectedFeature]}`}>
          {loadingDynamic ? (
            <LoadingSpinner label="Atualizando quartis..." />
          ) : (
            <BarChart
              labels={['Q1', 'Mediana', 'Q3']}
              datasets={[
                {
                  label: 'Legítimas',
                  data: [boxplot.legitimate.q1, boxplot.legitimate.median, boxplot.legitimate.q3],
                  backgroundColor: 'rgba(22, 163, 74, 0.75)',
                  borderRadius: 6,
                },
                {
                  label: 'Fraudes',
                  data: [boxplot.fraud.q1, boxplot.fraud.median, boxplot.fraud.q3],
                  backgroundColor: 'rgba(220, 38, 38, 0.75)',
                  borderRadius: 6,
                },
              ]}
            />
          )}
        </Card>
      </div>
    </>
  );
}
