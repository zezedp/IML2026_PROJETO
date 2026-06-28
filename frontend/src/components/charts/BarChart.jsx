import { Bar } from 'react-chartjs-2';
import { baseOptions } from './chartConfig';

export default function BarChart({ labels, datasets, options = {} }) {
  return (
    <div className="chart-box">
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
    </div>
  );
}
