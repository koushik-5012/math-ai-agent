# Math AI Agent

A multimodal AI system that solves math problems using:

- Text input
- Image OCR
- Audio speech recognition

---

## Architecture

```mermaid
graph TD
    UI[React Frontend]
    API[FastAPI Backend]
    Router
    TextFlow
    ImageFlow
    AudioFlow
    OCR[Pytesseract OCR]
    ASR[Speech Recognition]
    Parser
    RouterAgent
    KB[Knowledge Base]
    VectorStore[FAISS Vector Store]

    UI -->|POST /ask| API
    API --> Router
    Router --> TextFlow
    Router --> ImageFlow
    Router --> AudioFlow

    ImageFlow --> OCR
    AudioFlow --> ASR

    TextFlow --> Parser
    OCR --> Parser
    ASR --> Parser

    Parser --> RouterAgent
    RouterAgent --> KB
    KB --> VectorStore

Setup
Clone repository
git clone https://github.com/koushik-5012/math-ai-agent.git
cd math-ai-agent

Run Backend (Docker)
docker compose up --build


Open API docs:

http://localhost:7860/docs

API Usage

Endpoint:

POST /ask


Form fields:

Field	Type	Description
mode	string	text / image / audio
question	string	text input (for text mode)
file	file	image or audio file
Tech Stack

FastAPI

FAISS

React

Docker

Pytesseract

SpeechRecognition


---

## Step 3 — Commit and push

```bash
git add README.md
git commit -m "Fix README mermaid architecture diagram"
git push