import ollama, chromadb
from langchain_ollama import OllamaLLM
from rich.console import Console

# Initialize Rich Console for output
console = Console()

# Load the LLaMA 3.1 8B model
llm = OllamaLLM(model="llama3.1")

# Template system prompt setup for the LLaMA model
system_prompt = """
You are a Conversational AI assistant helping the user. Below we provide the user prompt and a context prompt for the conversation.
If the context prompt is semantically related to the user prompt, respond to the user prompt with respect to the context prompt.
Otherwise, respond to the user prompt based on your own understanding.
"""

# Get user input
user_prompt = input("Enter your prompt: ")

# Initialize ChromaDB client to retrieve the context prompt
client = chromadb.PersistentClient(path=r"./data")  # Access vector DB
collection = client.get_collection(name="my_data")  # Access the collection

# Generate embedding for the user query
model = "nomic-embed-text"  # The text embedding model
user_query_embedding = ollama.embeddings(model=model, prompt=user_prompt)['embedding']  # Get the embedding for the user prompt

# Perform cosine similarity search to retrieve the most relevant context prompts
try:
    context_results = collection.query(query_embeddings=[user_query_embedding], n_results=2)  # Query the DB
    # Filter and concatenate relevant context results into a single string
    context_prompt = " ".join(
        [doc for doc, score in zip(context_results['documents'], context_results['distances']) if score <= 0.3]
    ) or "No relevant context found."
except Exception as e:
    context_prompt = "No relevant context found."
    console.print(f"[red]Error during context retrieval: {e}[/red]")

# Combine the system, user, and context prompts into a conversation
conversation = f"System: {system_prompt}\nUser: {user_prompt}\nContext: {context_prompt}"

# Generate text using Ollama with the LLaMA 3.1 8B model
response = llm.invoke(conversation)

# Output the response from the model
console.print("[bold green]Response from AI:[/bold green]\n", response)
