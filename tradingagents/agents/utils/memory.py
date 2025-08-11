import os
import chromadb
from chromadb.config import Settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from openai import OpenAI


class FinancialSituationMemory:
    def __init__(self, name, config):
        self.config = config
        self.llm_provider = config.get("llm_provider", "openai")
        
        # Initialize embedding model and client based on provider
        if self.llm_provider == "google":
            # For Google provider, we'll use a simple text-based embedding method 
            # to avoid async issues with the Google gRPC client
            print("Note: Using simple text-based embeddings for Google provider to avoid async issues")
            self.embedding = None
            self.client = None
            self.embedding_model = None
        else:
            # Use OpenAI API for embeddings (works with OpenAI, Anthropic, Ollama)
            if config["backend_url"] == "http://localhost:11434/v1":
                self.embedding = "nomic-embed-text"
            else:
                self.embedding = "text-embedding-3-small"
            self.client = OpenAI(base_url=config["backend_url"])
            self.embedding_model = None

        self.chroma_client = chromadb.Client(Settings(allow_reset=True))
        self.situation_collection = self.chroma_client.create_collection(name=name)

    def get_embedding(self, text):
        """Get embedding for text using the appropriate provider"""
        if self.llm_provider == "google":
            # Use a simple text-based embedding for Google to avoid async issues
            # This creates consistent embeddings based on text content
            import hashlib
            
            # Create a deterministic embedding from text
            text_bytes = text.encode('utf-8')
            hash_obj = hashlib.sha256(text_bytes)
            hash_hex = hash_obj.hexdigest()
            
            # Convert hash to embedding vector (384 dimensions)
            embedding = []
            for i in range(0, min(len(hash_hex), 96), 2):  # 96 hex chars = 48 bytes = 384 bits
                byte_val = int(hash_hex[i:i+2], 16)
                # Convert each byte to 8 float values between -1 and 1
                for bit in range(8):
                    bit_val = (byte_val >> bit) & 1
                    embedding.append((bit_val * 2) - 1)  # Convert 0,1 to -1,1
            
            # Pad to 384 dimensions if needed
            while len(embedding) < 384:
                embedding.append(0.0)
            
            return embedding[:384]
        else:
            # Use OpenAI API (works for OpenAI, Anthropic, Ollama)
            response = self.client.embeddings.create(
                model=self.embedding, input=text
            )
            return response.data[0].embedding

    def add_situations(self, situations_and_advice):
        """Add financial situations and their corresponding advice. Parameter is a list of tuples (situation, rec)"""

        situations = []
        advice = []
        ids = []
        embeddings = []

        offset = self.situation_collection.count()

        for i, (situation, recommendation) in enumerate(situations_and_advice):
            situations.append(situation)
            advice.append(recommendation)
            ids.append(str(offset + i))
            embeddings.append(self.get_embedding(situation))

        self.situation_collection.add(
            documents=situations,
            metadatas=[{"recommendation": rec} for rec in advice],
            embeddings=embeddings,
            ids=ids,
        )

    def get_memories(self, current_situation, n_matches=1):
        """Find matching recommendations using appropriate embedding provider"""
        query_embedding = self.get_embedding(current_situation)

        results = self.situation_collection.query(
            query_embeddings=[query_embedding],
            n_results=n_matches,
            include=["metadatas", "documents", "distances"],
        )

        matched_results = []
        for i in range(len(results["documents"][0])):
            matched_results.append(
                {
                    "matched_situation": results["documents"][0][i],
                    "recommendation": results["metadatas"][0][i]["recommendation"],
                    "similarity_score": 1 - results["distances"][0][i],
                }
            )

        return matched_results


if __name__ == "__main__":
    # Example usage
    config = {
        "llm_provider": "openai",  # or "google" 
        "backend_url": "https://api.openai.com/v1"
    }
    matcher = FinancialSituationMemory("example_memory", config)

    # Example data
    example_data = [
        (
            "High inflation rate with rising interest rates and declining consumer spending",
            "Consider defensive sectors like consumer staples and utilities. Review fixed-income portfolio duration.",
        ),
        (
            "Tech sector showing high volatility with increasing institutional selling pressure",
            "Reduce exposure to high-growth tech stocks. Look for value opportunities in established tech companies with strong cash flows.",
        ),
        (
            "Strong dollar affecting emerging markets with increasing forex volatility",
            "Hedge currency exposure in international positions. Consider reducing allocation to emerging market debt.",
        ),
        (
            "Market showing signs of sector rotation with rising yields",
            "Rebalance portfolio to maintain target allocations. Consider increasing exposure to sectors benefiting from higher rates.",
        ),
    ]

    # Add the example situations and recommendations
    matcher.add_situations(example_data)

    # Example query
    current_situation = """
    Market showing increased volatility in tech sector, with institutional investors 
    reducing positions and rising interest rates affecting growth stock valuations
    """

    try:
        recommendations = matcher.get_memories(current_situation, n_matches=2)

        for i, rec in enumerate(recommendations, 1):
            print(f"\nMatch {i}:")
            print(f"Similarity Score: {rec['similarity_score']:.2f}")
            print(f"Matched Situation: {rec['matched_situation']}")
            print(f"Recommendation: {rec['recommendation']}")

    except Exception as e:
        print(f"Error during recommendation: {str(e)}")
