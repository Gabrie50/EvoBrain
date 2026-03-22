import { useState, type FormEvent } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiService } from '../../services/api';

interface DataSourceStepProps {
  config: any;
  onNext: (data: any) => void;
  onBack: () => void;
}

export default function DataSourceStep({ config, onNext, onBack }: DataSourceStepProps) {
  const [sourceType, setSourceType] = useState(config?.data_source?.type || 'bacbo');
  const [interval, setInterval] = useState(config?.data_source?.interval || 0.5);
  const [apiUrl, setApiUrl] = useState(config?.data_source?.rest_url || '');
  const [wsUrl, setWsUrl] = useState(config?.data_source?.ws_url || '');

  const { data: sourceTypes } = useQuery({ queryKey: ['data_source_types'], queryFn: apiService.listDataSourceTypes });

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    const dsConfig: any = { type: sourceType, enabled: true, interval };
    if (sourceType === 'rest_api') dsConfig.rest_url = apiUrl;
    if (sourceType === 'websocket') dsConfig.ws_url = wsUrl;
    onNext({ data_source: dsConfig });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <h2 className="text-xl font-semibold">Fonte de Dados</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {sourceTypes?.map((type: any) => (
          <button
            key={type.id}
            type="button"
            onClick={() => setSourceType(type.id)}
            className={`p-3 rounded-lg border-2 ${sourceType === type.id ? 'border-primary-500 bg-primary-50 dark:bg-gray-700' : 'border-gray-200 dark:border-gray-700'}`}
          >
            <div className="font-medium">{type.name}</div>
            <div className="text-xs text-gray-500">{type.description}</div>
          </button>
        ))}
      </div>
      {sourceType === 'rest_api' && <div><label className="block text-sm font-medium mb-2">URL da API</label><input type="text" value={apiUrl} onChange={(e) => setApiUrl(e.target.value)} className="w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600" required /></div>}
      {sourceType === 'websocket' && <div><label className="block text-sm font-medium mb-2">URL do WebSocket</label><input type="text" value={wsUrl} onChange={(e) => setWsUrl(e.target.value)} className="w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600" required /></div>}
      {sourceType === 'bacbo' && <div className="p-3 bg-green-50 dark:bg-green-900/30 rounded-lg"><p className="text-sm text-green-600 dark:text-green-300">✅ Bac Bo configurado automaticamente</p></div>}
      <div><label className="block text-sm font-medium mb-2">Intervalo: {interval}s</label><input type="range" min="0.1" max="5" step="0.1" value={interval} onChange={(e) => setInterval(parseFloat(e.target.value))} className="w-full" /></div>
      <div className="flex justify-between pt-4"><button type="button" onClick={onBack} className="px-4 py-2 border rounded-lg">Voltar</button><button type="submit" className="px-6 py-2 bg-primary-600 text-white rounded-lg">Próximo</button></div>
    </form>
  );
}
