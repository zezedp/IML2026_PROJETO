import { formatLargeNumber } from '../../utils/formatters';

export default function ConfusionMatrix({
  name,
  trueNegative,
  falsePositive,
  falseNegative,
  truePositive,
  isHighlighted = false,
}) {
  return (
    <article className={`confusion ${isHighlighted ? 'is-highlighted' : ''}`}>
      <h4>{name}</h4>
      <div className="confusion__grid">
        <div className="confusion__cell confusion__cell--good">
          <span>TN</span>
          <strong>{formatLargeNumber(trueNegative)}</strong>
        </div>
        <div className="confusion__cell confusion__cell--bad">
          <span>FP</span>
          <strong>{formatLargeNumber(falsePositive)}</strong>
        </div>
        <div className="confusion__cell confusion__cell--bad">
          <span>FN</span>
          <strong>{formatLargeNumber(falseNegative)}</strong>
        </div>
        <div className="confusion__cell confusion__cell--good">
          <span>TP</span>
          <strong>{formatLargeNumber(truePositive)}</strong>
        </div>
      </div>
    </article>
  );
}
