
interface WelcomeStepProps {
  onNext: () => void;
}

export default function WelcomeStep({ onNext }: WelcomeStepProps) {
  return (
    <div className="text-center">
      <div className="text-6xl mb-6">🧠</div>
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
        Bem-vindo ao EvoBrain
      </h2>
      <p className="text-gray-600 dark:text-gray-400 mb-6">
        Sistema de previsão 24/7 com RL + Neuroevolution + Memória
      </p>
      <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 mb-6 text-left">
        <h3 className="font-semibold mb-2">O que vamos configurar:</h3>
        <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
          <li>✓ 🧠 LLM (Ollama, Llama.cpp ou OpenAI)</li>
          <li>✓ 📡 Fonte de dados (API REST, WebSocket, Bac Bo)</li>
          <li>✓ 🎯 Domínio de aplicação (ações personalizadas)</li>
          <li>✓ 🤖 Agentes e parâmetros de evolução</li>
        </ul>
      </div>
      <button
        onClick={onNext}
        className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
      >
        Começar Configuração
      </button>
    </div>
  );
}
