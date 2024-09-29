import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

# Load the cleaned quotes
with open('data/cleaned_quotes.json', 'r') as f:
    quotes = json.load(f)

# Test quote to compare against
test_quote = "You have to write the book that wants to be written."

# Function to calculate cosine similarity between two vectors
def cosine_sim(a, b):
    return cosine_similarity([a], [b])[0][0]

# Models to compare
models = [
    'all-MiniLM-L6-v2', 
    'paraphrase-MiniLM-L12-v2',
    'sentence-transformers/all-MiniLM-L12-v2',
    'sentence-transformers/paraphrase-multilingual-mpnet-base-v2',
    'intfloat/multilingual-e5-small',
    'hkunlp/instructor-xl',
    'intfloat/multilingual-e5-large',
    'intfloat/multilingual-e5-base',
]

# Generate embeddings for the test quote and compare with pre-generated embeddings
for model_name in models:
    print(f"\nTesting model: {model_name}")
    
    # Load the model
    model = SentenceTransformer(model_name)
    
    # Generate embedding for the test quote
    test_embedding = model.encode(test_quote)
    
    # Load pre-generated embeddings for all quotes
    embeddings = np.load(f'data/embeddings_{model_name.replace("/", "-")}.npy')
    
    # Compare the test embedding with all other embeddings using cosine similarity
    similarities = []
    for i, quote in enumerate(quotes):
        sim = cosine_sim(test_embedding, embeddings[i])
        similarities.append((sim, quote['text']))
    
    # Sort by similarity (higher is more similar)
    similarities.sort(reverse=True, key=lambda x: x[0])
    
    # Print top 3 most similar quotes
    print(f"Top 3 similar quotes for model {model_name}:")
    for sim, text in similarities[:3]:
        print(f"Similarity: {sim:.4f}, Quote: {text}")
