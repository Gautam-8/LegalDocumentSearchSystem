"""
Similarity Methods for Legal Document Search
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict, Tuple, Any
import re


class SimilarityMethods:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        
    def cosine_similarity_search(self, query_embedding: np.ndarray, doc_embeddings: np.ndarray, 
                                documents: List[Dict], top_k: int = 5) -> List[Dict]:
        """
        Standard cosine similarity search
        """
        similarities = cosine_similarity(query_embedding.reshape(1, -1), doc_embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            doc = documents[idx].copy()
            doc['similarity_score'] = float(similarities[idx])
            doc['method'] = 'Cosine Similarity'
            results.append(doc)
        
        return results
    
    def euclidean_distance_search(self, query_embedding: np.ndarray, doc_embeddings: np.ndarray,
                                 documents: List[Dict], top_k: int = 5) -> List[Dict]:
        """
        Euclidean distance based search (lower distance = higher similarity)
        """
        distances = euclidean_distances(query_embedding.reshape(1, -1), doc_embeddings)[0]
        # Convert distances to similarity scores (inverse relationship)
        similarities = 1 / (1 + distances)
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            doc = documents[idx].copy()
            doc['similarity_score'] = float(similarities[idx])
            doc['method'] = 'Euclidean Distance'
            results.append(doc)
        
        return results
    
    def mmr_search(self, query_embedding: np.ndarray, doc_embeddings: np.ndarray,
                   documents: List[Dict], top_k: int = 5, lambda_param: float = 0.7) -> List[Dict]:
        """
        Maximal Marginal Relevance (MMR) search to reduce redundancy
        """
        # Calculate initial similarities
        similarities = cosine_similarity(query_embedding.reshape(1, -1), doc_embeddings)[0]
        
        selected_indices = []
        remaining_indices = list(range(len(documents)))
        
        # Select first document with highest similarity
        first_idx = int(np.argmax(similarities))
        selected_indices.append(first_idx)
        remaining_indices.remove(first_idx)
        
        # Iteratively select documents using MMR
        for _ in range(min(top_k - 1, len(remaining_indices))):
            mmr_scores = []
            
            for idx in remaining_indices:
                # Relevance score
                relevance = similarities[idx]
                
                # Redundancy score (max similarity with already selected documents)
                redundancy = 0
                if selected_indices:
                    selected_embeddings = doc_embeddings[selected_indices]
                    doc_similarities = cosine_similarity(
                        doc_embeddings[idx].reshape(1, -1), 
                        selected_embeddings
                    )[0]
                    redundancy = np.max(doc_similarities)
                
                # MMR score
                mmr_score = lambda_param * relevance - (1 - lambda_param) * redundancy
                mmr_scores.append(mmr_score)
            
            # Select document with highest MMR score
            best_idx = remaining_indices[np.argmax(mmr_scores)]
            selected_indices.append(best_idx)
            remaining_indices.remove(best_idx)
        
        results = []
        for idx in selected_indices:
            doc = documents[idx].copy()
            doc['similarity_score'] = float(similarities[idx])
            doc['method'] = 'MMR'
            results.append(doc)
        
        return results
    
    def hybrid_similarity_search(self, query: str, query_embedding: np.ndarray, 
                                doc_embeddings: np.ndarray, documents: List[Dict], 
                                top_k: int = 5) -> List[Dict]:
        """
        Hybrid similarity: 0.6 * Cosine + 0.4 * Legal Entity Match
        """
        # Cosine similarity component
        cosine_scores = cosine_similarity(query_embedding.reshape(1, -1), doc_embeddings)[0]
        
        # Legal entity matching component
        entity_scores = self._calculate_entity_match_scores(query, documents)
        
        # Combine scores (0.6 * cosine + 0.4 * entity_match)
        hybrid_scores = 0.6 * cosine_scores + 0.4 * entity_scores
        
        top_indices = np.argsort(hybrid_scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            doc = documents[idx].copy()
            doc['similarity_score'] = float(hybrid_scores[idx])
            doc['cosine_score'] = float(cosine_scores[idx])
            doc['entity_score'] = float(entity_scores[idx])
            doc['method'] = 'Hybrid Similarity'
            results.append(doc)
        
        return results
    
    def _calculate_entity_match_scores(self, query: str, documents: List[Dict]) -> np.ndarray:
        """
        Calculate legal entity matching scores
        """
        query_lower = query.lower()
        scores = []
        
        for doc in documents:
            score = 0
            entities = doc.get('entities', [])
            
            # Check for exact entity matches
            for entity in entities:
                if entity.lower() in query_lower:
                    score += 1
            
            # Check for partial entity matches
            for entity in entities:
                entity_words = entity.lower().split()
                query_words = query_lower.split()
                
                # Count overlapping words
                overlap = len(set(entity_words) & set(query_words))
                if overlap > 0:
                    score += overlap / len(entity_words)
            
            # Normalize score by number of entities
            if entities:
                score = score / len(entities)
            
            scores.append(score)
        
        return np.array(scores)
    
    def calculate_diversity_score(self, results: List[Dict]) -> float:
        """
        Calculate diversity score for MMR evaluation
        """
        if len(results) < 2:
            return 1.0
        
        categories = [doc['category'] for doc in results]
        unique_categories = len(set(categories))
        total_categories = len(categories)
        
        # Simple diversity metric: ratio of unique categories to total results
        diversity = unique_categories / total_categories
        
        return diversity
    
    def calculate_precision_at_k(self, results: List[Dict], relevant_categories: List[str], k: int = 5) -> float:
        """
        Calculate precision at k for evaluation
        """
        if not results:
            return 0.0
        
        top_k_results = results[:k]
        relevant_count = sum(1 for doc in top_k_results if doc['category'] in relevant_categories)
        
        return relevant_count / min(k, len(top_k_results))
    
    def calculate_recall_at_k(self, results: List[Dict], all_documents: List[Dict], 
                             relevant_categories: List[str], k: int = 5) -> float:
        """
        Calculate recall at k for evaluation
        """
        if not results:
            return 0.0
        
        # Total relevant documents in the dataset
        total_relevant = sum(1 for doc in all_documents if doc['category'] in relevant_categories)
        
        if total_relevant == 0:
            return 0.0
        
        # Relevant documents in top k results
        top_k_results = results[:k]
        relevant_retrieved = sum(1 for doc in top_k_results if doc['category'] in relevant_categories)
        
        return relevant_retrieved / total_relevant 