import { useEffect, useState, type ComponentType } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import toast from 'react-hot-toast';

import AgentsStep from '../components/SetupWizard/AgentsStep';
import DataSourceStep from '../components/SetupWizard/DataSourceStep';
import DomainStep from '../components/SetupWizard/DomainStep';
import LLMStep from '../components/SetupWizard/LLMStep';
import ReviewStep from '../components/SetupWizard/ReviewStep';
import WelcomeStep from '../components/SetupWizard/WelcomeStep';
import { apiService } from '../services/api';

const steps = [
  { id: 'welcome', title: 'Bem-vindo', component: WelcomeStep },
  { id: 'llm', title: 'LLM', component: LLMStep },
  { id: 'data_source', title: 'Fonte de Dados', component: DataSourceStep },
  { id: 'domain', title: 'Domínio', component: DomainStep },
  { id: 'agents', title: 'Agentes', component: AgentsStep },
  { id: 'review', title: 'Revisão', component: ReviewStep },
];

export default function SetupWizard() {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(0);
  const [config, setConfig] = useState<any>({});

  const { data: currentConfig } = useQuery({ queryKey: ['config'], queryFn: apiService.getConfig });
  const saveMutation = useMutation({
    mutationFn: apiService.saveConfig,
    onSuccess: () => {
      toast.success('Configuração salva!');
      setTimeout(() => navigate('/dashboard'), 1000);
    },
    onError: () => toast.error('Erro ao salvar'),
  });

  useEffect(() => {
    if (currentConfig) setConfig(currentConfig);
  }, [currentConfig]);

  const handleNext = (stepData?: any) => {
    const nextConfig = stepData ? { ...config, ...stepData } : config;
    setConfig(nextConfig);
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
      return;
    }
    saveMutation.mutate(nextConfig);
  };

  const CurrentComponent = steps[currentStep].component as ComponentType<any>;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-12">
      <div className="max-w-2xl mx-auto px-4">
        <div className="text-center mb-8"><h1 className="text-2xl font-bold dark:text-white">Configuração do EvoBrain</h1><p className="text-gray-500">Configure o sistema para seu domínio</p></div>
        <div className="flex justify-between mb-8 gap-2 flex-wrap">{steps.map((s, i) => (<div key={s.id} className="text-center flex-1 min-w-[72px]"><div className={`w-8 h-8 mx-auto rounded-full flex items-center justify-center ${i <= currentStep ? 'bg-primary-600 text-white' : 'bg-gray-300 text-gray-700'}`}>{i + 1}</div><span className="text-xs dark:text-gray-300">{s.title}</span></div>))}</div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <CurrentComponent config={config} onNext={handleNext} onBack={() => setCurrentStep(Math.max(0, currentStep - 1))} />
        </div>
      </div>
    </div>
  );
}
