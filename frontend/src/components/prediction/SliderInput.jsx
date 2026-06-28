import { formatDecimal } from '../../utils/formatters';

export default function SliderInput({
  label,
  description,
  value,
  min,
  max,
  step,
  decimalPlaces = 1,
  onChange,
}) {
  return (
    <label className="slider-field">
      <div className="slider-field__top">
        <span>
          <strong>{label}</strong>
          <small>{description}</small>
        </span>
        <em>{formatDecimal(value, decimalPlaces)}</em>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(event) => onChange(Number(event.target.value))}
      />
    </label>
  );
}
