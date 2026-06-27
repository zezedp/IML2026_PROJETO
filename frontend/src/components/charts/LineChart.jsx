import { Line } from 'react-chartjs-2';
import { baseOptions } from './chartConfig';

export default function LineChart({ datasets, labels, options = {} }) {
  return (
    <div className="chart-box">
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
    </div>
  );
}
