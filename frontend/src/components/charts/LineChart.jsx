import { Line } from 'react-chartjs-2';
import { baseOptions } from './chartConfig';
import ChartShell from './ChartShell';

export default function LineChart({ datasets, labels, options = {} }) {
  return (
    <ChartShell label="grafico de linhas">
      <Line
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
