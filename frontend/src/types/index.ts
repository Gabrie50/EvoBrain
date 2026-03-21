export interface Agent { id: number; name: string; personality: string; traits: string[]; mbti: string; accuracy: number; total_uso: number; fitness: number; specializations: string[]; acertos?: number; erros?: number; }
export interface Prediction { prediction: 'BANKER' | 'PLAYER'; confidence: number; votes: { BANKER: number; PLAYER: number; }; agents_active: number; timestamp: number; status?: string; }
export interface SimulationStats { active_agents: number; predictions_made: number; correct_predictions: number; accuracy: number; history_size: number; neuroevolution: { generation: number; best_fitness: number; population_size: number; }; recent_predictions: Prediction[]; }
export interface GenerationStats { total_agents: number; pending: number; created_last_minute: number; }
export interface SystemStats { status: string; simulation: SimulationStats; generation: GenerationStats; uptime: number; llm_connected: boolean; }
