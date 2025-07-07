"""
Configuration settings for Legal Document Search System
"""

# Model settings
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384  # Dimension for all-MiniLM-L6-v2

# Search settings
DEFAULT_TOP_K = 5
MAX_TOP_K = 20
MIN_TOP_K = 1

# MMR settings
MMR_LAMBDA = 0.7  # Balance between relevance and diversity

# Hybrid similarity weights
HYBRID_COSINE_WEIGHT = 0.6
HYBRID_ENTITY_WEIGHT = 0.4

# UI settings
MAX_CONTENT_PREVIEW_LENGTH = 300
MAX_ENTITIES_DISPLAY = 5

# File upload settings
ALLOWED_FILE_TYPES = ['pdf', 'docx']
MAX_FILE_SIZE_MB = 10

# Legal categories
LEGAL_CATEGORIES = [
    "Income Tax",
    "GST", 
    "Court Judgment",
    "Property Law",
    "Custom",
    "Uploaded"
]

# Sample queries for quick testing
SAMPLE_QUERIES = [
    "What are the advance tax payment requirements?",
    "How is agricultural income treated for tax purposes?",
    "What are the GST registration thresholds?",
    "When does GST liability arise on supply of goods?",
    "What constitutes breach of contract?",
    "How are damages calculated in contract disputes?",
    "What are the requirements for property registration?",
    "How is adverse possession established?",
    "What are the tax deductions available under Section 80C?",
    "What documents require compulsory registration?"
]

# Legal entity keywords for hybrid matching
LEGAL_ENTITY_KEYWORDS = [
    "act", "section", "clause", "amendment", "provision", "regulation",
    "court", "judgment", "order", "petition", "appeal", "writ",
    "contract", "agreement", "deed", "instrument", "document",
    "property", "immovable", "movable", "ownership", "title",
    "tax", "income", "gst", "duty", "liability", "assessment",
    "registration", "license", "permit", "compliance",
    "damages", "compensation", "penalty", "fine", "interest",
    "plaintiff", "defendant", "appellant", "respondent",
    "jurisdiction", "precedent", "statute", "ordinance"
]

# Evaluation settings
EVALUATION_METRICS = [
    "precision",
    "recall", 
    "f1_score",
    "diversity"
]

# Color scheme for UI
METHOD_COLORS = {
    'cosine': '#FF6B6B',
    'euclidean': '#4ECDC4',
    'mmr': '#45B7D1', 
    'hybrid': '#96CEB4'
}

CATEGORY_COLORS = {
    'Income Tax': '#FF6B6B',
    'GST': '#4ECDC4',
    'Court Judgment': '#45B7D1',
    'Property Law': '#96CEB4',
    'Custom': '#FECA57',
    'Uploaded': '#FF9FF3'
} 