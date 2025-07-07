"""
Document Processor for Legal Document Search System
"""

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional, Union
import PyPDF2
import docx
import io
import streamlit as st
from sample_data.sample_documents import SAMPLE_DOCUMENTS


class DocumentProcessor:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize document processor with sentence transformer model
        """
        self.model = SentenceTransformer(model_name)
        self.documents = []
        self.embeddings = None
        
    def load_sample_documents(self):
        """
        Load sample Indian legal documents
        """
        self.documents = SAMPLE_DOCUMENTS.copy()
        self._generate_embeddings()
        
    def add_document(self, title: str, content: str, category: str = "Custom", 
                    entities: Optional[List[str]] = None) -> bool:
        """
        Add a new document to the collection
        """
        try:
            doc_id = f"custom_{len(self.documents)}"
            new_doc = {
                "id": doc_id,
                "title": title,
                "category": category,
                "content": content,
                "entities": entities or []
            }
            
            self.documents.append(new_doc)
            self._generate_embeddings()
            return True
        except Exception as e:
            st.error(f"Error adding document: {str(e)}")
            return False
    
    def process_uploaded_file(self, uploaded_file, title: Optional[str] = None, 
                            category: str = "Uploaded") -> bool:
        """
        Process uploaded PDF or Word document
        """
        try:
            file_type = uploaded_file.type
            content = ""
            
            if file_type == "application/pdf":
                content = self._extract_pdf_text(uploaded_file)
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                content = self._extract_docx_text(uploaded_file)
            else:
                st.error("Unsupported file type. Please upload PDF or Word documents.")
                return False
            
            if not content.strip():
                st.error("Could not extract text from the uploaded file.")
                return False
            
            # Use filename as title if not provided
            if not title:
                title = uploaded_file.name
            
            # Extract basic entities (this is a simple implementation)
            entities = self._extract_basic_entities(content)
            
            return self.add_document(title, content, category, entities)
            
        except Exception as e:
            st.error(f"Error processing uploaded file: {str(e)}")
            return False
    
    def _extract_pdf_text(self, uploaded_file) -> str:
        """
        Extract text from PDF file
        """
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error extracting PDF text: {str(e)}")
            return ""
    
    def _extract_docx_text(self, uploaded_file) -> str:
        """
        Extract text from Word document
        """
        try:
            doc = docx.Document(uploaded_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            st.error(f"Error extracting Word document text: {str(e)}")
            return ""
    
    def _extract_basic_entities(self, content: str) -> List[str]:
        """
        Extract basic legal entities from content (simple keyword-based approach)
        """
        # Common legal terms and entities
        legal_keywords = [
            "act", "section", "clause", "amendment", "provision", "regulation",
            "court", "judgment", "order", "petition", "appeal", "writ",
            "contract", "agreement", "deed", "instrument", "document",
            "property", "immovable", "movable", "ownership", "title",
            "tax", "income", "gst", "duty", "liability", "assessment",
            "registration", "license", "permit", "compliance",
            "damages", "compensation", "penalty", "fine", "interest"
        ]
        
        content_lower = content.lower()
        found_entities = []
        
        for keyword in legal_keywords:
            if keyword in content_lower:
                found_entities.append(keyword)
        
        # Extract section references (e.g., "Section 10", "Section 2(1A)")
        import re
        section_pattern = r'section\s+\d+(?:\([^)]+\))?'
        sections = re.findall(section_pattern, content_lower)
        found_entities.extend(sections)
        
        return list(set(found_entities))  # Remove duplicates
    
    def _generate_embeddings(self):
        """
        Generate embeddings for all documents
        """
        if not self.documents:
            self.embeddings = None
            return
        
        try:
            # Extract content for embedding
            texts = [doc['content'] for doc in self.documents]
            
            # Generate embeddings
            self.embeddings = self.model.encode(texts, convert_to_tensor=False)
            
        except Exception as e:
            st.error(f"Error generating embeddings: {str(e)}")
            self.embeddings = None
    
    def get_query_embedding(self, query: str) -> Optional[np.ndarray]:
        """
        Generate embedding for search query
        """
        try:
            embedding = self.model.encode([query], convert_to_tensor=False)
            return embedding[0]
        except Exception as e:
            st.error(f"Error generating query embedding: {str(e)}")
            return None
    
    def get_documents(self) -> List[Dict]:
        """
        Get all documents
        """
        return self.documents
    
    def get_embeddings(self) -> Optional[np.ndarray]:
        """
        Get document embeddings
        """
        return self.embeddings
    
    def get_document_by_id(self, doc_id: str) -> Optional[Dict]:
        """
        Get document by ID
        """
        for doc in self.documents:
            if doc['id'] == doc_id:
                return doc
        return None
    
    def get_documents_by_category(self, category: str) -> List[Dict]:
        """
        Get documents by category
        """
        return [doc for doc in self.documents if doc['category'] == category]
    
    def get_document_statistics(self) -> Dict:
        """
        Get statistics about the document collection
        """
        if not self.documents:
            return {}
        
        categories = [doc['category'] for doc in self.documents]
        category_counts = {}
        for cat in categories:
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        total_entities = sum(len(doc.get('entities', [])) for doc in self.documents)
        avg_content_length = sum(len(doc['content']) for doc in self.documents) / len(self.documents)
        
        return {
            'total_documents': len(self.documents),
            'categories': category_counts,
            'total_entities': total_entities,
            'avg_content_length': avg_content_length,
            'embedding_dimension': self.embeddings.shape[1] if self.embeddings is not None else 0
        } 