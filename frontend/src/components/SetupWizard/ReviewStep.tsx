
interface ReviewStepProps {
  config: any;
  onNext: () => void;
  onBack: () => void;
}

export default function ReviewStep({ config, onNext, onBack }: ReviewStepProps) {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Revisar Configuração</h2>
      <div className="space-y-4">
        <div className="border rounded-lg p-4"><h3 className="font-semibold mb-2">Domínio</h3><p>{config?.domain?.name || 'Não configurado'}</p><div className="flex gap-2 mt-2 flex-wrap">{config?.domain?.actions?.map((a: any) => <span key={a.id} className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded">{a.emoji || a.color} {a.name}</span>)}</div></div>
        <div className="border rounded-lg p-4"><h3 className="font-semibold mb-2">LLM</h3><p>{config?.llm?.type} - {config?.llm?.model}</p></div>
        <div className="border rounded-lg p-4"><h3 className="font-semibold mb-2">Fonte de Dados</h3><p>{config?.data_source?.type}</p></div>
        <div className="border rounded-lg p-4"><h3 className="font-semibold mb-2">Agentes</h3><p>Máximo: {config?.agents?.max_agents} | Tamanho estado: {config?.agents?.state_size}</p></div>
      </div>
      <div className="flex justify-between pt-4"><button type="button" onClick={onBack} className="px-4 py-2 border rounded-lg">Voltar</button><button onClick={onNext} className="px-6 py-2 bg-green-600 text-white rounded-lg">Concluir e Iniciar</button></div>
    </div>
  );
}
