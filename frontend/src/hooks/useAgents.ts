import { useCallback, useEffect, useState } from 'react';
import { Agent, apiService } from '../services/api';

export function useAgents(interval: number = 10000) {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const fetchAgents = useCallback(async () => { try { const data = await apiService.listAgents(); setAgents(data); setError(null); } catch (err) { setError('Erro ao carregar agentes'); console.error(err); } finally { setIsLoading(false); } }, []);
  const getAgent = useCallback(async (name: string) => { try { return await apiService.getAgent(name); } catch (err) { console.error(err); return null; } }, []);
  const getAgentStats = useCallback(async (name: string) => { try { return await apiService.getAgentStats(name); } catch (err) { console.error(err); return null; } }, []);
  useEffect(() => { fetchAgents(); const id = window.setInterval(fetchAgents, interval); return () => window.clearInterval(id); }, [fetchAgents, interval]);
  return { agents, isLoading, error, getAgent, getAgentStats, refetch: fetchAgents };
}
