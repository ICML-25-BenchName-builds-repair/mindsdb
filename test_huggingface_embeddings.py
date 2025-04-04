#!/usr/bin/env python3
"""
This script tests if the HuggingFaceEmbeddings class can be imported and used without sentence-transformers
being explicitly installed.
"""

import sys

def test_huggingface_embeddings():
    """Test if the HuggingFaceEmbeddings class can be imported and used."""
    try:
        # Try to import HuggingFaceEmbeddings
        try:
            from langchain.embeddings.huggingface import HuggingFaceEmbeddings
            print("Successfully imported HuggingFaceEmbeddings from langchain")
        except ImportError:
            try:
                from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
                print("Successfully imported HuggingFaceEmbeddings from langchain_community")
            except ImportError:
                print("Could not import HuggingFaceEmbeddings from either langchain or langchain_community")
                return False
        
        # Check if sentence_transformers is a dependency
        import inspect
        source = inspect.getsource(HuggingFaceEmbeddings)
        if "sentence_transformers" in source:
            print("HuggingFaceEmbeddings uses sentence-transformers")
            
            # Try to import sentence_transformers
            try:
                import sentence_transformers
                print("Successfully imported sentence_transformers")
                return True
            except ImportError:
                print("Could not import sentence_transformers")
                return False
        else:
            print("HuggingFaceEmbeddings does not use sentence-transformers")
            return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_huggingface_embeddings()
    sys.exit(0 if success else 1)