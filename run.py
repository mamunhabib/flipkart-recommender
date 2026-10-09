from core.data_ingestion import DataIngestor
from core.rag_chain import RAGChainBuilder
from app import create_app

print("Booting up the AI Brain...")

# 1. Connect to the AstraDB Database
vector_store = DataIngestor().get_vector_store()

# 2. Build the LangChain Conversational Pipeline
rag_chain = RAGChainBuilder(vector_store).build_chain()

print("Injecting the AI into the Web Server...")

# 3. Create the Flask App using our factory function
app = create_app(rag_chain)

if __name__ == "__main__":
    print("✅ System Online! Starting server on http://localhost:5000")
    # Start the web server
    app.run(host="0.0.0.0", port=5000, debug=True)
