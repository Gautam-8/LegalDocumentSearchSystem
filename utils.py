"""
Utility functions for Legal Document Search System
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any
import streamlit as st


def format_similarity_score(score: float) -> str:
    """
    Format similarity score for display
    """
    return f"{score:.4f}"


def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Truncate text for display purposes
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def get_category_color(category: str) -> str:
    """
    Get color for different legal document categories
    """
    color_map = {
        'Income Tax': '#FF6B6B',
        'GST': '#4ECDC4', 
        'Court Judgment': '#45B7D1',
        'Property Law': '#96CEB4',
        'Custom': '#FECA57',
        'Uploaded': '#FF9FF3'
    }
    return color_map.get(category, '#95A5A6')


def calculate_overlap_percentage(results1: List[Dict], results2: List[Dict]) -> float:
    """
    Calculate percentage overlap between two result sets
    """
    if not results1 or not results2:
        return 0.0
    
    ids1 = set(doc['id'] for doc in results1)
    ids2 = set(doc['id'] for doc in results2)
    
    overlap = len(ids1.intersection(ids2))
    total_unique = len(ids1.union(ids2))
    
    return (overlap / total_unique) * 100 if total_unique > 0 else 0.0


def generate_search_summary(results: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """
    Generate a comprehensive summary of search results
    """
    summary = {
        'total_methods': len(results),
        'methods_with_results': sum(1 for method_results in results.values() if method_results),
        'total_unique_documents': len(set(
            doc['id'] for method_results in results.values() 
            for doc in method_results
        )),
        'category_distribution': {},
        'score_statistics': {}
    }
    
    # Calculate category distribution across all methods
    all_categories = []
    for method_results in results.values():
        all_categories.extend(doc['category'] for doc in method_results)
    
    for category in set(all_categories):
        summary['category_distribution'][category] = all_categories.count(category)
    
    # Calculate score statistics for each method
    for method_name, method_results in results.items():
        if method_results:
            scores = [doc['similarity_score'] for doc in method_results]
            summary['score_statistics'][method_name] = {
                'mean': np.mean(scores),
                'std': np.std(scores),
                'min': np.min(scores),
                'max': np.max(scores)
            }
    
    return summary


def create_method_comparison_table(results: Dict[str, List[Dict]]) -> pd.DataFrame:
    """
    Create a comparison table for different methods
    """
    comparison_data = []
    
    method_names = {
        'cosine': 'Cosine Similarity',
        'euclidean': 'Euclidean Distance', 
        'mmr': 'MMR',
        'hybrid': 'Hybrid Similarity'
    }
    
    for method_key, method_results in results.items():
        method_name = method_names.get(method_key, method_key)
        
        if method_results:
            # Calculate statistics
            scores = [doc['similarity_score'] for doc in method_results]
            categories = [doc['category'] for doc in method_results]
            
            comparison_data.append({
                'Method': method_name,
                'Results Count': len(method_results),
                'Avg Score': np.mean(scores),
                'Score Range': f"{np.min(scores):.3f} - {np.max(scores):.3f}",
                'Unique Categories': len(set(categories)),
                'Top Category': max(set(categories), key=categories.count) if categories else 'N/A'
            })
        else:
            comparison_data.append({
                'Method': method_name,
                'Results Count': 0,
                'Avg Score': 0.0,
                'Score Range': 'N/A',
                'Unique Categories': 0,
                'Top Category': 'N/A'
            })
    
    return pd.DataFrame(comparison_data)


def validate_query(query: str) -> tuple[bool, str]:
    """
    Validate search query
    """
    if not query or not query.strip():
        return False, "Please enter a search query"
    
    if len(query.strip()) < 3:
        return False, "Query must be at least 3 characters long"
    
    if len(query) > 500:
        return False, "Query is too long (max 500 characters)"
    
    return True, ""


def extract_key_terms(text: str, max_terms: int = 10) -> List[str]:
    """
    Extract key terms from text (simple implementation)
    """
    # Simple keyword extraction based on word frequency
    words = text.lower().split()
    
    # Filter out common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
        'before', 'after', 'above', 'below', 'between', 'among', 'within',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
        'must', 'can', 'shall', 'this', 'that', 'these', 'those', 'i', 'you',
        'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
    }
    
    # Count word frequencies
    word_freq = {}
    for word in words:
        # Remove punctuation and filter
        clean_word = ''.join(c for c in word if c.isalnum())
        if clean_word and len(clean_word) > 2 and clean_word not in stop_words:
            word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
    
    # Sort by frequency and return top terms
    sorted_terms = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [term for term, freq in sorted_terms[:max_terms]]


def format_legal_entities(entities: List[str], max_display: int = 5) -> str:
    """
    Format legal entities for display
    """
    if not entities:
        return "No entities found"
    
    if len(entities) <= max_display:
        return ", ".join(entities)
    
    displayed = ", ".join(entities[:max_display])
    remaining = len(entities) - max_display
    return f"{displayed} and {remaining} more"


def calculate_result_diversity(results: List[Dict]) -> Dict[str, float]:
    """
    Calculate diversity metrics for search results
    """
    if not results:
        return {'category_diversity': 0.0, 'content_diversity': 0.0}
    
    # Category diversity
    categories = [doc['category'] for doc in results]
    unique_categories = len(set(categories))
    category_diversity = unique_categories / len(categories)
    
    # Content diversity (simplified - based on title similarity)
    titles = [doc['title'] for doc in results]
    unique_titles = len(set(titles))
    content_diversity = unique_titles / len(titles)
    
    return {
        'category_diversity': category_diversity,
        'content_diversity': content_diversity
    }


@st.cache_data
def get_sample_queries() -> List[str]:
    """
    Get sample queries for legal document search
    """
    return [
        "What are the advance tax payment requirements?",
        "How is agricultural income treated for tax purposes?",
        "What are the GST registration thresholds?",
        "When does GST liability arise on supply of goods?",
        "What constitutes breach of contract?",
        "How are damages calculated in contract disputes?",
        "What are the requirements for property registration?",
        "How is adverse possession established?",
        "What are the tax deductions available under Section 80C?",
        "What documents require compulsory registration?",
        "How is immovable property defined in law?",
        "What are the legal remedies for property disputes?"
    ] 