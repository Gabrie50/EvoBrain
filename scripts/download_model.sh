#!/bin/bash
# Script para baixar modelo LLM

MODEL=${1:-"llama3.2"}

echo "📥 Baixando modelo: $MODEL"

if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama não encontrado. Instale com: curl -fsSL https://ollama.com/install.sh | sh"
    exit 1
fi

ollama pull $MODEL

echo "✅ Modelo $MODEL baixado com sucesso!"
echo "   Use com: ollama run $MODEL"
