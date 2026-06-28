import {
  ArcElement,
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Filler,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Tooltip,
} from 'chart.js';

ChartJS.register(
  ArcElement,
  BarElement,
  CategoryScale,
  Filler,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Tooltip,
);

export const chartColors = {
  primary: '#2563eb',
  green: '#16a34a',
  red: '#dc2626',
  amber: '#d97706',
  violet: '#7c3aed',
  grid: 'rgba(17, 24, 39, 0.08)',
  text: '#374151',
};

export const baseOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: chartColors.text,
        boxWidth: 12,
        usePointStyle: true,
        font: { family: 'DM Sans' },
      },
    },
    tooltip: {
      backgroundColor: '#111827',
      titleColor: '#ffffff',
      bodyColor: '#ffffff',
      borderWidth: 0,
      padding: 10,
    },
  },
  scales: {
    x: {
      grid: { color: chartColors.grid },
      ticks: { color: chartColors.text, font: { family: 'DM Sans' } },
    },
    y: {
      grid: { color: chartColors.grid },
      ticks: { color: chartColors.text, font: { family: 'DM Sans' } },
    },
  },
};
