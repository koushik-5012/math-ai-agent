---
title: Math Professor AI
emoji: 🧮
colorFrom: indigo
colorTo: blue
sdk: docker
pinned: false
---

# Math Professor AI – Multimodal LLM Agent

A production-grade multimodal AI agent capable of solving mathematical problems from:

- 📝 Text input  
- 🖼️ Image OCR (Tesseract)  
- 🎤 Audio transcription (FFmpeg + SpeechRecognition)

Built with **FastAPI + Docker** and deployed on HuggingFace Spaces.

## Features

- Text / Image / Audio unified `/ask` API
- Automatic OCR and speech-to-text pipeline
- Vector retrieval support
- Dockerized runtime with system dependencies
- Production-grade backend using Uvicorn

## API

`POST /ask`

Form fields:

- `mode`: `text | image | audio`
- `question`: required for text
- `file`: required for image/audio