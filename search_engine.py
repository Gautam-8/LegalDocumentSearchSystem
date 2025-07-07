"""
Legal Document Search Engine
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
from document_processor import DocumentProcessor
from similarity_methods import SimilarityMethods


class LegalSearchEngine:
    def __init__(self):
        self.doc_processor = DocumentProcessor()
        self.similarity_methods = SimilarityMethods()
        self.is_initialized = False
        
    def initialize(self):
        """
        Initialize the search engine with sample documents
        """
        try:
            self.doc_processor.load_sample_documents()
            self.is_initialized = True
            return True
        except Exception as e:
            print(f"Error initializing search engine: {str(e)}")
            return False
    
    def search(self, query: str, top_k: int = 5) -> Dict[str, List[Dict]]:
        """
        Perform search using all 4 similarity methods
        """
        if not self.is_initialized:
            return {}
        
        # Get query embedding
        query_embedding = self.doc_processor.get_query_embedding(query)
        if query_embedding is None:
            return {}
        
        # Get document data
        documents = self.doc_processor.get_documents()
        doc_embeddings = self.doc_processor.get_embeddings()
        
        if not documents or doc_embeddings is None:
            return {}
        
        # Perform searches with all methods
        results = {}
        
        # 1. Cosine Similarity
        results['cosine'] = self.similarity_methods.cosine_similarity_search(
            query_embedding, doc_embeddings, documents, top_k
        )
        
        # 2. Euclidean Distance
        results['euclidean'] = self.similarity_methods.euclidean_distance_search(
            query_embedding, doc_embeddings, documents, top_k
        )
        
        # 3. MMR (Maximal Marginal Relevance)
        results['mmr'] = self.similarity_methods.mmr_search(
            query_embedding, doc_embeddings, documents, top_k
        )
        
        # 4. Hybrid Similarity
        results['hybrid'] = self.similarity_methods.hybrid_similarity_search(
            query, query_embedding, doc_embeddings, documents, top_k
        )
        
        return results
    
    def evaluate_methods(self, query: str, relevant_categories: List[str], 
                        top_k: int = 5) -> Dict[str, Dict]:
        """
        Evaluate all similarity methods with metrics
        """
        results = self.search(query, top_k)
        evaluation = {}
        
        documents = self.doc_processor.get_documents()
        
        for method_name, method_results in results.items():
            # Calculate precision at k
            precision = self.similarity_methods.calculate_precision_at_k(
                method_results, relevant_categories, top_k
            )
            
            # Calculate recall at k
            recall = self.similarity_methods.calculate_recall_at_k(
                method_results, documents, relevant_categories, top_k
            )
            
            # Calculate diversity score
            diversity = self.similarity_methods.calculate_diversity_score(method_results)
            
            # Calculate F1 score
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            evaluation[method_name] = {
                'precision': precision,
                'recall': recall,
                'diversity': diversity,
                'f1_score': f1_score,
                'results_count': len(method_results)
            }
        
        return evaluation
    
    def add_document(self, title: str, content: str, category: str = "Custom") -> bool:
        """
        Add a new document to the search engine
        """
        success = self.doc_processor.add_document(title, content, category)
        return success
    
    def process_uploaded_file(self, uploaded_file, title: str = None, 
                            category: str = "Uploaded") -> bool:
        """
        Process and add uploaded file to search engine
        """
        return self.doc_processor.process_uploaded_file(uploaded_file, title, category)
    
    def get_document_statistics(self) -> Dict:
        """
        Get statistics about the document collection
        """
        return self.doc_processor.get_document_statistics()
    
    def get_all_documents(self) -> List[Dict]:
        """
        Get all documents in the collection
        """
        return self.doc_processor.get_documents()
    
    def get_categories(self) -> List[str]:
        """
        Get all unique categories in the document collection
        """
        documents = self.doc_processor.get_documents()
        categories = list(set(doc['category'] for doc in documents))
        return sorted(categories)
    
    def search_by_category(self, category: str) -> List[Dict]:
        """
        Get all documents in a specific category
        """
        return self.doc_processor.get_documents_by_category(category)
    
    def get_method_comparison_summary(self, results: Dict[str, List[Dict]]) -> Dict:
        """
        Generate a summary comparison of different methods
        """
        summary = {}
        
        for method_name, method_results in results.items():
            if method_results:
                # Calculate average similarity score
                avg_score = sum(doc.get('similarity_score', 0) for doc in method_results) / len(method_results)
                
                # Get categories represented
                categories = list(set(doc['category'] for doc in method_results))
                
                # Count unique documents (to check for overlap)
                doc_ids = [doc['id'] for doc in method_results]
                
                summary[method_name] = {
                    'avg_similarity_score': avg_score,
                    'categories_covered': categories,
                    'unique_documents': len(set(doc_ids)),
                    'total_results': len(method_results)
                }
        
        return summary 