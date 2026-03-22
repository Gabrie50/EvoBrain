import { useState, type FormEvent } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiService } from '../../services/api';

interface DomainStepProps {
  config: any;
  onNext: (data: any) => void;
  onBack: () => void;
}

export default function DomainStep({ config, onNext, onBack }: DomainStepProps) {
  const [domainType, setDomainType] = useState(config?.domain?.type || 'bacbo');
  const [customActions, setCustomActions] = useState(config?.domain?.actions || [{ id: 0, name: 'ACAO_A', color: '🔴' }, { id: 1, name: 'ACAO_B', color: '🔵' }]);

  const { data: domains } = useQuery({ queryKey: ['domains'], queryFn: apiService.listDomains });
  const selectedDomain = domains?.find((d: any) => d.id === domainType);

  const handleAddAction = () => setCustomActions([...customActions, { id: customActions.length, name: `ACAO_${String.fromCharCode(65 + customActions.length)}`, color: '⚪', emoji: '⚪' }]);
  const handleRemoveAction = (id: number) => setCustomActions(customActions.filter((a: any) => a.id !== id));
  const handleActionChange = (id: number, field: string, value: string) => setCustomActions(customActions.map((a: any) => a.id === id ? { ...a, [field]: value, emoji: field === 'color' ? value : a.emoji } : a));

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    const domainConfig = domainType === 'custom'
      ? { type: 'custom', name: 'Customizado', description: 'Domínio customizado', actions: customActions }
      : selectedDomain;
    onNext({ domain: domainConfig });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <h2 className="text-xl font-semibold">Domínio de Aplicação</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {domains?.map((domain: any) => (
          <button key={domain.id} type="button" onClick={() => setDomainType(domain.id)} className={`p-3 rounded-lg border-2 text-left ${domainType === domain.id ? 'border-primary-500 bg-primary-50 dark:bg-gray-700' : 'border-gray-200 dark:border-gray-700'}`}>
            <div className="font-medium">{domain.name}</div>
            <div className="text-xs text-gray-500">{domain.description}</div>
            <div className="flex gap-1 mt-1">{domain.actions?.map((a: any) => <span key={a.id} className="text-xs">{a.emoji || a.color}</span>)}</div>
          </button>
        ))}
      </div>
      {domainType === 'custom' && (
        <div className="space-y-3">
          <div className="flex justify-between"><label className="text-sm font-medium">Ações</label><button type="button" onClick={handleAddAction} className="text-primary-600 text-sm">+ Adicionar</button></div>
          {customActions.map((a: any) => (
            <div key={a.id} className="flex gap-2">
              <input type="text" value={a.name} onChange={(e) => handleActionChange(a.id, 'name', e.target.value)} className="flex-1 px-2 py-1 border rounded dark:bg-gray-700 dark:border-gray-600" placeholder="Nome" />
              <input type="text" value={a.color} onChange={(e) => handleActionChange(a.id, 'color', e.target.value)} className="w-12 px-1 py-1 border rounded text-center dark:bg-gray-700 dark:border-gray-600" placeholder="🔴" />
              {customActions.length > 2 && <button type="button" onClick={() => handleRemoveAction(a.id)} className="text-red-500">🗑️</button>}
            </div>
          ))}
        </div>
      )}
      <div className="flex justify-between pt-4"><button type="button" onClick={onBack} className="px-4 py-2 border rounded-lg">Voltar</button><button type="submit" className="px-6 py-2 bg-primary-600 text-white rounded-lg">Próximo</button></div>
    </form>
  );
}
