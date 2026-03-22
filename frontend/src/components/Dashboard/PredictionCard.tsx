import { Prediction } from '../../services/api';

interface PredictionCardProps {
  prediction: Prediction;
}

export default function PredictionCard({ prediction }: PredictionCardProps) {
  const isBanker = prediction.prediction === 'BANKER';
  const votes = prediction.votes || { BANKER: 0, PLAYER: 0 };
  const totalVotes = votes.BANKER + votes.PLAYER;
  const bankerPercentage = totalVotes > 0 ? (votes.BANKER / totalVotes) * 100 : 50;
  const playerPercentage = totalVotes > 0 ? (votes.PLAYER / totalVotes) * 100 : 50;

  return (
    <div className="card">
      <div className="text-center">
        <h2 className="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
          Previsão Atual
        </h2>
        <div className="mt-3">
          <span className={`text-5xl font-bold ${isBanker ? 'text-banker' : 'text-player'}`}>
            {prediction.prediction}
          </span>
          <span className="text-2xl text-gray-500 ml-2">
            ({prediction.confidence}%)
          </span>
        </div>
      </div>

      <div className="mt-6">
        <div className="flex h-10 rounded-lg overflow-hidden shadow-sm">
          <div
            className="bg-banker transition-all duration-500 flex items-center justify-center text-white text-sm font-medium"
            style={{ width: `${bankerPercentage}%` }}
          >
            {bankerPercentage > 15 && `BANKER ${Math.round(bankerPercentage)}%`}
          </div>
          <div
            className="bg-player transition-all duration-500 flex items-center justify-center text-white text-sm font-medium"
            style={{ width: `${playerPercentage}%` }}
          >
            {playerPercentage > 15 && `PLAYER ${Math.round(playerPercentage)}%`}
          </div>
        </div>
      </div>

      <div className="mt-4 flex justify-between text-sm text-gray-500 dark:text-gray-400">
        <span>{prediction.agents_active} agentes ativos</span>
        <span>
          {new Date(prediction.timestamp * 1000).toLocaleTimeString('pt-BR')}
        </span>
      </div>
    </div>
  );
}
