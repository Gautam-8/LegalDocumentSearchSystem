"""
Legal Document Search System - Streamlit App
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List
import time

# Import custom modules
from search_engine import LegalSearchEngine

# Configure page
st.set_page_config(
    page_title="Legal Document Search System",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'search_engine' not in st.session_state:
    st.session_state.search_engine = LegalSearchEngine()
    st.session_state.initialized = False

# Initialize search engine
if not st.session_state.initialized:
    with st.spinner("Initializing search engine..."):
        success = st.session_state.search_engine.initialize()
        if success:
            st.session_state.initialized = True
        else:
            st.error("Failed to initialize search engine")

def main():
    st.title("⚖️ Legal Document Search System")
    st.markdown("Compare 4 different similarity methods for Indian legal document retrieval")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Controls")
        
        # Document upload section
        st.subheader("📄 Upload Documents")
        uploaded_file = st.file_uploader(
            "Upload PDF or Word document",
            type=['pdf', 'docx'],
            help="Upload legal documents to add to the search collection"
        )
        
        if uploaded_file is not None:
            with st.form("upload_form"):
                title = st.text_input("Document Title (optional)", value=uploaded_file.name)
                category = st.selectbox(
                    "Category",
                    ["Income Tax", "GST", "Court Judgment", "Property Law", "Custom"],
                    index=4
                )
                
                if st.form_submit_button("Add Document"):
                    with st.spinner("Processing document..."):
                        success = st.session_state.search_engine.process_uploaded_file(
                            uploaded_file, title, category
                        )
                        if success:
                            st.success("Document added successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to process document")
        
        # Search parameters
        st.subheader("🔍 Search Parameters")
        top_k = st.slider("Number of results per method", 1, 10, 5)
        
        # Evaluation settings
        st.subheader("📊 Evaluation Settings")
        available_categories = st.session_state.search_engine.get_categories()
        relevant_categories = st.multiselect(
            "Select relevant categories for evaluation",
            available_categories,
            default=available_categories[:2] if available_categories else []
        )
        
        # Document statistics
        st.subheader("📈 Document Statistics")
        if st.session_state.initialized:
            stats = st.session_state.search_engine.get_document_statistics()
            st.metric("Total Documents", stats.get('total_documents', 0))
            st.metric("Total Categories", len(stats.get('categories', {})))
            st.metric("Embedding Dimension", stats.get('embedding_dimension', 0))
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Search interface
        st.header("🔍 Search Query")
        query = st.text_input(
            "Enter your legal query:",
            placeholder="e.g., 'What are the tax implications of property transfer?'",
            help="Enter a question or keywords related to Indian legal documents"
        )
        
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    with col2:
        # Quick search examples
        st.header("💡 Quick Examples")
        example_queries = [
            "advance tax payment",
            "property registration",
            "GST liability",
            "contract breach damages",
            "agricultural income exemption"
        ]
        
        for i, example in enumerate(example_queries):
            if st.button(f"📝 {example}", key=f"example_{i}"):
                st.session_state.example_query = example
                st.rerun()
    
    # Use example query if selected
    if 'example_query' in st.session_state:
        query = st.session_state.example_query
        search_button = True
        del st.session_state.example_query
    
    # Perform search
    if search_button and query:
        with st.spinner("Searching documents..."):
            start_time = time.time()
            results = st.session_state.search_engine.search(query, top_k)
            search_time = time.time() - start_time
            
            if results:
                st.success(f"Search completed in {search_time:.2f} seconds")
                
                # Display results in 4 columns
                st.header("📊 Search Results Comparison")
                
                # Method names and colors
                methods = {
                    'cosine': {'name': 'Cosine Similarity', 'color': '#FF6B6B'},
                    'euclidean': {'name': 'Euclidean Distance', 'color': '#4ECDC4'},
                    'mmr': {'name': 'MMR', 'color': '#45B7D1'},
                    'hybrid': {'name': 'Hybrid Similarity', 'color': '#96CEB4'}
                }
                
                # Create 4 columns for results
                cols = st.columns(4)
                
                for i, (method_key, method_info) in enumerate(methods.items()):
                    with cols[i]:
                        st.markdown(f"### {method_info['name']}")
                        
                        method_results = results.get(method_key, [])
                        
                        if method_results:
                            for j, doc in enumerate(method_results):
                                # Create expandable result card
                                with st.expander(f"#{j+1} {doc['title']}", expanded=(j == 0)):
                                    st.markdown(f"**Category:** {doc['category']}")
                                    st.markdown(f"**Similarity Score:** {doc['similarity_score']:.4f}")
                                    
                                    # Show additional scores for hybrid method
                                    if method_key == 'hybrid':
                                        st.markdown(f"**Cosine Score:** {doc.get('cosine_score', 0):.4f}")
                                        st.markdown(f"**Entity Score:** {doc.get('entity_score', 0):.4f}")
                                    
                                    # Show content preview
                                    content_preview = doc['content'][:300] + "..." if len(doc['content']) > 300 else doc['content']
                                    st.markdown(f"**Content Preview:**\n{content_preview}")
                                    
                                    # Show entities
                                    if doc.get('entities'):
                                        st.markdown("**Legal Entities:**")
                                        entities_str = ", ".join(doc['entities'][:5])  # Show first 5 entities
                                        st.markdown(f"_{entities_str}_")
                        else:
                            st.info("No results found")
                
                # Performance metrics
                if relevant_categories:
                    st.header("📈 Performance Metrics")
                    
                    evaluation = st.session_state.search_engine.evaluate_methods(
                        query, relevant_categories, top_k
                    )
                    
                    # Create metrics comparison
                    metrics_data = []
                    for method_key, method_info in methods.items():
                        if method_key in evaluation:
                            metrics = evaluation[method_key]
                            metrics_data.append({
                                'Method': method_info['name'],
                                'Precision@5': metrics['precision'],
                                'Recall@5': metrics['recall'],
                                'F1 Score': metrics['f1_score'],
                                'Diversity': metrics['diversity']
                            })
                    
                    if metrics_data:
                        # Display metrics table
                        metrics_df = pd.DataFrame(metrics_data)
                        st.dataframe(metrics_df, use_container_width=True)
                        
                        # Create comparison charts
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Precision/Recall comparison
                            fig1 = px.bar(
                                metrics_df, 
                                x='Method', 
                                y=['Precision@5', 'Recall@5'],
                                title='Precision vs Recall Comparison',
                                barmode='group'
                            )
                            st.plotly_chart(fig1, use_container_width=True)
                        
                        with col2:
                            # F1 Score and Diversity comparison
                            fig2 = px.bar(
                                metrics_df,
                                x='Method',
                                y=['F1 Score', 'Diversity'],
                                title='F1 Score vs Diversity Comparison',
                                barmode='group'
                            )
                            st.plotly_chart(fig2, use_container_width=True)
                
                # Method comparison summary
                st.header("🔄 Method Comparison Summary")
                summary = st.session_state.search_engine.get_method_comparison_summary(results)
                
                summary_data = []
                for method_key, method_info in methods.items():
                    if method_key in summary:
                        data = summary[method_key]
                        summary_data.append({
                            'Method': method_info['name'],
                            'Avg Similarity': f"{data['avg_similarity_score']:.4f}",
                            'Categories Covered': len(data['categories_covered']),
                            'Unique Documents': data['unique_documents'],
                            'Categories': ', '.join(data['categories_covered'])
                        })
                
                if summary_data:
                    summary_df = pd.DataFrame(summary_data)
                    st.dataframe(summary_df, use_container_width=True)
                
            else:
                st.error("No search results found. Please check your query or try again.")
    
    # Document browser
    st.header("📚 Document Browser")
    
    if st.session_state.initialized:
        # Category filter
        col1, col2 = st.columns([1, 3])
        
        with col1:
            selected_category = st.selectbox(
                "Filter by category:",
                ["All"] + available_categories
            )
        
        with col2:
            if selected_category == "All":
                documents = st.session_state.search_engine.get_all_documents()
            else:
                documents = st.session_state.search_engine.search_by_category(selected_category)
        
        if documents:
            st.write(f"Showing {len(documents)} documents")
            
            # Display documents in a more compact format
            for doc in documents:
                with st.expander(f"{doc['title']} ({doc['category']})"):
                    st.markdown(f"**ID:** {doc['id']}")
                    st.markdown(f"**Category:** {doc['category']}")
                    
                    # Content preview
                    content_preview = doc['content'][:400] + "..." if len(doc['content']) > 400 else doc['content']
                    st.markdown(f"**Content:**\n{content_preview}")
                    
                    # Entities
                    if doc.get('entities'):
                        st.markdown("**Legal Entities:**")
                        st.markdown(f"_{', '.join(doc['entities'])}_")
        else:
            st.info("No documents found in the selected category")

if __name__ == "__main__":
    main() 