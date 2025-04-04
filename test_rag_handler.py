#!/usr/bin/env python3
"""
This script tests if the RAG handler still works after removing the sentence-transformers dependency.
"""

import os
import sys
from mindsdb.integrations.handlers.rag_handler.settings import load_embeddings_model

def test_load_embeddings_model():
    """Test if the load_embeddings_model function still works."""
    try:
        # Try to load the default embeddings model
        from mindsdb.integrations.handlers.rag_handler.settings import DEFAULT_EMBEDDINGS_MODEL
        model = load_embeddings_model(DEFAULT_EMBEDDINGS_MODEL)
        print(f"Successfully loaded embeddings model: {DEFAULT_EMBEDDINGS_MODEL}")
        return True
    except Exception as e:
        print(f"Error loading embeddings model: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_load_embeddings_model()
    sys.exit(0 if success else 1)