
interface AgentVotesProps { votes?: { BANKER: number; PLAYER: number; }; onSelectAgent?: (agentName: string) => void; selectedAgent?: string | null; }

export default function AgentVotes({ votes }: AgentVotesProps) {
  if (!votes) return <div className="card"><h3 className="text-lg font-semibold mb-4">Votação dos Agentes</h3><div className="text-center text-gray-400 py-8">Aguardando votação...</div></div>;
  const total = votes.BANKER + votes.PLAYER;
  const bankerPercent = total > 0 ? (votes.BANKER / total) * 100 : 50;
  const playerPercent = total > 0 ? (votes.PLAYER / total) * 100 : 50;
  return <div className="card"><h3 className="text-lg font-semibold mb-4">Votação dos Agentes</h3><div className="space-y-4"><div><div className="flex justify-between text-sm mb-1"><span className="text-banker font-medium">BANKER</span><span>{votes.BANKER.toFixed(1)}</span></div><div className="h-2 bg-gray-200 rounded-full overflow-hidden"><div className="h-full bg-banker transition-all duration-500" style={{ width: `${bankerPercent}%` }} /></div></div><div><div className="flex justify-between text-sm mb-1"><span className="text-player font-medium">PLAYER</span><span>{votes.PLAYER.toFixed(1)}</span></div><div className="h-2 bg-gray-200 rounded-full overflow-hidden"><div className="h-full bg-player transition-all duration-500" style={{ width: `${playerPercent}%` }} /></div></div><div className="pt-4 text-center text-sm text-gray-500">Total de votos: {total.toFixed(1)}</div></div></div>;
}
