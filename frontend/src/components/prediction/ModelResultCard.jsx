import { normalizeProbability } from '../../utils/formatters';

export default function ModelResultCard({ name, fullName, classification, isFraud, fraudProbability }) {
  const probability = normalizeProbability(fraudProbability);
  return (
    <article className={`model-card ${isFraud ? 'is-fraud' : 'is-legit'}`}>
      <div className="model-card__top">
        <strong>{name}</strong>
        <span>{fullName}</span>
      </div>
      <div className="model-card__result">
        <span>{classification}</span>
        <strong>{probability.toFixed(1)}%</strong>
      </div>
      <div className="risk-bar">
        <span style={{ width: `${Math.min(100, probability)}%` }} />
      </div>
    </article>
  );
}
