import { Agent } from '../../types';

interface AgentDetailProps {
  agent: Agent;
}

export default function AgentDetail({ agent }: AgentDetailProps) {
  const accuracyColor = agent.accuracy >= 70 ? 'text-green-600' : agent.accuracy >= 50 ? 'text-yellow-600' : 'text-red-600';

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-4">
        <div className="w-16 h-16 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center text-2xl">
          🧠
        </div>
        <div>
          <h2 className="text-xl font-bold">{agent.name}</h2>
          <p className="text-gray-500">ID: {agent.id}</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <p className="text-sm text-gray-500">Precisão</p>
          <p className={`text-2xl font-bold ${accuracyColor}`}>{agent.accuracy.toFixed(1)}%</p>
        </div>
        <div className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <p className="text-sm text-gray-500">Decisões</p>
          <p className="text-2xl font-bold">{agent.total_uso}</p>
        </div>
        <div className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <p className="text-sm text-gray-500">Acertos</p>
          <p className="text-2xl font-bold text-green-600">{agent.acertos || 0}</p>
        </div>
        <div className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <p className="text-sm text-gray-500">Erros</p>
          <p className="text-2xl font-bold text-red-600">{(agent.total_uso || 0) - (agent.acertos || 0)}</p>
        </div>
      </div>

      <div>
        <h4 className="font-semibold mb-2">Personalidade</h4>
        <p className="text-gray-600 dark:text-gray-300">{agent.personality}</p>
      </div>

      <div>
        <h4 className="font-semibold mb-2">Traços</h4>
        <div className="flex flex-wrap gap-2">
          {agent.traits?.map((trait, idx) => (
            <span key={idx} className="px-3 py-1 bg-gray-100 dark:bg-gray-700 rounded-full text-sm">
              {trait}
            </span>
          ))}
        </div>
      </div>

      {agent.specializations?.length > 0 && (
        <div>
          <h4 className="font-semibold mb-2">Especializações</h4>
          <div className="flex flex-wrap gap-2">
            {agent.specializations.map((spec, idx) => (
              <span key={idx} className="px-3 py-1 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded-full text-sm">
                {spec}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
