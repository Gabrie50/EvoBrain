import React, { useEffect, useRef, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { PaperAirplaneIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { Agent, apiService } from '../../services/api';
import Loading from '../Common/Loading';

interface AgentChatProps { agent: Agent; onClose: () => void; }
interface Message { role: 'user' | 'assistant'; content: string; timestamp: Date; }

export default function AgentChat({ agent, onClose }: AgentChatProps) {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState<Message[]>([{ role: 'assistant', content: `Olá! Sou ${agent.name}. Como posso ajudá-lo hoje?`, timestamp: new Date() }]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const chatMutation = useMutation({ mutationFn: (q: string) => apiService.chatWithAgent(agent.name, q), onSuccess: (response) => setMessages((prev) => [...prev, { role: 'assistant', content: response.response, timestamp: new Date() }]) });
  const handleSend = () => { if (!question.trim() || chatMutation.isPending) return; setMessages((prev) => [...prev, { role: 'user', content: question, timestamp: new Date() }]); chatMutation.mutate(question); setQuestion(''); };
  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);
  useEffect(() => { inputRef.current?.focus(); }, []);
  return <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"><div className="bg-white dark:bg-gray-800 rounded-lg w-full max-w-2xl h-[600px] flex flex-col"><div className="flex justify-between items-center p-4 border-b dark:border-gray-700"><div><h3 className="font-semibold text-lg">{agent.name}</h3><p className="text-sm text-gray-500">{agent.personality.substring(0, 60)}...</p></div><button onClick={onClose} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"><XMarkIcon className="h-5 w-5" /></button></div><div className="flex-1 overflow-y-auto p-4 space-y-3">{messages.map((msg, idx)=><div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}><div className={`max-w-[80%] p-3 rounded-lg ${msg.role === 'user' ? 'bg-primary-600 text-white' : 'bg-gray-100 dark:bg-gray-700'}`}><p className="text-sm whitespace-pre-wrap">{msg.content}</p><p className="text-xs mt-1 opacity-70">{msg.timestamp.toLocaleTimeString()}</p></div></div>)}{chatMutation.isPending && <div className="flex justify-start"><div className="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg"><Loading size="sm" /></div></div>}<div ref={messagesEndRef} /></div><div className="p-4 border-t dark:border-gray-700 flex gap-2"><input ref={inputRef} type="text" value={question} onChange={(e)=>setQuestion(e.target.value)} onKeyDown={(e)=>{if(e.key==='Enter' && !e.shiftKey){e.preventDefault();handleSend();}}} placeholder={`Pergunte algo para ${agent.name}...`} className="flex-1 px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-primary-500" disabled={chatMutation.isPending} /><button onClick={handleSend} disabled={!question.trim() || chatMutation.isPending} className="p-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"><PaperAirplaneIcon className="h-5 w-5" /></button></div></div></div>;
}
