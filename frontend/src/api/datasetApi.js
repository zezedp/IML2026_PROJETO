import { apiGet } from './client';

export const getOverview = () => apiGet('/dataset/overview');
export const getStatistics = () => apiGet('/dataset/statistics');
export const getClassDistribution = () => apiGet('/dataset/class-distribution');
export const getSample = () => apiGet('/dataset/sample');
