import streamlit as st
from rag_pipeline import RAGPipeline

st.set_page_config(page_title="Legal Document Search", layout="wide")

st.title("⚖️ Indian Legal Document Search System")
st.markdown("Compare 4 similarity methods for legal document retrieval using LangChain.")

# Initialize RAG pipeline
pipeline = RAGPipeline()

# Upload documents
st.sidebar.header("📤 Upload Legal Files")
uploaded_files = st.sidebar.file_uploader("Upload .txt files", type=["txt"], accept_multiple_files=True)

if uploaded_files:
    import os
    os.makedirs("uploaded", exist_ok=True)
    for file in uploaded_files:
        path = os.path.join("uploaded", file.name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(file.read().decode())
    st.sidebar.success("Files uploaded!")

# Load and embed documents
if st.sidebar.button("🚀 Load & Index Documents"):
    pipeline.reset()
    pipeline.load_documents()
    st.success("Documents loaded and indexed!")

# Query input
query = st.text_input("🔎 Enter your legal query:")
run_search = st.button("Search")

if query and run_search:
    st.markdown(f"## 🔍 Query: `{query}`")
    
    results_cosine = pipeline.query_cosine(query)
    results_euclidean = [doc for doc, _ in pipeline.query_euclidean(query)]
    results_mmr = pipeline.query_mmr(query)
    results_hybrid = [doc for doc, _ in pipeline.query_hybrid(query)]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("### 🧠 Cosine Similarity")
        for doc in results_cosine:
            st.markdown(f"✅ `{doc.metadata['source']}`\n\n> {doc.page_content[:300]}...")

    with col2:
        st.markdown("### 📐 Euclidean Distance")
        for doc in results_euclidean:
            st.markdown(f"✅ `{doc.metadata['source']}`\n\n> {doc.page_content[:300]}...")

    with col3:
        st.markdown("### 🌀 MMR (Diverse)")
        for doc in results_mmr:
            st.markdown(f"✅ `{doc.metadata['source']}`\n\n> {doc.page_content[:300]}...")

    with col4:
        st.markdown("### ⚖️ Hybrid Similarity")
        for doc in results_hybrid:
            st.markdown(f"✅ `{doc.metadata['source']}`\n\n> {doc.page_content[:300]}...")

    st.markdown("---")
    st.markdown("## 📊 Evaluation Metrics")

    # Simulated ground truth using source match
    if "gst" in query.lower():
        ground_truth = ["gst_act.txt"]
    elif "income" in query.lower():
        ground_truth = ["income_tax_act.txt"]
    elif "property" in query.lower():
        ground_truth = ["property_law.txt"]
    elif "court" in query.lower():
        ground_truth = ["court_judgments.txt"]
    else:
        ground_truth = []

    if ground_truth:
        metrics = pipeline.evaluate(query, ground_truth)
        st.dataframe(metrics)
    else:
        st.warning("Couldn't auto-detect ground truth. Manual labels needed for metric evaluation.")
