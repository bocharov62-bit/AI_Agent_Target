#!/bin/bash
# Быстрое развертывание одной командой

cd ~ && \
git clone https://github.com/bocharov62-bit/AI_Agent_Target.git landing-assistant && \
cd landing-assistant/landing_redesign_assistant && \
cp .env.example .env && \
echo "GIGACHAT_CREDENTIALS=your_key_here" >> .env && \
mkdir -p output && \
chmod +x deploy.sh && \
./deploy.sh

