export const formatNumber = (value, maximumFractionDigits = 0) =>
  new Intl.NumberFormat('pt-BR', { maximumFractionDigits }).format(value ?? 0);

export const formatDecimal = (value, digits = 2) =>
  new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  }).format(value ?? 0);

export const formatPercent = (value, digits = 2) =>
  `${formatDecimal((value ?? 0) * 100, digits)}%`;

export const formatPercentValue = (value, digits = 2) =>
  `${formatDecimal(value ?? 0, digits)}%`;

export const formatLargeNumber = (value) => {
  const number = Number(value ?? 0);
  if (Math.abs(number) >= 1000) {
    return `${formatDecimal(number / 1000, 1)}k`;
  }
  return formatNumber(number);
};

export const normalizeProbability = (value) => {
  const number = Number(value ?? 0);
  return number > 1 ? number : number * 100;
};
