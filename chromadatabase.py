import chromadb
import os
import PyPDF2
from chromadb.utils import embedding_functions

def load_collection():
    chroma_client = chromadb.PersistentClient()
    print('Cargando modelo de embeddings...')
    embed_model = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name='sentence-transformers/paraphrase-multilingual-mpnet-base-v2',
        device='cuda',
        normalize_embeddings=True
    )

    collection = chroma_client.get_or_create_collection(name='recipes', embedding_function=embed_model)

    # Ruta a la carpeta con libros
    folder_path = 'llamaindex_data'

    # Obtener la lista de archivos en la carpeta
    files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]

    for book_path in files:
        print(f'Archivo: {book_path}')
        with open(book_path, 'rb') as book:
            documents=[]
            metadata=[]
            ids=[]
            lector = PyPDF2.PdfReader(book)
            for i in range(len(lector.pages)):
                page = lector.pages[i]
                text = page.extract_text()
                documents.append(text)
                metadata.append({'file_path': book_path, 'page_label': i})
                ids.append(f'{book_path}-{i}')
            if len(documents) > 150:
                for i in range(0, len(documents), 150):
                    collection.add(
                        documents=documents[i:i+150],
                        metadatas=metadata[i:i+150],
                        ids=ids[i:i+150]
                    )
            else:
                collection.add(
                    documents=documents,
                    metadatas=metadata,
                    ids=ids
                )

    return collection