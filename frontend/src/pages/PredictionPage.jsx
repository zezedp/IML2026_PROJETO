import Card from '../components/common/Card';
import ErrorMessage from '../components/common/ErrorMessage';
import LoadingSpinner from '../components/common/LoadingSpinner';
import SectionHeader from '../components/common/SectionHeader';
import ModelResultCard from '../components/prediction/ModelResultCard';
import RiskSummary from '../components/prediction/RiskSummary';
import SliderInput from '../components/prediction/SliderInput';
import ToggleSwitch from '../components/prediction/ToggleSwitch';
import { usePrediction } from '../hooks/usePrediction';

const SLIDERS = [
  {
    key: 'distance_from_home',
    label: 'Distância de Casa',
    description: 'Distância relativa até o endereço usual',
    min: 0,
    max: 300,
    step: 1,
    decimalPlaces: 0,
  },
  {
    key: 'distance_from_last_transaction',
    label: 'Distância da Última Transação',
    description: 'Separação da compra anterior',
    min: 0,
    max: 120,
    step: 0.5,
    decimalPlaces: 1,
  },
  {
    key: 'ratio_to_median_purchase_price',
    label: 'Razão ao Preço Mediano',
    description: 'Valor comparado ao padrão histórico',
    min: 0,
    max: 12,
    step: 0.1,
    decimalPlaces: 1,
  },
];

const TOGGLES = [
  { key: 'repeat_retailer', label: 'Varejista Frequente', icon: 'R' },
  { key: 'used_chip', label: 'Usou Chip', icon: 'C' },
  { key: 'used_pin_number', label: 'Usou PIN', icon: 'P' },
  { key: 'online_order', label: 'Compra Online', icon: 'O' },
];

export default function PredictionPage() {
  const {
    features,
    scenarios,
    result,
    loading,
    error,
    updateFeature,
    applyScenario,
  } = usePrediction();

  if (loading) return <LoadingSpinner label="Carregando cenários..." />;

  return (
    <>
      <SectionHeader
        title="PREDIÇÃO INTERATIVA"
        description="Simule uma transação e veja a resposta dos modelos carregados."
      />

      {error && <ErrorMessage error={error} />}

      <div className="scenario-row">
        {scenarios.map((scenario) => (
          <button
            key={scenario.id}
            type="button"
            className={`scenario scenario--${scenario.style || 'primary'}`}
            onClick={() => applyScenario(scenario)}
          >
            {scenario.label}
          </button>
        ))}
      </div>

      <div className="prediction-layout">
        <Card>
          <div className="form-section">
            <h3>Features Contínuas</h3>
            {SLIDERS.map((slider) => (
              <SliderInput
                key={slider.key}
                {...slider}
                value={features[slider.key]}
                onChange={(value) => updateFeature(slider.key, value)}
              />
            ))}
          </div>

          <div className="form-section">
            <h3>Features Binárias</h3>
            <div className="toggle-grid">
              {TOGGLES.map((toggle) => (
                <ToggleSwitch
                  key={toggle.key}
                  {...toggle}
                  checked={Number(features[toggle.key]) === 1}
                  onChange={(checked) => updateFeature(toggle.key, checked ? 1 : 0)}
                />
              ))}
            </div>
          </div>
        </Card>

        <div className="prediction-results">
          <div className="model-grid">
            {result?.models ? (
              Object.entries(result.models).map(([id, model]) => (
                <ModelResultCard
                  key={id}
                  name={model.name}
                  fullName={model.full_name}
                  classification={model.classification}
                  isFraud={model.is_fraud}
                  fraudProbability={model.fraud_probability}
                />
              ))
            ) : (
              <LoadingSpinner label="Calculando predição..." />
            )}
          </div>

          <Card title="Resumo de Risco Agregado">
            <RiskSummary
              averageProbability={result?.aggregate?.average_probability}
              fraudVotes={result?.aggregate?.fraud_votes}
              totalModels={result?.aggregate?.total_models}
              consensus={result?.aggregate?.consensus}
              consensusMessage={result?.aggregate?.consensus_message}
              riskLevel={result?.aggregate?.risk_level}
            />
          </Card>
        </div>
      </div>
    </>
  );
}
