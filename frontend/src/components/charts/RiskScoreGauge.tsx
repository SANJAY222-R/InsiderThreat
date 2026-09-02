/**
 * Risk Score Gauge
 *
 * Circular gauge displaying a user's current risk score.
 *
 * Phase 0: Stub component only.
 */

interface RiskScoreGaugeProps {
  score: number;
  label?: string;
}

export function RiskScoreGauge({ score, label }: RiskScoreGaugeProps) {
  return (
    <div id="chart-risk-gauge" className="chart-container">
      {/* TODO: Circular gauge visualization */}
      <span>{label}: {score}</span>
    </div>
  );
}
