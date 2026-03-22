import { useQuery } from '@tanstack/react-query';
import Loading from '../components/Common/Loading';
import AccuracyChart from '../components/Dashboard/AccuracyChart';
import AgentsStatus from '../components/Dashboard/AgentsStatus';
import PredictionCard from '../components/Dashboard/PredictionCard';
import RecentPredictions from '../components/Dashboard/RecentPredictions';
import StatsCards from '../components/Dashboard/StatsCards';
import { apiService } from '../services/api';

export default function Dashboard() {
  const { data: stats, isLoading: statsLoading, error: statsError } = useQuery({
    queryKey: ['stats'],
    queryFn: apiService.getStats,
    refetchInterval: 5000,
  });

  const { data: prediction } = useQuery({
    queryKey: ['prediction'],
    queryFn: apiService.getCurrentPrediction,
    refetchInterval: 2000,
  });

  if (statsLoading) {
    return <Loading />;
  }

  if (statsError || !stats) {
    return (
      <div className="text-center py-10 text-red-500">
        Erro ao carregar estatísticas. Verifique se o backend está rodando.
      </div>
    );
  }

  const hasPrediction = prediction && prediction.prediction;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Dashboard
        </h1>
        <p className="text-gray-500 dark:text-gray-400 mt-1">
          Visão geral do sistema de previsão 24/7
        </p>
      </div>

      {hasPrediction && <PredictionCard prediction={prediction} />}

      <StatsCards stats={stats} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AccuracyChart stats={stats} />
        <AgentsStatus stats={stats} />
      </div>

      <RecentPredictions predictions={stats?.simulation?.recent_predictions || []} />
    </div>
  );
}
