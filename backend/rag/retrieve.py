import chromadb
from sentence_transformers import SentenceTransformer
import os
from typing import List

class RAGRetriever:
    """
    Retrieves relevant fashion rules from ChromaDB based on user queries.
    """
    
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        db_path = os.path.join(os.path.dirname(__file__), "chroma_db")
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection("fashion_rules")
    
    def retrieve_rules(self, query: str, top_k: int = 5) -> List[str]:
        """
        Retrieve top-k relevant fashion rules for a given query.
        
        Args:
            query: User query (e.g., occasion)
            top_k: Number of rules to retrieve
        
        Returns:
            List of relevant fashion rules
        """
        try:
            # Generate embedding for the query
            query_embedding = self.embedding_model.encode([query])[0]
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k
            )
            
            # Extract documents
            rules = results['documents'][0] if results['documents'] else []
            
            return rules
        
        except Exception as e:
            print(f"Error retrieving rules: {e}")
            return ["General fashion advice: Wear what makes you feel confident and comfortable."]

if __name__ == "__main__":
    # Test retrieval
    retriever = RAGRetriever()
    rules = retriever.retrieve_rules("casual outing")
    print("Retrieved rules:")
    for rule in rules:
        print(f"- {rule}")