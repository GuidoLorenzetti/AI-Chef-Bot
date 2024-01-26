import chromadb
from chromadb.utils import embedding_functions
from llama_index import SimpleDirectoryReader
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.embeddings import HuggingFaceEmbedding
import chromadb

chroma_client = chromadb.PersistentClient()
print('Cargando modelo de embeddings...')
embed_model = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name='sentence-transformers/paraphrase-multilingual-mpnet-base-v2',
    device='cuda',
    normalize_embeddings=True
)

collection = chroma_client.get_or_create_collection(name='recipes1', embedding_function=embed_model)

documents = SimpleDirectoryReader("llamaindex_data").load_data()

# set up ChromaVectorStore and load in data
vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
service_context = ServiceContext.from_defaults(embed_model=embed_model)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, service_context=service_context
)

# Query Data
query_engine = index.as_query_engine()
response = query_engine.query("Receta de pollo")