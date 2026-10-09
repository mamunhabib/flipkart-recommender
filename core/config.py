import os
from dotenv import load_dotenv

# Securely load the secrets from the hidden .env file
load_dotenv()

class Config:
    # --------------------------------------------------------
    # 1. DATABASE CONFIGURATION (AstraDB)
    # --------------------------------------------------------
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE", "default_keyspace")

    # --------------------------------------------------------
    # 2. EMBEDDING MODEL CONFIGURATION (HuggingFace)
    # --------------------------------------------------------
    # This model converts product text into mathematical vectors for the database.
    # We load the HF token because the tutorial uses the HuggingFace Cloud API.
    HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
    
    # --------------------------------------------------------
    # 3. GENERATION MODEL CONFIGURATION (Groq LLM)
    # --------------------------------------------------------
    # This model reads the retrieved data and generates the conversational answer.
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    RAG_MODEL = "openai/gpt-oss-20b"

    # --------------------------------------------------------
    # 4. MEMORY CONFIGURATION (Redis)
    # --------------------------------------------------------
    # This URL connects to our Redis memory store. We default to localhost
    # so we can test it locally before pushing to the Kubernetes cluster.
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
