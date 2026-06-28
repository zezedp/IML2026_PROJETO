export default function ErrorMessage({ error }) {
  return (
    <div className="state state--error">
      <strong>Não foi possível carregar os dados.</strong>
      <p>{error?.message || 'Verifique se o backend está em execução.'}</p>
    </div>
  );
}
