import RiskGauge from './RiskGauge';

const RISK_COLORS = {
  Low: { bg: '#dcfce7', text: '#166534', dot: '#22c55e' },
  Average: { bg: '#fef3c7', text: '#92400e', dot: '#f59e0b' },
  Elevated: { bg: '#fecaca', text: '#991b1b', dot: '#ef4444' },
  'Carrier detected': { bg: '#fecaca', text: '#991b1b', dot: '#ef4444' },
  'No mutation detected': { bg: '#dcfce7', text: '#166534', dot: '#22c55e' },
  'Insufficient data': { bg: '#f1f5f9', text: '#64748b', dot: '#94a3b8' },
};

/* Clean SVG icons for each disease — no emojis */
function DiseaseIcon({ name, size = 22 }) {
  const color = 'var(--color-primary)';
  const props = { width: size, height: size, viewBox: '0 0 24 24', fill: 'none', stroke: color, strokeWidth: 1.8, strokeLinecap: 'round', strokeLinejoin: 'round' };

  switch (name) {
    case 'Type 2 Diabetes':
      /* Drop / blood icon */
      return <svg {...props}><path d="M12 2.69l5.66 5.66a8 8 0 11-11.31 0z" /></svg>;
    case 'Coronary Artery Disease':
      /* Heart icon */
      return <svg {...props}><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" /></svg>;
    case 'Breast Cancer':
      /* Ribbon / awareness icon */
      return <svg {...props}><path d="M12 3c-1.5 2-3 4-3 6 0 2 1.5 3 3 3s3-1 3-3c0-2-1.5-4-3-6z" /><path d="M9 12c-2 1-4 3-4 5s2 4 7 4 7-2 7-4-2-4-4-5" /></svg>;
    case "Alzheimer's Disease":
      /* Brain icon */
      return <svg {...props}><path d="M12 2a7 7 0 017 7c0 2.5-1.5 4.5-3 6l-1 1.5V20a2 2 0 01-2 2h-2a2 2 0 01-2-2v-3.5L8 15c-1.5-1.5-3-3.5-3-6a7 7 0 017-7z" /><path d="M9 18h6" /></svg>;
    case 'Thalassemia':
      /* DNA helix icon */
      return <svg {...props}><path d="M8 4c0 4 8 4 8 8s-8 4-8 8" /><path d="M16 4c0 4-8 4-8 8s8 4 8 8" /><line x1="8" y1="8" x2="16" y2="8" /><line x1="8" y1="16" x2="16" y2="16" /></svg>;
    case "Parkinson's Disease":
      /* Tremor / hand icon */
      return <svg {...props}><path d="M14 3v4a1 1 0 001 1h3" /><path d="M7 3v4a1 1 0 01-1 1H3" /><path d="M10.5 8v4.5c0 1 .5 2 1.5 2s1.5-1 1.5-2V8" /><circle cx="10.5" cy="18" r="2.5" /></svg>;
    case 'Lung Cancer':
      /* Lungs icon */
      return <svg {...props}><path d="M12 4v8" /><path d="M6 8c-2 0-4 2-4 5s2 5 4 7h2c1 0 2-1 2-2V8" /><path d="M18 8c2 0 4 2 4 5s-2 5-4 7h-2c-1 0-2-1-2-2V8" /></svg>;
    case 'Prostate Cancer':
      /* Male symbol / shield icon */
      return <svg {...props}><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /></svg>;
    case 'Celiac Disease':
      /* Wheat / grain icon */
      return <svg {...props}><path d="M12 21V10" /><path d="M8 10c0-2 2-4 4-4s4 2 4 4" /><path d="M6 14c0-2 2-3 3-3" /><path d="M18 14c0-2-2-3-3-3" /><path d="M9 7c0-1.5 1.5-3 3-3s3 1.5 3 3" /></svg>;
    case 'Rheumatoid Arthritis':
      /* Joint / bone icon */
      return <svg {...props}><circle cx="9" cy="7" r="3" /><circle cx="15" cy="17" r="3" /><path d="M9 10v2a3 3 0 003 3h0a3 3 0 003-3v-2" /></svg>;
    case 'Asthma':
      /* Wind / breathing icon */
      return <svg {...props}><path d="M17.7 7.7A2.5 2.5 0 0119 10c0 1.38-1.12 2.5-2.5 2.5H3" /><path d="M9.6 4.6A2 2 0 0111 4c1.1 0 2 .9 2 2s-.9 2-2 2H3" /><path d="M12.6 19.4A2 2 0 0014 20c1.1 0 2-.9 2-2s-.9-2-2-2H3" /></svg>;
    case 'Atrial Fibrillation':
      /* Heart rate / pulse icon */
      return <svg {...props}><polyline points="22 12 18 12 15 21 9 3 6 12 2 12" /></svg>;
    default:
      return <svg {...props}><circle cx="12" cy="12" r="8" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" /></svg>;
  }
}

export default function DiseaseRiskCard({ result, index }) {
  const colors = RISK_COLORS[result.risk_label] || RISK_COLORS['Insufficient data'];
  const isPRS = result.percentile != null;

  return (
    <div
      className="card-flat slide-up flex flex-col"
      style={{ animationDelay: `${index * 0.08}s`, animationFillMode: 'both' }}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2.5">
          <DiseaseIcon name={result.disease_name} />
          <h3 className="text-base font-bold" style={{ color: 'var(--color-text-primary)' }}>
            {result.disease_name}
          </h3>
        </div>
        {isPRS && <RiskGauge percentile={result.percentile} size={72} />}
      </div>

      {/* Risk badge */}
      <div className="mb-3">
        <span
          className="risk-badge"
          style={{ backgroundColor: colors.bg, color: colors.text }}
        >
          <span
            className="inline-block w-2 h-2 rounded-full mr-1.5"
            style={{ backgroundColor: colors.dot }}
          />
          {result.risk_label}
        </span>
      </div>

      {/* Details */}
      <div className="mt-auto">
        {isPRS && (
          <div className="flex gap-4 text-xs" style={{ color: 'var(--color-text-muted)' }}>
            <span>Percentile: <strong style={{ color: 'var(--color-text-secondary)' }}>{result.percentile}%</strong></span>
            {result.raw_score != null && (
              <span>Raw Score: <strong style={{ color: 'var(--color-text-secondary)' }}>{result.raw_score}</strong></span>
            )}
          </div>
        )}
        {result.is_estimated === 'true' && (
          <p className="text-xs mt-1.5 italic" style={{ color: 'var(--color-text-muted)' }}>
            * Population statistics are estimated
          </p>
        )}
      </div>
    </div>
  );
}
