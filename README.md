# 📄 MiniRAG - Contract Question Answering System

## 1. Overview

This project is a Retrieval-Augmented Generation (RAG) system designed to answer questions from a Master Service Agreement (MSA) document.

The system follows a full pipeline:
PDF → Text Extraction → Chunking → Embedding → Vector Search → LLM Answering → Evaluation

The goal is not just answering questions, but also showing **where the answer came from (page + paragraph level traceability)**.

---

## 2. Problem Statement

Legal contracts are long, structured, and repetitive. Searching manually is slow and error-prone.

This system helps:
- Extract relevant clauses
- Retrieve supporting context
- Generate grounded answers using LLMs
- Evaluate answer correctness automatically

---

## 3. Dataset (MSA Document)

The system uses a Master Service Agreement (MSA) containing clauses such as:
- Payment terms
- Late payment penalties
- Tax responsibilities
- Intellectual property rights
- Termination conditions
- Liability limitations

Each clause is structured across pages and paragraphs.

---

## 4. PDF Processing Strategy

We use PyMuPDF (`fitz`) for extraction.

Each paragraph is stored with metadata:

- Page number
- Paragraph number
- Text content

This enables traceable retrieval instead of raw text chunks.

---

## 5. Chunking Strategy

We use a sliding window chunking approach:

- Chunk size: 800 characters  
- Overlap: 200 characters  

### Reasoning:
Legal clauses often span multiple lines. Fixed-size chunking ensures:
- Context continuity
- Reduced information loss
- Better embedding stability

---

## 6. Embedding Model

We use:

### Sentence Transformer Model:
`BAAI/bge-small-en-v1.5`

### Why this model:
- Lightweight and fast for CPU execution
- Strong semantic understanding for English legal text
- Optimized for retrieval tasks (not just classification)
- Produces normalized embeddings suitable for cosine similarity search

---

## 7. Vector Database

We use **ChromaDB (Persistent Mode)**.

### Why ChromaDB:
- Simple integration
- Fast similarity search
- Stores embeddings + metadata together
- Suitable for prototype and production-level RAG systems

---

## 8. Retrieval Strategy

We use cosine similarity search with Top-K = 5.

Each retrieved chunk includes:
- Similarity score
- Page number
- Paragraph number
- Original text snippet

This ensures transparency in retrieval.

---

## 9. LLM for Answer Generation

We use OpenRouter API with:

### Model:
`meta-llama/llama-3.3-70b-instruct`

### Why this model:
- Strong reasoning capability
- Good instruction following
- Reliable for grounded QA tasks
- Works well with structured context prompts

### Prompt Strategy:
- Strict “answer only from context” constraint
- No external knowledge allowed
- Fallback: “Not found in document”

---

## 10. Evaluation Strategy

We use an **LLM-as-a-Judge approach**.

Each generated answer is compared against ground truth using:
- Match
- Partial Match
- No Match

### Accuracy Formula:
( Match + 0.5 × Partial Match ) / Total Questions

This reflects partial correctness rather than binary scoring.

---

## 11. UI (Streamlit)

The interface includes:

- PDF Upload
- Question Input
- Similarity Report (Ranked results)
- Page + Paragraph mapping
- Score Signal visualization
- Evaluation dashboard

---

## 12. Design Decisions

- Sentence-level metadata retained for traceability
- Embedding-based retrieval instead of keyword search for semantic understanding
- Lightweight architecture to ensure fast execution on CPU
- Evaluation included to measure real system performance, not just correctness

---

## 13. Limitations

- Retrieval quality depends on embedding model limitations
- Legal clauses with very similar wording may overlap
- No reranker layer (kept intentionally lightweight for assignment scope)

---


## 14. Run Instructions

```bash
pip install -r requirements.txt
streamlit run app.py