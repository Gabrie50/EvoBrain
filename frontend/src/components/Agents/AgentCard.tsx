import { ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline';
import { Agent } from '../../services/api';

interface AgentCardProps { agent: Agent; onClick: () => void; onChat: () => void; }

export default function AgentCard({ agent, onClick, onChat }: AgentCardProps) {
  const accuracyColor = agent.accuracy >= 70 ? 'text-green-600' : agent.accuracy >= 50 ? 'text-yellow-600' : 'text-red-600';
  return <div className="card hover:shadow-lg transition-shadow"><div className="flex justify-between items-start"><div className="flex-1 cursor-pointer" onClick={onClick}><h3 className="font-semibold text-lg">{agent.name}</h3><p className="text-sm text-gray-500 dark:text-gray-400 mt-1 line-clamp-2">{agent.personality}</p></div><button onClick={onChat} className="p-2 text-gray-400 hover:text-primary-600 transition-colors" title="Conversar com agente"><ChatBubbleLeftRightIcon className="h-5 w-5" /></button></div><div className="mt-4 flex items-center justify-between"><div><span className="text-xs text-gray-500">Precisão</span><p className={`text-xl font-bold ${accuracyColor}`}>{agent.accuracy.toFixed(1)}%</p></div><div><span className="text-xs text-gray-500">Decisões</span><p className="text-xl font-bold">{agent.total_uso}</p></div><div><span className="text-xs text-gray-500">Fitness</span><p className="text-xl font-bold">{agent.fitness.toFixed(0)}</p></div></div>{agent.specializations.length > 0 && <div className="mt-3 flex flex-wrap gap-1">{agent.specializations.slice(0,3).map((spec, idx)=><span key={idx} className="text-xs px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded-full">{spec}</span>)}</div>}</div>;
}
