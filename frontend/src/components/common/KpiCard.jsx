export default function KpiCard({ label, value, subtitle, color = 'primary', delay = 0 }) {
  return (
    <article className={`kpi kpi--${color}`} style={{ animationDelay: `${delay}ms` }}>
      <span className="kpi__bar" />
      <p>{label}</p>
      <strong>{value}</strong>
      <small>{subtitle}</small>
    </article>
  );
}
