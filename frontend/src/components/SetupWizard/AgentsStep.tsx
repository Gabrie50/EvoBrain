import { useState } from 'react';

interface AgentsStepProps {
  config: any;
  onNext: (data: any) => void;
  onBack: () => void;
}

export default function AgentsStep({ config, onNext, onBack }: AgentsStepProps) {
  const [maxAgents, setMaxAgents] = useState(config?.agents?.max_agents || 10000);
  const [stateSize, setStateSize] = useState(config?.agents?.state_size || 150);
  const [mutationRate, setMutationRate] = useState(config?.neuroevolution?.mutation_rate || 0.1);
  const [keepRatio, setKeepRatio] = useState(config?.competition?.keep_ratio || 0.3);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onNext({ agents: { max_agents: maxAgents, state_size: stateSize }, neuroevolution: { mutation_rate: mutationRate }, competition: { keep_ratio: keepRatio } });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <h2 className="text-xl font-semibold">Configuração dos Agentes</h2>
      <div><label className="block text-sm font-medium mb-2">Máximo de Agentes</label><input type="number" value={maxAgents} onChange={(e) => setMaxAgents(parseInt(e.target.value || '0', 10))} className="w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600" /></div>
      <div><label className="block text-sm font-medium mb-2">Tamanho do Estado</label><input type="number" value={stateSize} onChange={(e) => setStateSize(parseInt(e.target.value || '0', 10))} className="w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600" /></div>
      <div><label className="block text-sm font-medium mb-2">Taxa de Mutação: {mutationRate}</label><input type="range" min="0" max="0.5" step="0.01" value={mutationRate} onChange={(e) => setMutationRate(parseFloat(e.target.value))} className="w-full" /></div>
      <div><label className="block text-sm font-medium mb-2">Eliminação: manter {Math.round(keepRatio * 100)}% dos melhores</label><input type="range" min="0.1" max="0.5" step="0.05" value={keepRatio} onChange={(e) => setKeepRatio(parseFloat(e.target.value))} className="w-full" /></div>
      <div className="flex justify-between pt-4"><button type="button" onClick={onBack} className="px-4 py-2 border rounded-lg">Voltar</button><button type="submit" className="px-6 py-2 bg-primary-600 text-white rounded-lg">Próximo</button></div>
    </form>
  );
}
