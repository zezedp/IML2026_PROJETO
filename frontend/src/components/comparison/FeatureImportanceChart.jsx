import { formatDecimal } from '../../utils/formatters';

export default function FeatureImportanceChart({ features = [] }) {
  const max = Math.max(...features.map((feature) => feature.importance), 1);

  return (
    <div className="importance-list">
      {features.map((feature) => (
        <div className="importance" key={feature.name || feature.display_name}>
          <div className="importance__meta">
            <span>{feature.display_name}</span>
            <strong>{formatDecimal(feature.importance, 2)}%</strong>
          </div>
          <div className="importance__track">
            <span style={{ width: `${(feature.importance / max) * 100}%` }} />
          </div>
        </div>
      ))}
    </div>
  );
}
