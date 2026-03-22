import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiService } from '../../services/api';

interface LLMStepProps {
  config: any;
  onNext: (data: any) => void;
  onBack: () => void;
}

export default function LLMStep({ config, onNext, onBack }: LLMStepProps) {
  const [llmType, setLlmType] = useState(config?.llm?.type || 'ollama');
  const [model, setModel] = useState(config?.llm?.model || 'llama3.2');
  const [temperature, setTemperature] = useState(config?.llm?.temperature || 0.7);
  const [host, setHost] = useState(config?.llm?.host || 'http://localhost:11434');
  const [apiKey, setApiKey] = useState(config?.llm?.api_key || '');

  const { data: llmTypes } = useQuery({ queryKey: ['llm_types'], queryFn: apiService.listLLMTypes });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const llmConfig: any = { type: llmType, model, temperature };
    if (llmType === 'ollama') llmConfig.host = host;
    if (llmType === 'openai') llmConfig.api_key = apiKey;
    onNext({ llm: llmConfig });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <h2 className="text-xl font-semibold">Configurar LLM</h2>
      <div>
        <label className="block text-sm font-medium mb-2">Tipo de LLM</label>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {llmTypes?.map((type: any) => (
            <button
              key={type.id}
              type="button"
              onClick={() => setLlmType(type.id)}
              className={`p-3 rounded-lg border-2 ${llmType === type.id ? 'border-primary-500 bg-primary-50 dark:bg-gray-700' : 'border-gray-200 dark:border-gray-700'}`}
            >
              <div className="font-medium">{type.name}</div>
              <div className="text-xs text-gray-500">{type.description}</div>
            </button>
          ))}
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium mb-2">Modelo</label>
        <input type="text" value={model} onChange={(e) => setModel(e.target.value)} className="w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600" />
      </div>
      {llmType === 'ollama' && (
        <div>
          <label className="block text-sm font-medium mb-2">Host</label>
          <input type="text" value={host} onChange={(e) => setHost(e.target.value)} className="w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600" />
        </div>
      )}
      {llmType === 'openai' && (
        <div>
          <label className="block text-sm font-medium mb-2">API Key</label>
          <input type="password" value={apiKey} onChange={(e) => setApiKey(e.target.value)} className="w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600" />
        </div>
      )}
      <div>
        <label className="block text-sm font-medium mb-2">Temperatura: {temperature}</label>
        <input type="range" min="0" max="1" step="0.1" value={temperature} onChange={(e) => setTemperature(parseFloat(e.target.value))} className="w-full" />
      </div>
      <div className="flex justify-between pt-4">
        <button type="button" onClick={onBack} className="px-4 py-2 border rounded-lg">Voltar</button>
        <button type="submit" className="px-6 py-2 bg-primary-600 text-white rounded-lg">Próximo</button>
      </div>
    </form>
  );
}
