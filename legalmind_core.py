
import os
import json
import pickle
import faiss
import numpy as np
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    pipeline
)

from peft import PeftModel
from sentence_transformers import SentenceTransformer


# =========================
# PATHS
# =========================

PROJECT_ROOT = "/content/drive/MyDrive/LegalMind"

MODEL_PATH = f"{PROJECT_ROOT}/models/lawyer_qlora_mistral"

FAISS_INDEX_PATH = f"{PROJECT_ROOT}/index/faiss_index.bin"

METADATA_PATH = f"{PROJECT_ROOT}/index/faiss_metadata.jsonl"


# =========================
# LOAD MODEL
# =========================

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

BASE_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

tokenizer.pad_token = tokenizer.eos_token

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    quantization_config=bnb_config,
    device_map="auto",
    torch_dtype=torch.float16
)

model = PeftModel.from_pretrained(
    base_model,
    MODEL_PATH
)

model.eval()


# =========================
# LOAD RAG
# =========================

from sentence_transformers import (
    SentenceTransformer,
    CrossEncoder
)

index = faiss.read_index(FAISS_INDEX_PATH)

with open(METADATA_PATH, "r") as f:
    metadata = [json.loads(line) for line in f]

with open(
    f"{PROJECT_ROOT}/cache/chunk_text_by_id.pkl",
    "rb"
) as f:
    chunk_text_map = pickle.load(f)

# Embedding model
embedder = SentenceTransformer(
    "sentence-transformers/all-mpnet-base-v2"
)

# Cross-encoder reranker
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


# =========================
# RETRIEVAL
# =========================

# =========================
# RETRIEVAL
# =========================

def clean_context(text):

    replacements = {
        "companypany": "company",
        "companytract": "contract",
        "companyrt": "court",
        "numberice": "notice",
        "companymitted": "committed",
        "companysider": "consider",
        "companynection": "connection",
        "companypetition": "competition",
        "companynsel": "counsel",
        "companynviction": "conviction",
        "companymission": "commission",
        "companycontext": "context",
        "companycompensation": "compensation",
        "companycontinued": "continued",
        "companycurrent": "current",
        "companylateral": "collateral",
        "companysent": "consent",
        "companyduct": "conduct",
        "companyponent": "component",
        "number": "not"
    }

    for bad, good in replacements.items():
        text = text.replace(bad, good)

    import re

    text = re.sub(r'company[a-zA-Z]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text


def retrieve_top_k(query, k=10):

    query_embedding = embedder.encode(
        [query],
        normalize_embeddings=True
    )

    distances, indices = index.search(
        np.array(query_embedding),
        k
    )

    results = []
    seen = set()

    for idx, score in zip(indices[0], distances[0]):

        if idx >= len(metadata):
            continue

        item = metadata[idx]

        chunk_id = item.get("chunk_id")

        if chunk_id not in chunk_text_map:
            continue

        text = chunk_text_map[chunk_id]

        # Skip tiny chunks
        if len(text) < 200:
            continue

        # Remove duplicates
        if text in seen:
            continue

        seen.add(text)

        results.append(text)

    if not results:
        return "No relevant legal context found."

    # =====================
    # RERANKING
    # =====================

    pairs = [(query, text) for text in results]

    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(results, scores),
        key=lambda x: x[1],
        reverse=True
    )

    results = [x[0] for x in ranked[:5]]

    # =====================
    # CLEAN RESULTS
    # =====================

    cleaned_results = []

    for r in results:

        r = clean_context(r)

        r = r.replace("\n", " ")

        r = " ".join(r.split())

        cleaned_results.append(r[:700])

    return "\n\n".join(cleaned_results)
# =========================
# LAWYER AGENT
# =========================
import re
import torch

