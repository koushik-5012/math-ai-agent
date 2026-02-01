🧮 Math Professor AI – Multimodal RAG + LLM Agent

A production-style multimodal AI system that solves mathematical problems from *text, images, or audio* using a Retrieval-Augmented Generation (RAG) pipeline with guardrails and human-in-the-loop safety.

Live Demo: https://math-ai-agent-8wmi.onrender.com/ui

---

# Problem Statement

Students frequently share math problems as:

•⁠  ⁠typed text
•⁠  ⁠screenshots/photos
•⁠  ⁠spoken audio

Traditional solvers only accept text input.

*Goal:*  
Build a unified backend system that can:

1.⁠ ⁠Parse multimodal input (OCR + Speech → Text)
2.⁠ ⁠Retrieve relevant knowledge (vector search)
3.⁠ ⁠Use LLM reasoning for step-by-step solutions
4.⁠ ⁠Enforce strict math-only guardrails
5.⁠ ⁠Provide transparent reasoning trace

---

# Features

## Multimodal Input
•⁠  ⁠📝 Text questions
•⁠  ⁠🖼️ Image OCR (Tesseract)
•⁠  ⁠🎤 Audio transcription (FFmpeg + SpeechRecognition)

## AI Pipeline
•⁠  ⁠OpenAI embeddings for semantic retrieval
•⁠  ⁠FAISS local vector database
•⁠  ⁠Retrieval-Augmented Generation (RAG)
•⁠  ⁠Step-by-step reasoning via LLM
•⁠  ⁠Guardrails to block non-math queries

## Engineering
•⁠  ⁠FastAPI backend
•⁠  ⁠Dockerized runtime
•⁠  ⁠Stateless deployment
•⁠  ⁠REST API
•⁠  ⁠Frontend UI
•⁠  ⁠Cloud deployable (Render / HuggingFace Spaces)

---

# Architecture

## High-Level Flow

```mermaid
flowchart TD

A[User Input<br/>Text/Image/Audio]
B[OCR / Speech To Text]
C[Guardrails Check]
D[Embeddings]
E[FAISS Vector Search]
F[Context Injection]
G[LLM Reasoning (MCP)]
H[Structured JSON Answer]
I[Frontend UI]

A --> B --> C
C -->|valid| D --> E --> F --> G --> H --> I
C -->|invalid| I
Tech Stack

Backend
	•	FastAPI
	•	Uvicorn
	•	Python

AI / ML
	•	OpenAI API (LLM + Embeddings)
	•	FAISS (vector search)
	•	Tesseract OCR
	•	SpeechRecognition
	•	FFmpeg

Infra
	•	Docker
	•	Render / HuggingFace Spaces
	•	Linux runtime
#Project Structure 
backend/
  app/
    routers/        # API endpoints
    services/
      ocr.py
      rag.py
      mcp.py
      vector_store.py
      guardrails.py
frontend/
Dockerfile
requirements.txt

1.Setup & Run
git clone <repo>
cd math-ai-agent

2.Install dependencies
pip install -r requirements.txt

3. Set environment variable
export OPENAI_API_KEY=your_key
4. Run locally
uvicorn app.main:app --reload
Open:
http://localhost:8000/ui

⸻

 Docker Run
docker build -t math-ai-agent .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key math-ai-agent

⸻

 API

POST /ask

Multipart form:
Field
Type
Description
question
string
text input
image
file
JPG/PNG
audio
file
WAV

{
  "detected_text": "...",
  "answer": "...",
  "steps": [...],
  "confidence": 0.95,
  "agent_trace": [...]
}

Guardrails

System blocks:
	•	politics
	•	news
	•	general knowledge
	•	non-math queries

Only math-related problems reach the LLM.

Benefits:
	•	lower API cost
	•	higher accuracy
	•	safer outputs

Design Decisions

Why FAISS (not Pinecone)?
	•	free
	•	local
	•	no latency
	•	small knowledge base
	•	avoids paid limits

Why RAG?
	•	improves factual consistency
	•	reduces hallucinations
	•	cheaper than pure LLM calls

Why Guardrails?
	•	prevents misuse
	•	reduces cost
	•	enforces scope

Limitations
	•	Tesseract OCR may fail on complex math layouts
	•	handwritten math not supported
	•	large knowledge bases need external vector DB
	•	not a symbolic math engine

Production alternative:
	•	MathPix OCR
	•	Pinecone/Weaviate
	•	SymPy integration

Future Improvements
	•	Math-specific OCR (MathPix)
	•	Symbolic solving with SymPy
	•	Step verification
	•	Confidence scoring
	•	User editable OCR
	•	Fine-tuned math LLM

Author

Built end-to-end:
	•	backend
	•	RAG pipeline
	•	multimodal ingestion
	•	Docker infra
	•	deployment
	•	guardrails

Designed as a production-style AI system rather than a demo notebook.

Demo

Live UI: https://math-ai-agent-8wmi.onrender.com/ui/