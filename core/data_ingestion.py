from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from core.config import Config
from core.data_converter import DataConverter

class DataIngestor:
    def __init__(self):
        print("Initializing Local HuggingFace Model & Connecting to AstraDB...")
        
        # -------------------------------------------------------------------
        # STEP 1: INITIALIZE THE LOCAL EMBEDDING MODEL
        # -------------------------------------------------------------------
        # This downloads the model to your Mac/Pod and runs it locally for FREE.
        self.embedding = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)

        # -------------------------------------------------------------------
        # STEP 2: CONNECT TO THE DATABASE (AND GLUE THEM TOGETHER)
        # -------------------------------------------------------------------
        # LangChain forces us to pass the 'embedding' object directly into 
        # the database here. This is because the database needs to know exactly 
        # how to translate English into Math before it can store anything!
        self.vstore = AstraDBVectorStore(
            embedding=self.embedding,
            collection_name="flipkart_database",
            api_endpoint=Config.ASTRA_DB_API_ENDPOINT,
            token=Config.ASTRA_DB_APPLICATION_TOKEN,
            namespace=Config.ASTRA_DB_KEYSPACE
        )

    def ingest(self):
        """Extracts data via the converter and loads it into AstraDB"""
        # Step 1: Data Conversion (Extract & Transform)
        converter = DataConverter()
        docs = converter.convert()
        
        # Step 2: Data Ingestion (Load to Cloud)
        print(f"Pushing {len(docs)} vectors to AstraDB. This may take a moment...")
        self.vstore.add_documents(docs)
        print("✅ Data ingestion complete! Vectors are securely stored in the cloud.")
        
        return self.vstore

    def get_vector_store(self):
        """Returns the database connection without re-ingesting the data"""
        return self.vstore

# If executed directly from the terminal, trigger the ingestion process
if __name__ == "__main__":
    ingestor = DataIngestor()
    ingestor.ingest()
