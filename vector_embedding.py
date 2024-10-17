import ollama
import chromadb
from chromadb.config import Settings

# Load the embedding model name
model = "nomic-embed-text"

# Your dataset (a list of texts)
dataset = [
    "The sky is blue.",
    "The grass is green.",
    "The ocean is vast."
]

# Generate embeddings using Ollama's embeddings function
embeddings = []
for text in dataset:
    embedding = ollama.embeddings(model=model, prompt=text)['embedding']  # Get the embedding for the text
    embeddings.append(embedding)

# Initialize ChromaDB client
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="."))
# Create or get a collection
collection = client.create_collection("my_collection")

# Add documents and embeddings to the collection
collection.add(documents=dataset, embeddings=embeddings)

# Function to find similar items
def find_similar(query_text, k=2):
    query_embedding = ollama.embeddings(model=model, prompt=query_text)['embedding']  # Get embedding for the query
    
    # Query for similar items in ChromaDB
    results = collection.query(embeddings=[query_embedding], n_results=k)
    return results['documents']

# Example query
similar_items = find_similar("What color is the ocean?")
print("Similar items:", similar_items)
