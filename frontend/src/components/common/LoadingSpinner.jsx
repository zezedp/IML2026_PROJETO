export default function LoadingSpinner({ label = 'Carregando dados...' }) {
  return (
    <div className="state state--loading">
      <span className="spinner" />
      <p>{label}</p>
    </div>
  );
}
