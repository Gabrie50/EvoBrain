import { useCallback, useEffect, useState } from 'react';
import { Prediction, apiService } from '../services/api';

export function usePredictions(interval: number = 2000) {
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [history, setHistory] = useState<Prediction[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const fetchCurrentPrediction = useCallback(async () => { try { const data = await apiService.getCurrentPrediction(); setPrediction(data); setError(null); } catch (err) { setError('Erro ao carregar previsão'); console.error(err); } finally { setIsLoading(false); } }, []);
  const fetchHistory = useCallback(async () => { try { const data = await apiService.getPredictionHistory(100); setHistory(data.history || []); } catch (err) { console.error(err); } }, []);
  useEffect(() => { fetchCurrentPrediction(); fetchHistory(); const id = window.setInterval(fetchCurrentPrediction, interval); return () => window.clearInterval(id); }, [fetchCurrentPrediction, fetchHistory, interval]);
  return { prediction, history, isLoading, error, refetch: fetchCurrentPrediction };
}
