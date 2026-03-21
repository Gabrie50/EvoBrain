import React from 'react';
import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

interface Prediction { prediction: string; confidence: number; timestamp: number; }
interface TimelineProps { predictions: Prediction[]; }

export default function Timeline({ predictions }: TimelineProps) {
  const data = predictions.slice(-30).map((prediction, index) => ({ index, confidence: prediction.confidence, prediction: prediction.prediction }));
  if (!data.length) return <div className="card"><h3 className="text-lg font-semibold mb-4">Linha do Tempo</h3><div className="text-center text-gray-400 py-8">Aguardando previsões...</div></div>;
  return <div className="card"><h3 className="text-lg font-semibold mb-4">Linha do Tempo (últimas 30 previsões)</h3><ResponsiveContainer width="100%" height={300}><LineChart data={data}><CartesianGrid strokeDasharray="3 3" stroke="#374151" /><XAxis dataKey="index" stroke="#9CA3AF" /><YAxis domain={[0, 100]} stroke="#9CA3AF" /><Tooltip contentStyle={{ backgroundColor: '#1F2937', border: 'none', borderRadius: '8px' }} labelFormatter={(label) => `Previsão #${Number(label) + 1}`} formatter={(value: number) => [`${value}%`, 'Confiança']} /><Line type="monotone" dataKey="confidence" stroke="#3B82F6" strokeWidth={2} dot={({ cx, cy, payload }) => <circle cx={cx} cy={cy} r={3} fill={payload.prediction === 'BANKER' ? '#ef4444' : '#3b82f6'} stroke="none" />} name="Confiança (%)" /></LineChart></ResponsiveContainer><div className="mt-4 flex justify-center gap-4 text-sm"><div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-banker" /><span>Previsão BANKER</span></div><div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-player" /><span>Previsão PLAYER</span></div></div></div>;
}
