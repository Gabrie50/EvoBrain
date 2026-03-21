import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiService } from '../services/api';
import StatsCards from '../components/Dashboard/StatsCards';
import AccuracyChart from '../components/Dashboard/AccuracyChart';
import AgentsStatus from '../components/Dashboard/AgentsStatus';
import RecentPredictions from '../components/Dashboard/RecentPredictions';
import PredictionCard from '../components/Dashboard/PredictionCard';
import Loading from '../components/Common/Loading';

export default function Dashboard() {
  const { data: stats, isLoading: statsLoading, error: statsError } = useQuery({
    queryKey: ['stats'],
    queryFn: apiService.getStats,
    refetchInterval: 5000,
  });

  const { data: prediction, isLoading: predLoading } = useQuery({
    queryKey: ['prediction'],
    queryFn: apiService.getCurrentPrediction,
    refetchInterval: 2000,
  });

  if (statsLoading) {
    return <Loading />;
  }

  if (statsError) {
    return (
      <div className="text-center py-10 text-red-500">
        Erro ao carregar estatísticas. Verifique se o backend está rodando.
      </div>
    );
  }

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

      {/* Previsão Atual */}
      {prediction && prediction.status !== 'no_prediction' && (
        <PredictionCard prediction={prediction} />
      )}

      {/* Cards de Estatísticas */}
      <StatsCards stats={stats} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Gráfico de Precisão */}
        <AccuracyChart stats={stats} />

        {/* Status dos Agentes */}
        <AgentsStatus stats={stats} />
      </div>

      {/* Últimas Previsões */}
      <RecentPredictions predictions={stats?.simulation?.recent_predictions || []} />
    </div>
  );
}
