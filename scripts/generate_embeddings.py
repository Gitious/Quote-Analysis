import json
from sentence_transformers import SentenceTransformer
import numpy as np

# Load the cleaned quotes
with open('data/cleaned_quotes.json', 'r') as f:
    quotes = json.load(f)

# List of embedding models to test
models = [
    'all-MiniLM-L6-v2',           # MiniLM
    'paraphrase-MiniLM-L12-v2',   # Another MiniLM variant
    'sentence-transformers/all-MiniLM-L12-v2',  # Fixed comma here
    'sentence-transformers/paraphrase-multilingual-mpnet-base-v2',  # MPNet for better contextual embeddings
    'intfloat/multilingual-e5-small',  # E5 small variant
    'hkunlp/instructor-xl',
    'intfloat/multilingual-e5-large',
    'intfloat/multilingual-e5-base',
]

# Function to generate embeddings for a given model
def generate_embeddings(texts, model_name):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, batch_size=2, show_progress_bar=True)
    return embeddings

# Extract only the quote texts from each quote
texts = [quote['text'] for quote in quotes]

# Test different embedding models
for model_name in models:
    print(f"Generating embeddings with model: {model_name}")

    # Generate embeddings for the current model
    embeddings = generate_embeddings(texts, model_name)

    # Save embeddings for this model to a file
    np.save(f'data/embeddings_{model_name.replace("/", "-")}.npy', np.array(embeddings))

    print(f"Embeddings generated and saved for model: {model_name}")
