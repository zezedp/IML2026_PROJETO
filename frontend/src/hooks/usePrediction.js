import { useCallback, useEffect, useState } from 'react';
import { getScenarios, predictTransaction } from '../api/predictionApi';
import { DEFAULT_FEATURES } from '../utils/constants';

export function usePrediction() {
  const [features, setFeatures] = useState(DEFAULT_FEATURES);
  const [scenarios, setScenarios] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [predicting, setPredicting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    getScenarios()
      .then((payload) => {
        if (active) setScenarios(payload.scenarios || []);
      })
      .catch((err) => {
        if (active) setError(err);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    let active = true;
    const timer = window.setTimeout(() => {
      setPredicting(true);
      setError(null);
      predictTransaction(features)
        .then((payload) => {
          if (active) setResult(payload);
        })
        .catch((err) => {
          if (active) setError(err);
        })
        .finally(() => {
          if (active) setPredicting(false);
        });
    }, 300);

    return () => {
      active = false;
      window.clearTimeout(timer);
    };
  }, [features]);

  const updateFeature = useCallback((name, value) => {
    setFeatures((current) => ({ ...current, [name]: value }));
  }, []);

  const applyScenario = useCallback((scenario) => {
    if (scenario?.features) setFeatures(scenario.features);
  }, []);

  return {
    features,
    scenarios,
    result,
    loading,
    predicting,
    error,
    updateFeature,
    applyScenario,
  };
}
