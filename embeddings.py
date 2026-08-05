from langchain_ollama import OllamaEmbeddings

def embedding_function():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings