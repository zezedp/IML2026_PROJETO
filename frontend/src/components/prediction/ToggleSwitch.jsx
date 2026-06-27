export default function ToggleSwitch({ label, icon, checked, onChange }) {
  return (
    <button
      type="button"
      className={`toggle ${checked ? 'is-on' : ''}`}
      onClick={() => onChange(!checked)}
      aria-pressed={checked}
    >
      <span className="toggle__icon" aria-hidden="true">{icon}</span>
      <span>{label}</span>
      <i />
    </button>
  );
}
