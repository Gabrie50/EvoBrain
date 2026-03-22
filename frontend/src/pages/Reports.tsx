import { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import GenerateReport from '../components/Reports/GenerateReport';
import ReportViewer from '../components/Reports/ReportViewer';
import Error from '../components/Common/Error';
import Loading from '../components/Common/Loading';
import { apiService } from '../services/api';

type ReportType = 'full' | 'summary' | 'detailed';

export default function Reports() {
  const [reportType, setReportType] = useState<ReportType>('full');
  const [report, setReport] = useState<string | null>(null);
  const { data: stats, isLoading: statsLoading, error: statsError } = useQuery({ queryKey: ['stats'], queryFn: apiService.getStats });
  const generateMutation = useMutation({ mutationFn: (type: ReportType) => apiService.generateReport(type), onSuccess: (data) => setReport(data.report) });
  if (statsLoading) return <Loading />;
  if (statsError) return <Error message="Erro ao carregar dados" />;
  return <div className="space-y-6"><div><h1 className="text-2xl font-bold text-gray-900 dark:text-white">Relatórios</h1><p className="text-gray-500 dark:text-gray-400 mt-1">Gere relatórios detalhados da simulação</p></div><div className="grid grid-cols-1 lg:grid-cols-3 gap-6"><div className="lg:col-span-1"><GenerateReport stats={stats} reportType={reportType} onReportTypeChange={setReportType} onGenerate={() => generateMutation.mutate(reportType)} isLoading={generateMutation.isPending} /></div><div className="lg:col-span-2"><ReportViewer report={report} isLoading={generateMutation.isPending} stats={stats} /></div></div></div>;
}
