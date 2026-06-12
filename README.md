⚖️ LegalMind AI
Multi-Agent Legal Reasoning Framework Leveraging Fine-Tuning of LLMs and RAG to Reduce Hallucinations

LegalMind AI is a production-ready Multi-Agent Legal Reasoning System designed for Indian legal research and analysis.

The system combines:

Retrieval-Augmented Generation (RAG)
QLoRA Fine-Tuned Large Language Models
Natural Language Inference (NLI)
Multi-Agent Architecture
Hallucination Detection and Verification

to generate legally grounded, explainable, and verifiable legal opinions.

🎯 Problem Statement

Large Language Models frequently hallucinate:

Fake case laws
Incorrect statutory references
Unsupported legal conclusions
Fabricated legal doctrines

These issues become critical in legal applications where factual correctness and evidential grounding are mandatory.

LegalMind AI addresses this challenge through a multi-agent pipeline that retrieves legal evidence, generates legal reasoning, verifies every claim, and synthesizes a final legal opinion.

🏗 System Architecture
User Query / PDF Upload
          │
          ▼
 ┌──────────────────────┐
 │ Retrieval Layer      │
 │ (RAG + FAISS)        │
 └──────────────────────┘
          │
          ▼
 ┌──────────────────────┐
 │ Lawyer Agent         │
 │ Fine-Tuned LLM       │
 └──────────────────────┘
          │
          ▼
 ┌──────────────────────┐
 │ Verifier Agent       │
 │ NLI Verification     │
 └──────────────────────┘
          │
          ▼
 ┌──────────────────────┐
 │ Judge Agent          │
 │ Final Legal Opinion  │
 └──────────────────────┘
          │
          ▼
       Streamlit UI
🚀 Key Features
🔍 Retrieval-Augmented Generation (RAG)
Semantic retrieval from Indian legal corpus
Dense vector search using FAISS
Cross-encoder re-ranking
Context grounding before generation
⚖️ Lawyer Agent
Fine-tuned Legal LLM
Generates structured legal analysis
Context-aware reasoning
Hallucination-resistant prompting
🧠 Verifier Agent
NLI-based verification
Detects unsupported claims
Detects contradictions
Detects fabricated legal references
👨‍⚖️ Judge Agent
Synthesizes final legal opinion
Assigns confidence score
Generates verification status
Produces explainable output
📄 PDF Analysis
Upload legal documents
Automatic text extraction
Query uploaded documents
Integrated with RAG pipeline
🌐 Web Application
Streamlit Frontend
FastAPI Backend
Dark Professional UI
Multi-Tab Explainable Results
🛠 Technology Stack
Layer	Technology
Frontend	Streamlit
Backend	FastAPI
Vector Search	FAISS
Embeddings	all-mpnet-base-v2
Re-Ranker	ms-marco-MiniLM-L-6-v2
Legal LLM	TinyLlama / Fine-Tuned Legal Model
Verification	DeBERTa-v3 MNLI-FEVER-ANLI
PDF Processing	PyMuPDF
Training	QLoRA
Deep Learning	PyTorch
NLP	HuggingFace Transformers
📚 Dataset
IL-TUR Dataset

Indian Legal Text Understanding and Reasoning Dataset

Contains:

42,465 Indian Legal Cases
Issue Identification
Judgment Reasoning
Outcome Prediction
Doctrine Explanation

The dataset combines:

ILDC
CJPE

into a unified legal reasoning benchmark.

🧠 Multi-Agent Pipeline
Agent 1: Lawyer Agent

Responsibilities:

Legal Issue Identification
Legal Reasoning
Context-Based Analysis
Preliminary Assessment

Input:

Question + Retrieved Context

Output:

Legal Analysis
Agent 2: Verifier Agent

Responsibilities:

Claim Verification
Hallucination Detection
Contradiction Detection
Legal Sanity Checks

Model:

MoritzLaurer/deberta-v3-base-mnli-fever-anli

Output:

Supported
Review Required
Contradiction Detected
Agent 3: Judge Agent

Responsibilities:

Final Legal Opinion
Confidence Scoring
Opinion Synthesis
Professional Formatting

Output:

FINAL LEGAL OPINION
📂 Project Structure
LegalMind/
│
├── app.py
├── api.py
├── legalmind_core.py
├── pdf_utils.py
├── requirements.txt
├── Dockerfile
├── README.md
│
├── data/
│   ├── legalmind_cases.jsonl
│   └── chunks.jsonl
│
├── index/
│   └── faiss_index.bin
│
├── cache/
│
├── models/
│
└── results/
⚙️ Installation

Clone Repository

git clone https://github.com/SohamS7S/LegalMind-AI.git

cd LegalMind-AI

Install Dependencies

pip install -r requirements.txt
▶️ Run Streamlit Application
streamlit run app.py
▶️ Run FastAPI Backend
uvicorn api:app --reload
📷 Screenshots
Home Page
Legal Query Input
PDF Upload
Multi-Agent Analysis
Retrieved Context
Top Retrieved Legal Chunks
Explainable Evidence
Lawyer Agent
Legal Analysis
Context Grounding
Verifier Agent
Hallucination Detection
Support Verification
Final Legal Opinion
Verified Output
Confidence Score
🎯 Example Query
A doctor performed surgery without obtaining informed consent.
Could this amount to medical negligence or battery?

Output:

FINAL LEGAL OPINION

Issue:
...

Legal Analysis:
...

Verification Status:
Supported

Confidence Level:
High
📈 Research Contributions

✅ Indian Legal RAG System

✅ Multi-Agent Legal Reasoning

✅ QLoRA Fine-Tuning Pipeline

✅ Hallucination Detection using NLI

✅ Explainable Legal AI

✅ Streamlit + FastAPI Deployment

✅ PDF-Based Legal Analysis

👨‍🎓 Academic Information

Author: Soham Sachin Shelar

Roll No: DS24M32

Program: Master of Technology (Data Science)

University: Savitribai Phule Pune University

Guide: Dr. Manisha Bharati

Academic Year: 2025–26

⚠️ Disclaimer

LegalMind AI is an AI-assisted legal research system intended for educational and research purposes.

The generated outputs should not be considered professional legal advice. Users should consult qualified legal practitioners before making legal decisions.

⭐ If you found this project useful

Please consider giving this repository a star. It helps support future research and development in Explainable Legal AI.

⭐ Star the repository
🍴 Fork the project
📢 Share with researchers and developers
