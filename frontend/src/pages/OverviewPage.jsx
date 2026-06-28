import { useEffect, useState } from 'react';
import { getClassDistribution, getOverview, getSample, getStatistics } from '../api/datasetApi';
import Badge from '../components/common/Badge';
import BinaryChip from '../components/common/BinaryChip';
import Card from '../components/common/Card';
import ErrorMessage from '../components/common/ErrorMessage';
import InsightBox from '../components/common/InsightBox';
import KpiCard from '../components/common/KpiCard';
import LoadingSpinner from '../components/common/LoadingSpinner';
import SectionHeader from '../components/common/SectionHeader';
import DonutChart from '../components/charts/DonutChart';
import { FEATURE_DISPLAY_NAMES, getFeatureType } from '../utils/constants';
import { formatDecimal, formatNumber, formatPercent, formatPercentValue } from '../utils/formatters';


const formatStatistic = (feature, statistic, value) => {
  const number = Number(value ?? 0);
  const shouldShowMorePrecision = statistic === 'min' && Math.abs(number) > 0 && Math.abs(number) < 0.01;
  return formatDecimal(number, shouldShowMorePrecision ? 4 : 2);
};

export default function OverviewPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    Promise.all([getOverview(), getClassDistribution(), getStatistics(), getSample()])
      .then(([overview, distribution, statistics, sample]) => {
        if (active) setData({ overview, distribution, statistics, sample });
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

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  const { overview, distribution, statistics, sample } = data;
  const stats = statistics.statistics || [];
  const rows = sample.sample || [];
  const fraudPercent = distribution.percentages?.[1] ?? overview.fraud_rate * 100;

  return (
    <>
      <SectionHeader
        title="VISÃO GERAL DO DATASET"
        description="Resumo operacional do conjunto de transações usado para análise e treinamento dos modelos."
      />

      <div className="kpi-grid">
        <KpiCard label="Total de Transações" value={formatNumber(overview.total_transactions)} subtitle="7 features preditoras" color="primary" delay={0} />
        <KpiCard label="Transações Legítimas" value={formatNumber(overview.legitimate_transactions)} subtitle={`${formatPercent(overview.legitimate_rate)} do total`} color="green" delay={80} />
        <KpiCard label="Transações Fraudulentas" value={formatNumber(overview.fraud_transactions)} subtitle={`${formatPercent(overview.fraud_rate)} do total`} color="red" delay={160} />
        <KpiCard label="Taxa de Fraude" value={formatPercent(overview.fraud_rate)} subtitle="classe minoritária" color="amber" delay={240} />
      </div>

      <div className="grid grid--two">
        <Card title="Distribuição de Classes">
          <DonutChart
            labels={distribution.labels}
            data={distribution.percentages}
            colors={['#16a34a', '#dc2626']}
            centerLabel={formatPercentValue(fraudPercent)}
          />
          <div className="legend-row">
            <span><i className="dot dot--green" /> Legítima: {formatNumber(distribution.counts?.[0])}</span>
            <span><i className="dot dot--red" /> Fraude: {formatNumber(distribution.counts?.[1])}</span>
          </div>
          <InsightBox variant="amber">
            O dataset é desbalanceado: fraudes representam apenas {formatPercentValue(fraudPercent)} das transações.
          </InsightBox>
        </Card>

        <Card title="Estatísticas Descritivas">
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Feature</th>
                  <th>Tipo</th>
                  <th>Mín.</th>
                  <th>Média</th>
                  <th>Máx.</th>
                  <th>Desv. Padrão</th>
                </tr>
              </thead>
              <tbody>
                {stats.map((item) => {
                  const type = getFeatureType(item.feature);
                  return (
                    <tr key={item.feature}>
                      <td>{item.display_name || FEATURE_DISPLAY_NAMES[item.feature] || item.feature}</td>
                      <td><Badge variant={type === 'Binária' ? 'binary' : 'type'}>{type}</Badge></td>
                      <td>{formatStatistic(item.feature, 'min', item.min)}</td>
                      <td>{formatStatistic(item.feature, 'mean', item.mean)}</td>
                      <td>{formatStatistic(item.feature, 'max', item.max)}</td>
                      <td>{formatStatistic(item.feature, 'std', item.std)}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </Card>
      </div>

      <Card title="Amostra de Transações">
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                {Object.keys(FEATURE_DISPLAY_NAMES).map((feature) => (
                  <th key={feature}>{FEATURE_DISPLAY_NAMES[feature]}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.index}>
                  <td>#{row.index}</td>
                  <td>{formatDecimal(row.distance_from_home, 2)}</td>
                  <td>{formatDecimal(row.distance_from_last_transaction, 2)}</td>
                  <td>{formatDecimal(row.ratio_to_median_purchase_price, 2)}</td>
                  <td><BinaryChip value={row.repeat_retailer} /></td>
                  <td><BinaryChip value={row.used_chip} /></td>
                  <td><BinaryChip value={row.used_pin_number} /></td>
                  <td><BinaryChip value={row.online_order} /></td>
                  <td><Badge variant={row.fraud ? 'fraud' : 'legit'}>{row.fraud ? 'Fraude' : 'Legítima'}</Badge></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </>
  );
}
