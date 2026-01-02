# Math AI Agent 

A multimodal AI agent that solves math problems using:
- Text input
- Image OCR
- Audio speech recognition

---

## Architecture

```mermaid
graph TD
    UI[React Frontend]
    UI -->|POST /ask| API[FastAPI Backend]
    API --> Router
    Router --> TextFlow
    Router --> ImageFlow
    Router --> AudioFlow

    ImageFlow --> OCR[pytesseract OCR]
    AudioFlow --> ASR[Speech Recognition]

    TextFlow --> Parser
    OCR --> Parser
    ASR --> Parser

    Parser --> RouterAgent
    RouterAgent --> KB[Knowledge Base]
    KB --> VectorStore
    VectorStore --> FAISS
Setup
Clone repo
git clone https://github.com/<your-username>/math-ai-agent.git
cd math-ai-agent

Create env file
cp .env.example .env


Add your API keys in .env.

Run with Docker
docker compose up --build


Open:

http://localhost:7860/docs

API Usage
Mode	Field
text	mode=text, question="2+2"
image	mode=image, file=image.png
audio	mode=audio, file=audio.wav

---

#  Initialize Git Safely

In project root:

```bash
git init
git status
Add files carefully
git add .gitignore .env.example README.md backend frontend docker-compose.yml Dockerfile
git status


Check files — if .env is staged remove it:

git rm --cached .env