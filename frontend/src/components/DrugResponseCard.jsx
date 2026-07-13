const STATUS_COLORS = {
  'Normal Metabolizer': { bg: '#dcfce7', text: '#166534', dot: '#22c55e' },
  'Normal Sensitivity': { bg: '#dcfce7', text: '#166534', dot: '#22c55e' },
  'Normal Function': { bg: '#dcfce7', text: '#166534', dot: '#22c55e' },
  'HLA-B*57:01 Negative': { bg: '#dcfce7', text: '#166534', dot: '#22c55e' },
  'Rapid Acetylator': { bg: '#dcfce7', text: '#166534', dot: '#22c55e' },
  'Intermediate Metabolizer': { bg: '#fef3c7', text: '#92400e', dot: '#f59e0b' },
  'Intermediate Acetylator': { bg: '#fef3c7', text: '#92400e', dot: '#f59e0b' },
  'Intermediate Function': { bg: '#fef3c7', text: '#92400e', dot: '#f59e0b' },
  'Mildly Sensitive': { bg: '#fef3c7', text: '#92400e', dot: '#f59e0b' },
  'Moderately Sensitive': { bg: '#fef3c7', text: '#92400e', dot: '#f59e0b' },
  'Poor Metabolizer': { bg: '#fecaca', text: '#991b1b', dot: '#ef4444' },
  'Poor Function': { bg: '#fecaca', text: '#991b1b', dot: '#ef4444' },
  'Slow Acetylator': { bg: '#fecaca', text: '#991b1b', dot: '#ef4444' },
  'Highly Sensitive': { bg: '#fecaca', text: '#991b1b', dot: '#ef4444' },
  'HLA-B*57:01 Positive': { bg: '#fecaca', text: '#991b1b', dot: '#ef4444' },
  'Rapid Metabolizer': { bg: '#dbeafe', text: '#1e40af', dot: '#3b82f6' },
  'Ultra-rapid Metabolizer': { bg: '#e0e7ff', text: '#3730a3', dot: '#6366f1' },
  'Insufficient data': { bg: '#f1f5f9', text: '#64748b', dot: '#94a3b8' },
};

/* Clean SVG icons for drug types */
function DrugIcon({ drugName, size = 22 }) {
  const color = 'var(--color-accent)';
  const props = { width: size, height: size, viewBox: '0 0 24 24', fill: 'none', stroke: color, strokeWidth: 1.8, strokeLinecap: 'round', strokeLinejoin: 'round' };

  switch (drugName) {
    case 'Warfarin':
      /* Stethoscope icon */
      return <svg {...props}><path d="M4.8 2.6A2 2 0 103 5h0" /><path d="M3 5v6a7 7 0 0014 0V5" /><circle cx="17" cy="4" r="2" /><path d="M17 6v3" /></svg>;
    case 'Abacavir':
      /* Shield with cross */
      return <svg {...props}><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /><line x1="12" y1="9" x2="12" y2="15" /><line x1="9" y1="12" x2="15" y2="12" /></svg>;
    case 'Simvastatin':
      /* Muscle icon */
      return <svg {...props}><path d="M6 4c0 2.5 2 4 4 4h0c-2 0-4 1.5-4 4v4c0 2 1 4 3 4" /><path d="M18 4c0 2.5-2 4-4 4h0c2 0 4 1.5 4 4v4c0 2-1 4-3 4" /></svg>;
    default:
      /* Pill / capsule icon (used for most drugs) */
      return <svg {...props}><path d="M10.5 1.5l-8 8a5 5 0 007 7l8-8a5 5 0 00-7-7z" /><line x1="8" y1="12" x2="12" y2="8" /></svg>;
  }
}

export default function DrugResponseCard({ result, index }) {
  const colors = STATUS_COLORS[result.metabolizer_status] || STATUS_COLORS['Insufficient data'];

  return (
    <div
      className="card-flat slide-up"
      style={{ animationDelay: `${(index + 5) * 0.08}s`, animationFillMode: 'both' }}
    >
      {/* Header */}
      <div className="flex items-center gap-2.5 mb-2">
        <DrugIcon drugName={result.drug_name} />
        <div>
          <h3 className="text-base font-bold" style={{ color: 'var(--color-text-primary)' }}>
            {result.drug_name}
          </h3>
          <p className="text-xs font-medium" style={{ color: 'var(--color-text-muted)' }}>
            Gene: {result.gene}
          </p>
        </div>
      </div>

      {/* Status badge */}
      <div className="mb-3">
        <span
          className="risk-badge"
          style={{ backgroundColor: colors.bg, color: colors.text }}
        >
          <span
            className="inline-block w-2 h-2 rounded-full mr-1.5"
            style={{ backgroundColor: colors.dot }}
          />
          {result.metabolizer_status}
        </span>
      </div>

      {/* Guidance text */}
      {result.guidance_text && (
        <div
          className="rounded-lg p-3 text-sm leading-relaxed"
          style={{
            backgroundColor: 'var(--color-surface)',
            color: 'var(--color-text-secondary)',
            border: '1px solid var(--color-border-light)',
          }}
        >
          {result.guidance_text}
        </div>
      )}
    </div>
  );
}
