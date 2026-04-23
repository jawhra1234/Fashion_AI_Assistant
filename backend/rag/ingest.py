import chromadb
from sentence_transformers import SentenceTransformer
import os
from typing import List

class RAGIngestor:
    """
    Ingests fashion rules into ChromaDB vector database.
    """
    
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.db_path = os.path.join(os.path.dirname(__file__), "chroma_db")
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.client.get_or_create_collection("fashion_rules")
    
    def ingest_rules(self, rules_file: str = "rules.txt"):
        """
        Ingest fashion rules from text file into vector database.
        
        Args:
            rules_file: Path to the rules text file
        """
        rules_path = os.path.join(os.path.dirname(__file__), rules_file)
        with open(rules_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split into individual rules (by double newlines or sections)
        rules = self._parse_rules(content)
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(rules)
        
        # Add to ChromaDB
        ids = [f"rule_{i}" for i in range(len(rules))]
        
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=rules,
            ids=ids
        )
        
        print(f"Ingested {len(rules)} fashion rules into database")
    
    def _parse_rules(self, content: str) -> List[str]:
        """
        Parse the rules text into individual rule chunks.
        
        Args:
            content: Raw text content
        
        Returns:
            List of individual rules
        """
        # Split by double newlines and filter out headers
        sections = content.split('\n\n')
        rules = []
        
        for section in sections:
            lines = section.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('- ') or line.startswith('## ') or line.startswith('# '):
                    # Remove bullet points and headers
                    if line.startswith('- '):
                        rules.append(line[2:])
                    elif line.startswith('## ') or line.startswith('# '):
                        rules.append(line[3:])
        
        return rules

if __name__ == "__main__":
    # Change to the rag directory
    os.chdir(os.path.dirname(__file__))
    
    ingestor = RAGIngestor()
    ingestor.ingest_rules()