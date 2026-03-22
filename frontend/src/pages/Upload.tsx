import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import PDFUploader from '../components/Upload/PDFUploader';
import { apiService } from '../services/api';

interface UploadResult { filename: string; entities_found: number; relations_found: number; agents_requested: number; }

export default function Upload() {
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [result, setResult] = useState<UploadResult | null>(null);
  const uploadMutation = useMutation({ mutationFn: (file: File) => apiService.uploadPDF(file), onSuccess: (data: UploadResult) => { setUploadStatus('success'); setResult(data); toast.success(`PDF processado! ${data.entities_found} entidades encontradas.`); }, onError: () => { setUploadStatus('error'); toast.error('Erro ao processar PDF'); } });
  const handleUpload = (file: File) => { setUploadStatus('uploading'); uploadMutation.mutate(file); };
  return <div className="space-y-6"><div><h1 className="text-2xl font-bold text-gray-900 dark:text-white">Upload de PDF</h1><p className="text-gray-500 dark:text-gray-400 mt-1">Carregue um PDF para extrair conhecimento e gerar agentes</p></div><div className="grid grid-cols-1 lg:grid-cols-2 gap-6"><PDFUploader onUpload={handleUpload} isLoading={uploadStatus === 'uploading'} />{result && <div className="card"><h3 className="text-lg font-semibold mb-4">Resultado do Processamento</h3><div className="space-y-2"><div className="flex justify-between"><span className="text-gray-500">Arquivo:</span><span className="font-medium">{result.filename}</span></div><div className="flex justify-between"><span className="text-gray-500">Entidades encontradas:</span><span className="font-medium text-primary-600">{result.entities_found}</span></div><div className="flex justify-between"><span className="text-gray-500">Relações encontradas:</span><span className="font-medium text-primary-600">{result.relations_found}</span></div><div className="flex justify-between"><span className="text-gray-500">Agentes solicitados:</span><span className="font-medium text-primary-600">{result.agents_requested}</span></div><div className="mt-4 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg"><p className="text-sm text-green-600 dark:text-green-400">✅ Agentes estão sendo criados em background. Acompanhe na página de Agentes.</p></div></div></div>}</div></div>;
}
