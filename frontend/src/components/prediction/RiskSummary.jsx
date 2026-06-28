import { normalizeProbability } from '../../utils/formatters';

export default function RiskSummary({
  averageProbability = 0,
  fraudVotes = 0,
  totalModels = 4,
  consensus = 'Indefinido',
  consensusMessage = 'Aguardando predição.',
  riskLevel = 'low',
}) {
  const probability = normalizeProbability(averageProbability);
  return (
    <div className={`risk-summary risk-summary--${riskLevel}`}>
      <div className="risk-summary__top">
        <div>
          <span>Probabilidade média</span>
          <strong>{probability.toFixed(1)}%</strong>
        </div>
        <div>
          <span>Votos de fraude</span>
          <strong>{fraudVotes}/{totalModels}</strong>
        </div>
      </div>
      <div className="risk-bar risk-bar--large">
        <span style={{ width: `${Math.min(100, probability)}%` }} />
      </div>
      <h4>{consensus}</h4>
      <p>{consensusMessage}</p>
    </div>
  );
}
