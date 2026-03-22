import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { Stats } from '../../services/api';

interface AccuracyChartProps {
  stats: Stats;
}

export default function AccuracyChart({ stats }: AccuracyChartProps) {
  const predictions = stats?.simulation?.recent_predictions || [];
  
  // Calcula precisão móvel a cada 10 previsões
  const data = [];
  for (let i = 10; i <= predictions.length; i += 10) {
    const slice = predictions.slice(i - 10, i);
    const accuracy = slice.filter(p => p.prediction === 'BANKER' ? true : false).length / 10 * 100; // Placeholder
    data.push({
      step: i,
      accuracy: accuracy,
    });
  }

  if (data.length === 0) {
    return (
      <div className="card">
        <h3 className="text-lg font-semibold mb-4">Evolução da Precisão</h3>
        <div className="h-64 flex items-center justify-center text-gray-400">
          Aguardando dados...
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4">Evolução da Precisão</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis dataKey="step" stroke="#9CA3AF" />
          <YAxis domain={[0, 100]} stroke="#9CA3AF" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1F2937',
              border: 'none',
              borderRadius: '8px',
            }}
          />
          <Line
            type="monotone"
            dataKey="accuracy"
            stroke="#3B82F6"
            strokeWidth={2}
            dot={{ fill: '#3B82F6', r: 4 }}
            name="Precisão (%)"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