def lawyer_agent(question, context):

    prompt = f"""
You are a Senior Legal Research Associate assisting a practicing lawyer.

Retrieved Context:
{context}

User Query:
{question}

IMPORTANT:

Your task is NOT to summarize the retrieved case.

Your task is to analyze the USER'S legal problem using the retrieved materials.

Produce the following sections:

LEGAL ISSUES:
- Identify the legal issues raised by the user's query.

RELEVANT LEGAL PRINCIPLES:
- Extract only principles supported by the retrieved materials.

MISSING FACTS:
- Identify facts that would be required before providing legal advice.

PRELIMINARY ASSESSMENT:
- Explain how the retrieved materials may apply to the user's problem.

RULES:

1. Do NOT summarize the retrieved case.
2. Do NOT narrate procedural history.
3. Do NOT describe plaintiffs, defendants, judges, appeals, or litigation history.
4. Focus on legal issues and legal principles.
5. If the retrieved materials do not support a principle, write:
   "Retrieved materials do not establish this issue."
6. Never invent statutes, sections, constitutional provisions, precedents, or legal doctrines.
7. Do NOT cite legal provisions unless explicitly present in the retrieved materials.
8. Keep the response concise and structured.

Generate the response now.
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=2048
    )

    inputs = {
        k: v.to(model.device)
        for k, v in inputs.items()
    }

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=220,
            do_sample=False,
            repetition_penalty=1.15,
            pad_token_id=tokenizer.eos_token_id
        )

    response = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )
    response = response.replace(prompt, "").strip()
    foreign_terms = [
    "uniform commercial code",
    "digital millennium copyright act",
    "economic espionage act",
    "computer fraud and abuse act",
    "u.c.c.",
    "first amendment",
    "u.s. constitution",
    "united states constitution",
    "american law",
    "federal court",
    "supreme court of the united states",
    "copyright act of 1976",
    "u.s.c.",
    "federal statute",
    "state law",
    "california",
    "new york law"
    ]

    for term in foreign_terms:
        if term in response.lower():
            return """
    LEGAL ISSUES:
    Retrieved materials do not clearly establish the legal issues.

    RELEVANT LEGAL PRINCIPLES:
    Retrieved materials do not establish this issue.

    MISSING FACTS:
    Additional evidence and legal authorities are required.

    PRELIMINARY ASSESSMENT:
    The generated response relied on unsupported legal authorities and has been rejected.

    Confidence:
    Low
    """.strip()



    # Template leakage protection
    if (
        "<reasoning" in response.lower()
        or
        "<legal opinion" in response.lower()
        or
        "<analysis" in response.lower()
    ):
        return """
    LEGAL ISSUES:
    Insufficient legal analysis generated.

    RELEVANT LEGAL PRINCIPLES:
    Insufficient legal analysis generated.

    MISSING FACTS:
    Additional facts required.

    PRELIMINARY ASSESSMENT:
    Low confidence response generated.
    """.strip()

    # Remove unwanted headings
    response = response.replace("Explanation:", "")
    response = response.replace("Reasoning:", "")
    response = response.replace("Legal Analysis:", "")

    # Remove confidence generated by model
    response = re.sub(
        r"Confidence:\s*(High|Medium|Low)",
        "",
        response,
        flags=re.IGNORECASE
    )

    # Detect case-summary behavior
    bad_patterns = [
        "the appellant",
        "the respondent",
        "the plaintiff",
        "the defendant",
        "the high court",
        "the supreme court",
        "the trial court",
        "the petitioner"
    ]

    summary_score = 0

    for pattern in bad_patterns:
        summary_score += response.lower().count(pattern)

    if summary_score > 1:

        return """
    LEGAL ISSUES:
    Retrieved materials do not clearly establish the legal issues.

    RELEVANT LEGAL PRINCIPLES:
    Insufficient evidence from retrieved materials.

    MISSING FACTS:
    Additional facts and authorities are required.

    PRELIMINARY ASSESSMENT:
    The retrieved content appears highly case-specific and cannot reliably support a generalized legal analysis.

    Confidence:
    Low
    """.strip()

    response = re.sub(r"\n{3,}", "\n\n", response)

    return response.strip()
# =========================
# VERIFIER
# =========================

nli_model = pipeline(
    "text-classification",
    model="MoritzLaurer/deberta-v3-base-mnli-fever-anli"
)


def verifier_agent(question, lawyer_answer, context):

    issues = []

    # Clean response first
    cleaned_answer = lawyer_answer.replace("[INST]", "")
    cleaned_answer = cleaned_answer.replace("[/INST]", "")

    import re

    claims = re.split(
        r'[.;\n]',
        cleaned_answer
    )

    for claim in claims:

        claim = claim.strip()

        # Skip tiny fragments
        if len(claim) < 40:
            continue

        # Skip formatting sections
        if any(x in claim.lower() for x in [
            "legal position",
            "applicable law",
            "explanation",
            "conclusion",
            "confidence",
            "issue",
            "legal issues",
            "relevant legal principles",
            "missing facts",
            "preliminary assessment"
        ]):
            continue

        try:

            result = nli_model(
                f"{claim} </s> {context[:1000]}"
            )[0]

            label = result["label"]
            score = result["score"]

            # Strong contradiction
            if label == "contradiction" and score > 0.80:

                issues.append(
                    f"❌ Possible contradiction: {claim}"
                )

            # Strong unsupported statement
            elif label == "neutral" and score > 0.95:

                issues.append(
                    f"⚠️ Unsupported claim: {claim}"
                )

        except Exception:
            continue

    # =====================================
    # Unsupported Legal Reference Checks
    # =====================================

    if (
        "section 11" in cleaned_answer.lower()
        and "section 11" not in context.lower()
    ):
        issues.append(
            "⚠️ Unsupported statutory reference detected: Section 11"
        )

    for keyword in [
        "section",
        "article",
        "ipc",
        "crpc",
        "constitution"
    ]:

        if (
            keyword in cleaned_answer.lower()
            and keyword not in context.lower()
        ):

            issues.append(
                f"⚠️ Possible unsupported legal reference: {keyword}"
            )

    import re

    sections = re.findall(
        r"section\s+\d+[a-zA-Z]*",
        cleaned_answer.lower()
    )

    for sec in sections:

        if sec not in context.lower():

            issues.append(
                f"⚠️ Unsupported statutory reference: {sec}"
            )

    # =====================================
    # Legal Sanity Checks
    # =====================================

    if (
        "minor can enter into valid contracts"
        in cleaned_answer.lower()
        or
        "minor can enter into valid contract"
        in cleaned_answer.lower()
    ):

        issues.append(
            "⚠️ Possible legal error: minors generally lack contractual capacity under Indian law."
        )

    # =====================================
    # Final Result
    # =====================================

    if not issues:

        return (
            "Answer appears supported by retrieved context."
        )

    return "\n".join(issues[:3])


# =========================
# JUDGE
# =========================

def judge_agent(
    question,
    lawyer_answer,
    verifier_report
):

    # If verifier found serious issues
    if (
    "contradiction" in verifier_report.lower()
    or
    "unsupported" in verifier_report.lower()
    or
    "possible legal error" in verifier_report.lower()
    ):

        return f"""
FINAL LEGAL OPINION

⚠️ Verification Warning

The generated answer contains claims that are not fully
supported by retrieved legal materials.

Verifier Findings:
{verifier_report}

Lawyer Answer:
{lawyer_answer}

Recommendation:
Manual legal review required before relying on this opinion.
""".strip()

    # Normal path
    verification_status = "Supported"
    confidence = "High"

    final = f"""
FINAL LEGAL OPINION

Issue:
{question}

Legal Analysis:
{lawyer_answer}

Verification Status:
{verification_status}

Confidence Level:
{confidence}

Professional Note:
This opinion is based on retrieved legal materials and automated verification.
Final legal advice should consider complete facts, applicable statutes,
and current judicial precedents.
"""

    return final.strip()

# =========================
# MASTER PIPELINE
# =========================

def run_legalmind(question):

    context = retrieve_top_k(question)

    lawyer = lawyer_agent(
        question,
        context
    )

    verifier = verifier_agent(
        question,
        lawyer,
        context
    )

    final = judge_agent(
        question,
        lawyer,
        verifier
    )

    return {
        "context": context,
        "lawyer": lawyer,
        "verifier": verifier,
        "final": final
    }
