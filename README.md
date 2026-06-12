# ⚖️ LegalMind AI

## Multi-Agent Legal Reasoning System using RAG, Fine-Tuned LLMs, and NLI Verification

LegalMind AI is an AI-powered legal reasoning framework designed to generate grounded and explainable legal opinions by combining Retrieval-Augmented Generation (RAG), fine-tuned Large Language Models, and Natural Language Inference (NLI)-based verification.

The system follows a multi-agent architecture where specialized agents perform legal retrieval, legal reasoning, and verification to reduce hallucinations and improve reliability.

---

## 🚀 Features

* Retrieval-Augmented Generation (RAG)
* Multi-Agent Legal Reasoning
* Fine-Tuned Legal Language Model
* Hallucination Detection using NLI
* Explainable AI Pipeline
* Semantic Legal Search using FAISS
* PDF-Based Legal Document Analysis
* Streamlit Web Interface
* FastAPI Backend Support

---

## 🏗️ System Architecture

```text
User Query
    │
    ▼
┌─────────────────────┐
│ Retrieval Agent     │
│ FAISS + Embeddings  │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Lawyer Agent        │
│ Legal Reasoning     │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Verifier Agent      │
│ NLI Verification    │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Final Legal Opinion │
└─────────────────────┘
```

---

## 🧠 Multi-Agent Framework

### Lawyer Agent

Responsibilities:

* Legal issue identification
* Context-based legal analysis
* Legal reasoning generation
* Opinion drafting

### Verifier Agent

Responsibilities:

* Detect unsupported claims
* Detect contradictions
* Verify generated legal reasoning
* Reduce hallucinations

### Final Opinion Generator

Responsibilities:

* Combine verified reasoning
* Generate structured legal opinion
* Provide confidence assessment

---

## 🛠️ Technology Stack

| Component          | Technology                 |
| ------------------ | -------------------------- |
| Frontend           | Streamlit                  |
| Backend            | FastAPI                    |
| Vector Database    | FAISS                      |
| Embeddings         | Sentence Transformers      |
| Legal LLM          | TinyLlama Fine-Tuned Model |
| Verification Model | DeBERTa-v3 MNLI            |
| Deep Learning      | PyTorch                    |
| NLP Framework      | HuggingFace Transformers   |
| PDF Processing     | PyMuPDF                    |

---

## 📂 Project Structure

```text
LegalMind-AI/
│
├── app.py
├── api.py
├── legalmind_core.py
├── pdf_utils.py
├── Dockerfile
├── requirements.txt
├── README.md
│
├── data/
├── index/
├── cache/
├── models/
└── results/
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/SohamS7S/LegalMind-AI.git

cd LegalMind-AI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Streamlit Application

```bash
streamlit run app.py
```

---

## ▶️ Running the FastAPI Backend

```bash
uvicorn api:app --reload
```

---

## 📊 Example Query

```text
Can a doctor perform surgery without informed consent?
```

Example Output:

```text
FINAL LEGAL OPINION

Issue:
Whether surgery without informed consent may create legal liability.

Legal Analysis:
...

Verification Status:
Supported

Confidence Level:
High
```

---

## 🔍 Retrieval-Augmented Generation Pipeline

1. User submits legal query.
2. Query embeddings are generated.
3. Relevant legal chunks are retrieved from FAISS.
4. Lawyer Agent generates legal reasoning.
5. Verifier Agent validates claims using NLI.
6. Final legal opinion is generated.

---

## 🎓 Academic Information

**Project Title**

LegalMind AI: Multi-Agent Legal Reasoning System using Retrieval-Augmented Generation and Hallucination Verification

**Student**

Soham Shelar (DS24M32)

**Program**

Master of Technology (Data Science)

**University**

Savitribai Phule Pune University

**Guide**

Dr. Manisha Bharati

---

## 📌 Future Improvements

* Advanced Legal Citation Verification
* Court Judgment Summarization
* Multilingual Legal Support
* Enhanced Explainability Dashboard
* Real-Time Legal Knowledge Updates

---

## ⚠️ Disclaimer

This project is intended for educational and research purposes.

The generated legal opinions should not be considered professional legal advice. Users should consult qualified legal professionals before making legal decisions.

---

## ⭐ Support

If you found this project useful:

* Star the repository
* Fork the project
* Share feedback and suggestions

---
