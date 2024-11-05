# RAG_Project

For my ML course project

## Project Overview

This project aims to develop a Conversational AI assistant that helps users with queries related to medical leave (ML) and on-duty (OD) leave applications. The project utilizes various machine learning models and tools to process and respond to user queries effectively.

## Project Structure
```
-|
 |-Chroma_set.py
 |-od-|
      |-od-ml-curated.csv
      |-od-ml-raw.csv
 |-README.md
 |-requirement.txt
 |-run_model.py
```

### Files and Directories
- **Chroma_set.py:** Script to initialize and populate the ChromaDB with embeddings and metadata from the dataset.
- **od/:** Directory containing CSV files with curated and raw data related to ML and OD leave applications.
    - **od-ml-curated.csv:** Curated dataset with metadata, questions, and answers.
    - **od-ml-raw.csv:** Raw dataset with detailed descriptions and procedures.
- **README.md:** This file, providing an overview of the project.
- **requirement.txt:** List of dependencies required to run the project.
- **run_model.py:** Script to run the Conversational AI model using the LLaMA 3.1 8B model and ChromaDB for context retrieval.

### Setup Instructions
1. Clone the repository to your local machine.
   ```
    git clone <repository-url>
    cd RAG_Project
   ```
2. Install the required dependencies using the `requirement.txt` file.
    ```
     pip install -r requirement.txt
    ```
3. Run the `run_model.py` script to start the Conversational AI model.
    ```
    python run_model.py
    ```
4. Follow the instructions provided by the model to interact with the Conversational AI assistant.

Alternatively, you can seed the database with embeddings and metadata using the `Chroma_set.py` script before running the model.

### Dependencies 
- chromadb
- ollama
- langchain
- rich
- pandas
- scikit-learn
- transformers

## Contributors

> - [Suvan GS](https://github.com/greeenboi)
> - [Mohammed Ariffin](https://github.com/MohammedAriffin)
> - [Ishan Roy](https://github.com/royishan2004)