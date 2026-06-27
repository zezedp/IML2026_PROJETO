import { apiGet, apiPost } from './client';

export const getScenarios = () => apiGet('/prediction/scenarios');
export const predictTransaction = (features) => apiPost('/prediction/predict', features);
