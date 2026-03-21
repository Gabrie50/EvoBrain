#!/bin/bash
# Script para iniciar Ollama

echo "🚀 Iniciando Ollama..."

# Verifica se Ollama está instalado
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama não encontrado. Instale com: curl -fsSL https://ollama.com/install.sh | sh"
    exit 1
fi

# Inicia Ollama em background
ollama serve &
OLLAMA_PID=$!

echo "✅ Ollama iniciado (PID: $OLLAMA_PID)"
echo "⏳ Aguardando serviço..."

# Aguarda serviço
sleep 5

# Baixa modelo padrão
ollama pull llama3.2

echo "✅ Ollama pronto para uso!"
echo "   Modelo: llama3.2"
echo "   API: http://localhost:11434"
