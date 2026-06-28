import { Doughnut } from 'react-chartjs-2';
import './chartConfig';
import { formatPercentValue } from '../../utils/formatters';
import ChartShell from './ChartShell';

export default function DonutChart({ labels, data, colors, centerLabel }) {
  const chartData = {
    labels,
    datasets: [
      {
        data,
        backgroundColor: colors,
        borderColor: '#ffffff',
        borderWidth: 4,
        hoverOffset: 6,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '70%',
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (context) => `${context.label}: ${formatPercentValue(context.parsed, 2)}`,
        },
      },
    },
  };

  return (
    <ChartShell className="donut" label="grafico de rosca">
      <Doughnut data={chartData} options={options} />
      <div className="donut__center">
        <strong>{centerLabel}</strong>
        <span>fraude</span>
      </div>
    </ChartShell>
  );
}
