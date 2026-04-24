#!/bin/bash

echo "Starting Our Br00d Setup..."

# 1. Check for Ollama
if ! command -v ollama &> /dev/null
then
    echo "Ollama could not be found. Please install it from https://ollama.com/"
    exit
fi

# 2. Pull Models
echo "Pulling LLM models (Llama 3.1 8B and Mistral-Nemo)..."
ollama pull llama3.1:8b
ollama pull mistral-nemo

# 3. Build Containers
echo "Building Docker containers..."
docker compose build

echo "Setup complete! To start the system, run:"
echo "docker compose up"
echo ""
echo "After starting, run the audio bridge on your Mac:"
echo "python3 audio_bridge/bridge.py"
