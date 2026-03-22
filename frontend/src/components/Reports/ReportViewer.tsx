import { Stats } from '../../services/api';
import Loading from '../Common/Loading';

interface ReportViewerProps { report: string | null; isLoading: boolean; stats?: Stats; }

export default function ReportViewer({ report, isLoading }: ReportViewerProps) {
  if (isLoading) return <div className="card flex items-center justify-center h-96"><Loading /></div>;
  if (report) return <div className="card"><h3 className="text-lg font-semibold mb-4">Relatório Gerado</h3><pre className="whitespace-pre-wrap font-mono text-sm bg-gray-50 dark:bg-gray-700 p-4 rounded-lg overflow-auto max-h-[500px]">{report}</pre></div>;
  return <div className="card flex items-center justify-center h-96"><div className="text-center text-gray-400"><p className="text-lg mb-2">Nenhum relatório gerado</p><p className="text-sm">Clique em "Gerar Relatório" para começar</p></div></div>;
}
