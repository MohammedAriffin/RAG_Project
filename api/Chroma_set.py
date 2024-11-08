import chromadb
import ollama
import csv
from chromadb.config import Settings

# Initialize PersistentClient
client = chromadb.PersistentClient(path=r"./data")

# Create or access a collection
collection = client.get_or_create_collection(name="my_data")

# Load the embedding model name
model = "nomic-embed-text"

# Load and update count.txt for unique IDs
with open('count.txt', 'a+') as file1:
    file1.seek(0)
    count = file1.read()
    count = int(count) if count else 0
    file1.seek(0)
    file1.truncate()
    file1.write(str(count + 1))

# Load the dataset
with open('data.csv', 'r') as file:
    dataset = list(csv.DictReader(file, delimiter=','))

# Vectorize and store embeddings
embeddings = []
for data in dataset:
    # Add phrases for clarity in concatenation
    embedding_input = f"The category labels are {data['metadata']} and the question is: {data['question']}"
    embedding = ollama.embeddings(model=model, prompt=embedding_input)['embedding']
    embeddings.append(embedding)

# Insert embeddings, metadata, and IDs into the collection
try:
    for i, data in enumerate(dataset):
        # Use incremented count as a unique ID prefix
        unique_id = f"doc_{count + i}"

        # Add each document with embedding and metadata to the collection
        collection.add(
            ids=[unique_id],
            documents=[data['answer']],  # Assuming answer as the main document text
            embeddings=[embeddings[i]],  # Corresponding embedding
            metadatas=[data]  # Metadata for context (without context prompt)
        )
    print("Data added to the collection successfully!")

except Exception as e:
    print(f"Unsuccessful operation: {e}")
