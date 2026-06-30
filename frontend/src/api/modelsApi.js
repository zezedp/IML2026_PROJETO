import { apiGet } from './client';

export const getMetrics = () => apiGet('/models/metrics');
export const getRocCurves = () => apiGet('/models/roc-curves');
export const getPrCurves = () => apiGet('/models/pr-curves');
export const getCrossValidation = () => apiGet('/models/cross-validation');
export const getConfusionMatrices = () => apiGet('/models/confusion-matrices');
export const getFeatureImportance = () => apiGet('/models/feature-importance');
