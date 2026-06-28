import { useState } from 'react';
import MainLayout from './components/layout/MainLayout';
import ComparisonPage from './pages/ComparisonPage';
import ExplorationPage from './pages/ExplorationPage';
import OverviewPage from './pages/OverviewPage';
import PredictionPage from './pages/PredictionPage';

export default function App() {
  const [activeScreen, setActiveScreen] = useState('overview');

  return (
    <MainLayout activeScreen={activeScreen} onNavigate={setActiveScreen}>
      <section className={`screen ${activeScreen === 'overview' ? 'is-active' : ''}`}>
        <OverviewPage />
      </section>
      <section className={`screen ${activeScreen === 'exploration' ? 'is-active' : ''}`}>
        <ExplorationPage />
      </section>
      <section className={`screen ${activeScreen === 'prediction' ? 'is-active' : ''}`}>
        <PredictionPage />
      </section>
      <section className={`screen ${activeScreen === 'comparison' ? 'is-active' : ''}`}>
        <ComparisonPage />
      </section>
    </MainLayout>
  );
}
