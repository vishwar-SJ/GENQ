import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

export default function RiskGauge({ percentile, size = 100 }) {
  if (percentile == null) return null;

  const value = Math.round(percentile);
  const remaining = 100 - value;
  const data = [
    { name: 'Score', value: value },
    { name: 'Remaining', value: remaining },
  ];

  // Color based on percentile
  let fillColor = '#22c55e'; // green (Low)
  if (value >= 33 && value <= 66) fillColor = '#f59e0b'; // amber (Average)
  if (value > 66) fillColor = '#ef4444'; // red (Elevated)

  return (
    <div className="relative" style={{ width: size, height: size }}>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            startAngle={90}
            endAngle={-270}
            innerRadius={size * 0.32}
            outerRadius={size * 0.44}
            dataKey="value"
            stroke="none"
          >
            <Cell fill={fillColor} />
            <Cell fill="#e2e8f0" />
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      <div
        className="absolute inset-0 flex items-center justify-center"
      >
        <div className="text-center">
          <span className="text-lg font-bold" style={{ color: fillColor }}>{value}</span>
          <span className="text-[10px] block" style={{ color: 'var(--color-text-muted)', marginTop: '-2px' }}>
            %ile
          </span>
        </div>
      </div>
    </div>
  );
}
