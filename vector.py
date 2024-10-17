from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Your dataset (a list of sentences)
sentences = [
    "The sky is blue.",
    "The grass is green.",
    "The ocean is vast."
]

# Generate embeddings
embeddings = model.encode(sentences)

# Print the embeddings (vector representations)
for i, embedding in enumerate(embeddings):
    print(f"Sentence: {sentences[i]}")
    print(f"Embedding: {embedding}\n")
