export const SCREENS = [
  { id: 'overview', label: 'VISÃO GERAL' },
  { id: 'exploration', label: 'EXPLORAÇÃO' },
  { id: 'prediction', label: 'PREDIÇÃO INTERATIVA' },
  { id: 'comparison', label: 'COMPARAÇÃO DE MODELOS' },
];

export const CONTINUOUS_FEATURES = [
  'distance_from_home',
  'distance_from_last_transaction',
  'ratio_to_median_purchase_price',
];

export const BINARY_FEATURES = new Set([
  'repeat_retailer',
  'used_chip',
  'used_pin_number',
  'online_order',
]);

export const FEATURE_DISPLAY_NAMES = {
  distance_from_home: 'Distância de Casa',
  distance_from_last_transaction: 'Distância da Última Transação',
  ratio_to_median_purchase_price: 'Razão ao Preço Mediano',
  repeat_retailer: 'Varejista Frequente',
  used_chip: 'Usou Chip',
  used_pin_number: 'Usou PIN',
  online_order: 'Compra Online',
  fraud: 'Fraude',
};

export const FEATURE_SHORT_NAMES = {
  distance_from_home: 'Dist. Casa',
  distance_from_last_transaction: 'Dist. Última',
  ratio_to_median_purchase_price: 'Razão Preço',
};

export const MODEL_COLORS = {
  lda: '#0f766e',
  qda: '#dc2626',
  pca_qda: '#0891b2',
  lr: '#7c3aed',
  rf: '#d97706',
  random_forest: '#d97706',
  'reg._logística': '#7c3aed',
  'reg._logÃ­stica': '#7c3aed',
};

export const DEFAULT_FEATURES = {
  distance_from_home: 10,
  distance_from_last_transaction: 2,
  ratio_to_median_purchase_price: 1,
  repeat_retailer: 1,
  used_chip: 1,
  used_pin_number: 0,
  online_order: 0,
};

export const getFeatureType = (feature) => (BINARY_FEATURES.has(feature) ? 'Binária' : 'Contínua');
