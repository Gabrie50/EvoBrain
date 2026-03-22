import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Agent, apiService } from '../services/api';
import AgentChat from '../components/Agents/AgentChat';
import AgentDetail from '../components/Agents/AgentDetail';
import AgentList from '../components/Agents/AgentList';
import Loading from '../components/Common/Loading';
import Error from '../components/Common/Error';
import Modal from '../components/Common/Modal';

export default function Agents() {
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [showChat, setShowChat] = useState(false);
  const [search, setSearch] = useState('');
  const { data: agents, isLoading, error, refetch } = useQuery({ queryKey: ['agents'], queryFn: apiService.listAgents, refetchInterval: 10000 });
  const filteredAgents = agents?.filter((agent: Agent) => agent.name.toLowerCase().includes(search.toLowerCase()));
  if (isLoading) return <Loading />;
  if (error) return <Error message="Erro ao carregar agentes" onRetry={refetch} />;
  return <div className="space-y-6"><div className="flex justify-between items-center"><div><h1 className="text-2xl font-bold text-gray-900 dark:text-white">Agentes</h1><p className="text-gray-500 dark:text-gray-400 mt-1">{agents?.length || 0} agentes ativos</p></div><input type="text" placeholder="Buscar agente..." value={search} onChange={(e) => setSearch(e.target.value)} className="px-4 py-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700" /></div><AgentList agents={filteredAgents || []} onSelectAgent={(agent)=>{setSelectedAgent(agent);setShowChat(false);}} onChatWithAgent={(agent)=>{setSelectedAgent(agent);setShowChat(true);}} />{selectedAgent && !showChat && <Modal isOpen={true} onClose={() => setSelectedAgent(null)} title={`Detalhes: ${selectedAgent.name}`} size="lg"><AgentDetail agent={selectedAgent} /><div className="mt-4 flex justify-end"><button onClick={() => setShowChat(true)} className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">Conversar com agente</button></div></Modal>}{selectedAgent && showChat && <AgentChat agent={selectedAgent} onClose={() => { setSelectedAgent(null); setShowChat(false); }} />}</div>;
}
