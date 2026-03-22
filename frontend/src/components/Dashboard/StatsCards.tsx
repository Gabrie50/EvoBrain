import { Stats } from '../../services/api';

interface StatsCardsProps {
  stats: Stats;
}

export default function StatsCards({ stats }: StatsCardsProps) {
  const simulation = stats?.simulation || {};
  const generation = stats?.generation || {};

  const cards = [
    {
      title: 'Precisão',
      value: `${simulation.accuracy?.toFixed(1) || 0}%`,
      change: null,
      icon: '🎯',
      color: 'text-green-600',
    },
    {
      title: 'Previsões',
      value: simulation.predictions_made || 0,
      change: null,
      icon: '📊',
      color: 'text-blue-600',
    },
    {
      title: 'Agentes Ativos',
      value: simulation.active_agents || 0,
      change: `+${generation.created_last_minute || 0} / min`,
      icon: '🤖',
      color: 'text-purple-600',
    },
    {
      title: 'Total Agentes',
      value: generation.total_agents || 0,
      change: `${generation.pending || 0} pendentes`,
      icon: '👥',
      color: 'text-orange-600',
    },
    {
      title: 'Geração',
      value: simulation.neuroevolution?.generation || 0,
      change: `fitness ${simulation.neuroevolution?.best_fitness?.toFixed(1) || 0}%`,
      icon: '🧬',
      color: 'text-indigo-600',
    },
    {
      title: 'Uptime',
      value: `${Math.floor((stats.uptime || 0) / 3600)}h`,
      change: stats.llm_connected ? 'LLM OK' : 'LLM offline',
      icon: '⏱️',
      color: 'text-gray-600',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {cards.map((card, idx) => (
        <div key={idx} className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400">{card.title}</p>
              <p className={`text-2xl font-bold ${card.color}`}>{card.value}</p>
              {card.change && (
                <p className="text-xs text-gray-400 mt-1">{card.change}</p>
              )}
            </div>
            <div className="text-3xl">{card.icon}</div>
          </div>
        </div>
      ))}
    </div>
  );
}
