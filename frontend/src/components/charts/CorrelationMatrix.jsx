import ChartShell from './ChartShell';

export default function CorrelationMatrix({ labels = [], matrix = [] }) {
  const colorFor = (value) => {
    const abs = Math.abs(value);
    const alpha = Math.min(0.9, Math.max(0.08, abs));
    if (value > 0) return `rgba(37, 99, 235, ${alpha})`;
    if (value < 0) return `rgba(220, 38, 38, ${alpha})`;
    return 'rgba(107, 114, 128, 0.08)';
  };

  return (
    <ChartShell className="matrix-wrap" label="matriz de correlacao">
      <table className="matrix">
        <thead>
          <tr>
            <th />
            {labels.map((label) => (
              <th key={label}>{label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {matrix.map((row, rowIndex) => (
            <tr key={labels[rowIndex] || rowIndex}>
              <th>{labels[rowIndex]}</th>
              {row.map((value, columnIndex) => (
                <td
                  key={`${rowIndex}-${columnIndex}`}
                  style={{
                    backgroundColor: colorFor(value),
                    color: Math.abs(value) > 0.55 ? '#ffffff' : '#111827',
                  }}
                >
                  {Number(value).toFixed(2)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </ChartShell>
  );
}
