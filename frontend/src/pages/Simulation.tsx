import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiService } from '../services/api';
import SimulationView from '../components/Simulation/SimulationView';
import AgentVotes from '../components/Simulation/AgentVotes';
import Timeline from '../components/Simulation/Timeline';
import Loading from '../components/Common/Loading';
import Error from '../components/Common/Error';

export default function Simulation() {
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
  const { data: stats, isLoading, error, refetch } = useQuery({ queryKey: ['stats'], queryFn: apiService.getStats, refetchInterval: 2000 });
  const { data: prediction } = useQuery({ queryKey: ['prediction'], queryFn: apiService.getCurrentPrediction, refetchInterval: 2000 });
  if (isLoading) return <Loading />;
  if (error) return <Error message="Erro ao carregar dados" onRetry={refetch} />;
  return <div className="space-y-6"><div><h1 className="text-2xl font-bold text-gray-900 dark:text-white">Simulação 24/7</h1><p className="text-gray-500 dark:text-gray-400 mt-1">Visualização da simulação em tempo real</p></div><div className="grid grid-cols-1 lg:grid-cols-3 gap-6"><div className="lg:col-span-2"><SimulationView prediction={prediction} stats={stats} /></div><div><AgentVotes votes={prediction?.votes} onSelectAgent={setSelectedAgent} selectedAgent={selectedAgent} /></div></div><Timeline predictions={stats?.simulation?.recent_predictions || []} /></div>;
}
