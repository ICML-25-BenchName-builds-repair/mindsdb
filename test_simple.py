import os
import sys

# Check if sentence-transformers is imported in the RAG handler
try:
    import sentence_transformers
    print("sentence-transformers is installed")
except ImportError:
    print("sentence-transformers is not installed")

# Check the requirements file
with open('mindsdb/integrations/handlers/rag_handler/requirements.txt', 'r') as f:
    reqs = f.read()
    print("\nRAG handler requirements.txt:")
    print(reqs)
    
    if 'sentence-transformers' in reqs:
        print("\nsentence-transformers is listed in requirements.txt but not imported in the code")
    else:
        print("\nsentence-transformers is not listed in requirements.txt")