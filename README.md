
# LegalMind

AI-powered multi-agent legal reasoning system.

## Features

- QLoRA Fine-Tuned Mistral
- FAISS Retrieval-Augmented Generation (RAG)
- Lawyer Agent
- Verifier Agent
- Judge Agent
- Streamlit Interface

## Architecture

User Query
↓
FAISS Retriever
↓
Lawyer Agent
↓
Verifier Agent
↓
Judge Agent
↓
Final Legal Opinion

## Evaluation

Professional Legal Scenario Success Rate: 96.7%

## Run

streamlit run app.py
