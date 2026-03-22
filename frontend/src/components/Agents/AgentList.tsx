import { Agent } from '../../services/api';
import AgentCard from './AgentCard';

interface AgentListProps { agents: Agent[]; onSelectAgent: (agent: Agent) => void; onChatWithAgent: (agent: Agent) => void; }

export default function AgentList({ agents, onSelectAgent, onChatWithAgent }: AgentListProps) {
  if (agents.length === 0) return <div className="text-center py-12 text-gray-500">Nenhum agente encontrado. Faça upload de um PDF para criar agentes.</div>;
  return <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">{agents.map((agent) => <AgentCard key={agent.id} agent={agent} onClick={() => onSelectAgent(agent)} onChat={() => onChatWithAgent(agent)} />)}</div>;
}
