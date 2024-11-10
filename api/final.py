import pandas as pd
import chromadb
from langchain_ollama import OllamaLLM
from rich.console import Console
from typing import List

class ODMLAssistant:
    def __init__(self, csv_path: str = "./public/od/od-ml-curated.csv", db_path: str = "./data", collection_name: str = "od_ml_data"):
        self.console = Console()
        self.llm = OllamaLLM(model="llama3.1")
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Create or get collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            self.console.print("[green]Found existing collection[/green]")
        except Exception:
            self.collection = self.client.create_collection(name=collection_name , metadata={"hnsw:space": "cosine"})
            self.console.print("[yellow]Created new collection[/yellow]")
            self._load_data(csv_path)
        
        self.system_prompt = """
        You are an AI assistant specifically trained to help students with OD (On-Duty) and ML (Medical Leave) related queries 
        at SRM Institute. Use the provided context to answer questions about leave application procedures, requirements, and rules. 
        If the context contains relevant information, use it to provide accurate answers. If no relevant context is found, 
        inform the user that you don't have specific information about that aspect.
        """

    def _load_data(self, csv_path: str):
        """Load data from CSV into ChromaDB."""
        try:
            # Prepare data for ChromaDB
            df = pd.read_csv(csv_path)
            documents = []
            metadatas = []
            ids = [str(i) for i in df['ids'].tolist()]
            for index, row in df.iterrows():
                combined_text = f"{row['question']} {row['answer']}"
                documents.append(combined_text)
                metadatas.append({'category': row['metadata']})
            
            # Add data to collection without custom embeddings
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            self.console.print("[green]Successfully loaded data into ChromaDB with default embeddings[/green]")

            # Optional: Verify by querying a sample ID to ensure it’s accessible
            try:
                sample_result = self.collection.get(ids=[ids[0]])
                self.console.print(f"Sample document check: {sample_result}")
                
            except Exception as e:
                self.console.print(f"[red]Error verifying data insertion: {e}[/red]")
                

        except Exception as e:
            self.console.print(f"[red]Error loading data: {e}[/red]")

    def search_context(self, user_prompt: str, min_contexts: int = 3, n_results: int = 5) -> str:
        """Search for relevant context using vector similarity, returning the top contexts based on closest distances."""
        try:
            # Perform the similarity search with default embedding
            results = self.collection.query(
                query_texts=[user_prompt],
                n_results=n_results,
                #where_document={"$contains": user_prompt},
                include=["documents", "distances"]
            )
            
            # Gather top results regardless of a distance threshold
            relevant_contexts = []
            for doc in results['documents'][0]:
                context = f"Answer: {doc}"
                print(context)
                relevant_contexts.append(context)
                if len(relevant_contexts) >= min_contexts:
                    break
                    
            # Check if we have sufficient context results
            if len(relevant_contexts) < min_contexts:
                print("no data found")
                return "No sufficient relevant information found in the OD/ML knowledge base."
                
            
            return "\n\n".join(relevant_contexts)
        
        except Exception as e:
            self.console.print(f"[red]Error during context search: {e}[/red]")
            return "Error accessing the OD/ML knowledge base."

    def generate_response(self, user_prompt: str) -> str:
        """Generate a response based on user prompt and relevant context."""
        # Search for relevant context
        context_prompt = self.search_context(user_prompt)
        
        # Construct the full conversation prompt
        conversation = f"""System: {self.system_prompt}
User Question: {user_prompt}
Relevant Information:
{context_prompt}

Please provide an answer based on the above information."""

        # Generate response using the LLM
        try:
            print(conversation)
            response = self.llm.invoke(conversation)
            return response
        except Exception as e:
            self.console.print(f"[red]Error generating response: {e}[/red]")
            return f"Error generating response: {str(e)}"

def main():
    # Initialize the assistant
    assistant = ODMLAssistant()
    console = Console()
    
    while True:
        # Get user input
        user_prompt = input("\nEnter your question about OD/ML (or 'quit' to exit): ")
        
        if user_prompt.lower() == 'quit':
            break
            
        # Generate and display response
        response = assistant.generate_response(user_prompt)
        console.print("\n[bold green]Response:[/bold green]")
        console.print(response)
        console.print("\n" + "="*50)

if __name__ == "__main__":
    main()
