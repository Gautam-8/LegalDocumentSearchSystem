from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Tuple, Dict
import os
from collections import defaultdict
import numpy as np 

class RAGPipeline:
    def __init__(self, data_dir="uploaded", persist_dir="chroma_index"):
        self.data_dir = data_dir
        self.persist_dir = persist_dir
        self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.documents = []

    def load_documents(self):
        print("🔹 Loading documents...")
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".txt"):
                with open(os.path.join(self.data_dir, filename), "r", encoding="utf-8") as f:
                    text = f.read()
                    chunks = self.split_text_into_chunks(text)
                    for chunk in chunks:
                        self.documents.append(Document(page_content=chunk.strip(), metadata={"source": filename}))
        print(f"✅ Loaded {len(self.documents)} documents")
        self.build_vectorstore()

    def split_text_into_chunks(self, text: str, chunk_size=500, chunk_overlap=50):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        return splitter.split_text(text)

    def build_vectorstore(self):
        print("🔹 Building Chroma vector store...")
        self.vectorstore = Chroma.from_documents(self.documents, self.embedding_model, persist_directory=self.persist_dir)
        self.vectorstore.persist()
        print("✅ Vector store built and persisted")

    def query_cosine(self, query: str, k: int = 5) -> List[Document]:
        vectorstore = Chroma(persist_directory=self.persist_dir, embedding_function=self.embedding_model)
        return vectorstore.similarity_search(query, k=k)
   

    def query_euclidean(self, query: str, k: int = 5) -> List[Tuple[Document, float]]:
        vectorstore = Chroma(persist_directory=self.persist_dir, embedding_function=self.embedding_model)

        # Embed query
        query_emb = self.embedding_model.embed_query(query)

        # Get all doc embeddings
        data = vectorstore._collection.get(include=["documents", "metadatas", "embeddings"])
        
        embeddings = data.get("embeddings")
        documents = data.get("documents")
        metadatas = data.get("metadatas")

        if embeddings is None or documents is None or metadatas is None:
            raise ValueError("No embeddings, documents, or metadatas found in vectorstore")
        
        doc_scores = []
        for doc_emb, content, meta in zip(embeddings, documents, metadatas):
            distance = np.linalg.norm(np.array(query_emb) - np.array(doc_emb))
            score = vectorstore._euclidean_relevance_score_fn(distance.__float__())
            doc = Document(page_content=content, metadata=meta or {})
            doc_scores.append((doc, score))

        # Sort by score descending (higher = more relevant)
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        return doc_scores[:k]


    def query_mmr(self, query: str, k: int = 5) -> List[Document]:
        vectorstore = Chroma(persist_directory=self.persist_dir, embedding_function=self.embedding_model)
        return vectorstore.max_marginal_relevance_search(query, k=k, fetch_k=20)

    def query_hybrid(self, query: str, k: int = 5) -> List[Tuple[Document, float]]:
        # Placeholder: hybrid = 0.6 * cosine + 0.4 * legal entity match
        # We'll simulate "legal entity match" as keyword match for now
        vectorstore = Chroma(persist_directory=self.persist_dir, embedding_function=self.embedding_model)
        cosine_results = vectorstore.similarity_search_with_relevance_scores(query, k=k*2)
        final = []
        for doc, score in cosine_results:
            # Simulate legal keyword match score
            legal_keywords = ["section", "act", "court", "gst", "income", "registration"]
            match_score = sum(1 for word in legal_keywords if word in doc.page_content.lower())
            hybrid_score = 0.6 * score + 0.4 * match_score
            final.append((doc, hybrid_score))
        final.sort(key=lambda x: x[1], reverse=True)
        return final[:k]

    def reset(self):
        if os.path.exists(self.persist_dir):
            import shutil
            shutil.rmtree(self.persist_dir)
        self.documents = []
        self.vectorstore = None

    def evaluate(self, query: str, ground_truth_sources: List[str], k=5) -> Dict[str, Dict[str, float]]:
        methods = {
            "cosine": self.query_cosine,
            "euclidean": lambda q, k: [doc for doc, _ in self.query_euclidean(q, k)],
            "mmr": self.query_mmr,
            "hybrid": lambda q, k: [doc for doc, _ in self.query_hybrid(q, k)],
        }

        scores = defaultdict(dict)

        for method_name, method_func in methods.items():
            top_docs = method_func(query, k)
            sources = [doc.metadata['source'] for doc in top_docs]

            # Precision@k
            true_positive = sum(1 for s in sources if s in ground_truth_sources)
            precision = true_positive / k

            # Recall (simple version: overlap with ground truth set)
            recall = true_positive / len(ground_truth_sources)

            # Diversity: count unique sources or sections
            diversity = len(set(sources)) / k

            scores[method_name] = {
                "precision@5": round(precision, 2),
                "recall": round(recall, 2),
                "diversity": round(diversity, 2)
            }

        return scores
