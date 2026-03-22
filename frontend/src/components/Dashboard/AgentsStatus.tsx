import { Stats } from '../../services/api';

interface AgentsStatusProps {
  stats: Stats;
}

export default function AgentsStatus({ stats }: AgentsStatusProps) {
  const simulation = stats?.simulation || {};
  const generation = stats?.generation || {};

  const progress = generation.total_agents
    ? (simulation.active_agents / generation.total_agents) * 100
    : 0;

  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4">Status dos Agentes</h3>
      
      <div className="space-y-4">
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span>Agentes Ativos</span>
            <span>{simulation.active_agents} / {generation.total_agents}</span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4 mt-4">
          <div className="text-center p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
            <p className="text-2xl font-bold text-primary-600">{simulation.active_agents || 0}</p>
            <p className="text-xs text-gray-500">Ativos</p>
          </div>
          <div className="text-center p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
            <p className="text-2xl font-bold text-yellow-600">{generation.pending || 0}</p>
            <p className="text-xs text-gray-500">Pendentes</p>
          </div>
          <div className="text-center p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
            <p className="text-2xl font-bold text-green-600">{generation.created_last_minute || 0}</p>
            <p className="text-xs text-gray-500">/ min</p>
          </div>
          <div className="text-center p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
            <p className="text-2xl font-bold text-purple-600">
              {simulation.neuroevolution?.generation || 0}
            </p>
            <p className="text-xs text-gray-500">Geração</p>
          </div>
        </div>
      </div>
    </div>
  );
}
