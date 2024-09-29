import numpy as np

# Load embeddings from the saved .npy file
model_name = 'all-MiniLM-L6-v2'  # Change this to test other models
embeddings = np.load(f'data/embeddings_{model_name}.npy')

print(f"Loaded embeddings for model: {model_name}")
print(f"Embeddings shape: {embeddings.shape}")
print(f"First embedding vector:\n{embeddings[0]}")  # Print the first embedding
