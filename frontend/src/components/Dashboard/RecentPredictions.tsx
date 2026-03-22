
interface Prediction {
  prediction: string;
  confidence: number;
  timestamp: number;
}

interface RecentPredictionsProps {
  predictions: Prediction[];
}

export default function RecentPredictions({ predictions }: RecentPredictionsProps) {
  if (predictions.length === 0) {
    return (
      <div className="card">
        <h3 className="text-lg font-semibold mb-4">Últimas Previsões</h3>
        <div className="text-center text-gray-400 py-8">
          Nenhuma previsão realizada ainda
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4">Últimas Previsões</h3>
      <div className="space-y-2">
        {predictions.slice(-10).reverse().map((pred, idx) => (
          <div
            key={idx}
            className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg"
          >
            <div className="flex items-center gap-3">
              <span
                className={`text-xl font-bold ${
                  pred.prediction === 'BANKER' ? 'text-banker' : 'text-player'
                }`}
              >
                {pred.prediction}
              </span>
              <span className="text-sm text-gray-500">
                {pred.confidence}% confiança
              </span>
            </div>
            <span className="text-sm text-gray-400">
              {new Date(pred.timestamp * 1000).toLocaleTimeString('pt-BR')}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
