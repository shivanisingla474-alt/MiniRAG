import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
from dotenv import load_dotenv

import streamlit as st
import json

from src.pdf_processor import PDFProcessor
from src.chunker import TextChunker
from src.embedder import Embedder
from src.vector_store import VectorStore
from src.retriever import Retriever
from src.llm_service import LLMService
from src.evaluator import Evaluator


# ================= UI =================
st.set_page_config(page_title="MiniRAG", layout="wide")
st.title("📄 MiniRAG - MSA Contract QA System")


# ================= INIT =================
pdf_processor = PDFProcessor()
chunker = TextChunker()
embedder = Embedder()
vector_store = VectorStore()
retriever = Retriever(vector_store)

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


llm = LLMService(API_KEY)
evaluator = Evaluator(API_KEY)

if "ready" not in st.session_state:
    st.session_state.ready = False


# ================= SIGNAL =================
def get_signal(score):

    if score >= 0.70:
        return "🟢 Strong"
    elif score >= 0.60:
        return "🟡 Good"
    elif score >= 0.50:
        return "🟠 Weak"
    else:
        return "🔴 Poor"


# ================= UPLOAD =================
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:

    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    paragraphs = pdf_processor.extract_text("temp.pdf")

    chunks, metadatas = chunker.chunk_text(paragraphs)

    embeddings = embedder.embed_chunks(chunks)

    vector_store.reset()
    vector_store.add_chunks(chunks, embeddings, metadatas)

    st.session_state.ready = True
    st.success("PDF processed successfully")


# ================= QUESTION =================
question = st.text_input("Ask a question")

if question and st.session_state.ready:

    results = retriever.retrieve(embedder.embed_text(question))

    top_chunks = [r["chunk"] for r in results]

    answer = llm.generate_answer(question, top_chunks)

    st.subheader("📊 Similarity Report")

    st.table([
        {
            "Rank": r["rank"],
            "Location": f"Page {r['page']}, Para {r['para']}",
            "Similarity Score": r["similarity"],
            "Score Signal": get_signal(r["similarity"]),
            "Chunk Preview": r["chunk"][:120]
        }
        for r in results
    ])

    st.subheader("💡 Answer")
    st.write(answer)


# ================= EVALUATION =================
st.subheader("🧪 Evaluation (10 Questions)")

if st.button("Run Evaluation"):

    if not st.session_state.ready:
        st.warning("Upload PDF first")
        st.stop()

    with open("data/ground_truth.json") as f:
        data = json.load(f)

    table = []

    match = 0
    partial = 0
    no_match = 0

    for item in data:

        results = retriever.retrieve(embedder.embed_text(item["question"]))

        system_answer = llm.generate_answer(
            item["question"],
            [r["chunk"] for r in results]
        )

        judge = evaluator.judge_answer(
            item["answer"],
            system_answer
        )

        label = judge["label"].lower()

        if "partial" in label:
            label = "Partial Match"
            partial += 1
        elif "no" in label:
            label = "No Match"
            no_match += 1
        else:
            label = "Match"
            match += 1

        table.append({
            "Category": item.get("category", item["question"]),
            "Judgement": label,
            "Reason": judge["reason"]
        })

    st.subheader("📊 Evaluation Table")
    st.table(table)

    total = len(table)

    accuracy = round((match + 0.5 * partial) / total * 100, 2)

    st.subheader("📈 Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Match", match)
    col2.metric("Partial", partial)
    col3.metric("No Match", no_match)

    st.success(f"Overall Accuracy: {accuracy}%")