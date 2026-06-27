export default function BinaryChip({ value }) {
  const active = Number(value) === 1;
  return <span className={`binary-chip ${active ? 'is-active' : ''}`}>{active ? 'SIM' : 'NÃO'}</span>;
}
