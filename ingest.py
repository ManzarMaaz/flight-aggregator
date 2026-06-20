import os

from dotenv import load_dotenv
from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.vector_stores.postgres import PGVectorStore
from sqlalchemy import make_url

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 2. Modern Google GenAI Configuration
Settings.llm = GoogleGenAI(model="gemini-2.5-flash")
Settings.embed_model = GoogleGenAIEmbedding()


def ingest_data():
    print("Connecting to Postgres Vector Store...")
    # 4. Initialize Postgres Vector Store (UPGRADED TO 3072)
    url = make_url(DATABASE_URL)
    vector_store = PGVectorStore.from_params(
        database=url.database,
        host=url.host,
        password=url.password,
        port=url.port,
        user=url.username,
        table_name="data_flight_policy",
        embed_dim=3072,
    )

    print("Reading text files from ./data folder...")
    documents = SimpleDirectoryReader("./data").load_data()

    print("Connecting to storage context...")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    print("Chunking, Embedding, and pushing to Postgres...")
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, show_progress=True
    )
    print("Ingestion complete! Data successfully saved.")


if __name__ == "__main__":
    ingest_data()
