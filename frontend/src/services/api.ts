import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
});

// Tipos
export interface Stats {
  status: string;
  simulation: {
    active_agents: number;
    predictions_made: number;
    correct_predictions: number;
    accuracy: number;
    history_size: number;
    neuroevolution: {
      generation: number;
      best_fitness: number;
      population_size: number;
    };
    recent_predictions: Array<{
      prediction: string;
      confidence: number;
      timestamp: number;
    }>;
  };
  generation: {
    total_agents: number;
    pending: number;
    created_last_minute: number;
  };
  uptime: number;
  llm_connected: boolean;
}

export interface Prediction {
  prediction: string;
  confidence: number;
  votes: {
    BANKER: number;
    PLAYER: number;
  };
  agents_active: number;
  timestamp: number;
}

export interface Agent {
  id: number;
  name: string;
  personality: string;
  traits: string[];
  mbti: string;
  accuracy: number;
  total_uso: number;
  fitness: number;
  specializations: string[];
}

export const apiService = {
  // Stats
  getStats: async (): Promise<Stats> => {
    const response = await api.get('/stats');
    return response.data;
  },
  
  getStatsSummary: async () => {
    const response = await api.get('/stats/summary');
    return response.data;
  },
  
  // Predictions
  getCurrentPrediction: async (): Promise<Prediction> => {
    const response = await api.get('/predict/current');
    return response.data;
  },
  
  getPredictionHistory: async (limit: number = 100) => {
    const response = await api.get(`/predict/history?limit=${limit}`);
    return response.data;
  },
  
  // Agents
  listAgents: async (): Promise<Agent[]> => {
    const response = await api.get('/agents');
    return response.data;
  },
  
  getAgent: async (name: string): Promise<Agent> => {
    const response = await api.get(`/agents/${encodeURIComponent(name)}`);
    return response.data;
  },
  
  getAgentStats: async (name: string) => {
    const response = await api.get(`/agents/${encodeURIComponent(name)}/stats`);
    return response.data;
  },
  
  // Chat
  chatWithAgent: async (agentName: string, question: string) => {
    const response = await api.post('/chat/agent', {
      agent_name: agentName,
      question,
    });
    return response.data;
  },
  
  listChatAgents: async () => {
    const response = await api.get('/chat/agents');
    return response.data;
  },
  
  // Reports
  generateReport: async (type: 'full' | 'summary' | 'detailed' = 'full') => {
    const response = await api.get(`/report/generate?type=${type}`);
    return response.data;
  },
  
  getReportSummary: async () => {
    const response = await api.get('/report/summary');
    return response.data;
  },
  
  // Upload
  uploadPDF: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/upload/pdf', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
  

  // Config
  getConfig: async () => {
    const response = await api.get('/config');
    return response.data;
  },

  saveConfig: async (config: any) => {
    const response = await api.post('/config/save', config);
    return response.data;
  },

  listDomains: async () => {
    const response = await api.get('/config/domains');
    return response.data;
  },

  listLLMTypes: async () => {
    const response = await api.get('/config/llm_types');
    return response.data;
  },

  listDataSourceTypes: async () => {
    const response = await api.get('/config/data_source_types');
    return response.data;
  },
  // Health
  health: async () => {
    const response = await api.get('/health');
    return response.data;
  },
  
  detailedHealth: async () => {
    const response = await api.get('/health/detailed');
    return response.data;
  },
};

export default apiService;
