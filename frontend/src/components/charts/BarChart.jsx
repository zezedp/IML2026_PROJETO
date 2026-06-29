import { Bar } from 'react-chartjs-2';
import { baseOptions } from './chartConfig';
import ChartShell from './ChartShell';

export default function BarChart({ labels, datasets, options = {} }) {
  return (
    <ChartShell label="grafico de barras">
      <Bar
        data={{ labels, datasets }}
        options={{
          ...baseOptions,
          ...options,
          scales: {
            ...baseOptions.scales,
            ...(options.scales || {}),
          },
        }}
      />
    </ChartShell>
  );
}
