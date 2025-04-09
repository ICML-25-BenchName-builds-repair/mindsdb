import os
import sys

# Add the repository root to the Python path
sys.path.insert(0, os.path.abspath('.'))

# Import the load_embeddings_model function from the RAG handler
from mindsdb.integrations.handlers.rag_handler.settings import load_embeddings_model

# Try to load an embeddings model
try:
    model = load_embeddings_model("BAAI/bge-base-en")
    print("Successfully loaded embeddings model")
except ImportError as e:
    print(f"ImportError: {e}")
    if "sentence_transformers" in str(e):
        print("\nThe 'sentence-transformers' package is required but not imported in the code.")
        print("This confirms the issue reported in the CI workflow.")
except Exception as e:
    print(f"Other error: {e}")