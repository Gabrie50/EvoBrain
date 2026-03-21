import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { CloudArrowUpIcon, DocumentIcon } from '@heroicons/react/24/outline';
import Loading from '../Common/Loading';

interface PDFUploaderProps { onUpload: (file: File) => void; isLoading: boolean; }

export default function PDFUploader({ onUpload, isLoading }: PDFUploaderProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const onDrop = useCallback((acceptedFiles: File[]) => { const file = acceptedFiles[0]; if (file && file.type === 'application/pdf') setSelectedFile(file); }, []);
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, accept: { 'application/pdf': ['.pdf'] }, maxFiles: 1 });
  return <div className="card"><h3 className="text-lg font-semibold mb-4">Upload de PDF</h3><div {...getRootProps()} className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${isDragActive ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20' : 'border-gray-300 dark:border-gray-600 hover:border-primary-400'}`}><input {...getInputProps()} /><CloudArrowUpIcon className="h-12 w-12 mx-auto text-gray-400 mb-4" />{isDragActive ? <p className="text-primary-600">Solte o arquivo aqui...</p> : <div><p className="text-gray-600 dark:text-gray-400">Arraste e solte um arquivo PDF aqui, ou clique para selecionar</p><p className="text-sm text-gray-400 mt-2">Apenas arquivos PDF são aceitos</p></div>}</div>{selectedFile && <div className="mt-4 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg flex items-center justify-between"><div className="flex items-center gap-3"><DocumentIcon className="h-8 w-8 text-red-500" /><div><p className="font-medium truncate max-w-[200px]">{selectedFile.name}</p><p className="text-xs text-gray-500">{(selectedFile.size / 1024).toFixed(1)} KB</p></div></div><button onClick={() => onUpload(selectedFile)} disabled={isLoading} className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50">{isLoading ? <Loading size="sm" /> : 'Enviar'}</button></div>}<div className="mt-4 text-sm text-gray-500"><p>O PDF será processado para extrair:</p><ul className="list-disc list-inside mt-2 space-y-1"><li>Entidades e relações (GraphRAG)</li><li>Geração dinâmica de agentes</li><li>Personalidades baseadas no conteúdo</li></ul></div></div>;
}
