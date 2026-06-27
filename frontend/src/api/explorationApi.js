import { apiGet } from './client';

export const getHistogram = (feature) => apiGet(`/exploration/histogram?feature=${feature}`);
export const getBoxplot = (feature) => apiGet(`/exploration/boxplot?feature=${feature}`);
export const getBinaryFeatures = () => apiGet('/exploration/binary-features');
export const getCorrelation = () => apiGet('/exploration/correlation');
