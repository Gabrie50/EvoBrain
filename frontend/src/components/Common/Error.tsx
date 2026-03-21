import React from 'react';
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline';

interface ErrorProps { message: string; onRetry?: () => void; }

export default function Error({ message, onRetry }: ErrorProps) {
  return <div className="flex flex-col items-center justify-center p-8 text-center"><ExclamationTriangleIcon className="h-12 w-12 text-red-500 mb-4" /><p className="text-gray-600 dark:text-gray-400 mb-4">{message}</p>{onRetry && <button onClick={onRetry} className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">Tentar novamente</button>}</div>;
}
