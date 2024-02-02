from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.embeddings import LangchainEmbedding
from llama_index import ServiceContext
from llama_index import VectorStoreIndex
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores import ChromaVectorStore
from jinja2 import Template
import requests
from decouple import config
import torch
from chromadatabase import load_collection
import nltk
from maps_scraper import *
import pandas as pd
import pickle
from time import sleep

nltk.download('stopwords')
from nltk.corpus import stopwords

spanish_stop_words = stopwords.words('spanish')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"PyTorch está utilizando el dispositivo: {device}")

HUGGINGFACE_TOKEN=config('HUGGINGFACE_TOKEN')

def zephyr_instruct_template(messages, add_generation_prompt=True):
    # Definir la plantilla Jinja
    template_str = "{% for message in messages %}"
    template_str += "{% if message['role'] == 'user' %}"
    template_str += "<|user|>{{ message['content'] }}</s>\n"
    template_str += "{% elif message['role'] == 'assistant' %}"
    template_str += "<|assistant|>{{ message['content'] }}</s>\n"
    template_str += "{% elif message['role'] == 'system' %}"
    template_str += "<|system|>{{ message['content'] }}</s>\n"
    template_str += "{% else %}"
    template_str += "<|unknown|>{{ message['content'] }}</s>\n"
    template_str += "{% endif %}"
    template_str += "{% endfor %}"
    template_str += "{% if add_generation_prompt %}"
    template_str += "<|assistant|>\n"
    template_str += "{% endif %}"

    # Crear un objeto de plantilla con la cadena de plantilla
    template = Template(template_str)

    # Renderizar la plantilla con los mensajes proporcionados
    return template.render(messages=messages, add_generation_prompt=add_generation_prompt)


# Aquí hacemos la llamada el modelo
def generate_answer(prompt: str, max_new_tokens: int = 768) -> None:
    try:
        # Tu clave API de Hugging Face
        api_key = config('HUGGINGFACE_TOKEN')

        # URL de la API de Hugging Face para la generación de texto
        api_url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

        # Cabeceras para la solicitud
        headers = {"Authorization": f"Bearer {api_key}"}

        # Datos para enviar en la solicitud POST
        # Sobre los parámetros: https://huggingface.co/docs/transformers/main_classes/text_generation
        data = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "temperature": 0.7,
                "top_k": 50,
                "top_p": 0.95
            }
        }

        # Realizamos la solicitud POST
        response = requests.post(api_url, headers=headers, json=data)

        # Extraer respuesta
        respuesta = response.json()[0]["generated_text"][len(prompt):]
        return respuesta

    except Exception as e:
        print(f"An error occurred: {e}")

# Esta función prepara el prompt en estilo QA
def prepare_prompt(query_str: str, nodes: list):
  TEXT_QA_PROMPT_TMPL = (
      "La información de contexto es la siguiente:\n"
      "---------------------\n"
      "{context_str}\n"
      "---------------------\n"
      "RESPONDE EN ESPAÑOL. Dada la información de contexto anterior, y sin utilizar conocimiento previo, responde en español la siguiente consulta. En caso de que tu respuesta sea una receta envíala con título, ingredientes, procedimiento y meciona en que página de que libro se encuentra sin agregarle al título el nombre de la carpeta que es llamaindex_data. No debes agregar recetas de otros libros ni material adicional. En caso de que la receta pedida no se encuentre en el material provisto debes aclararlo y no enviar receta. No añadas el directorio de los libros en las respuestas.\n"
      "Pregunta: {query_str}\n"
      "Respuesta: "
  )

  # Construimos el contexto de la pregunta
  context_str = ''
  for node in nodes:
      page_label = node.metadata["page_label"]
      file_path = node.metadata["file_path"]
      context_str += f"\npage_label: {page_label}\n"
      context_str += f"file_path: {file_path}\n\n"
      context_str += f"{node.text}\n"

  messages = [
      {
          "role": "system",
          "content": "Eres un asistente de cocina útil que siempre responde con respuestas veraces, útiles y basadas en hechos.",
      },
      {"role": "user", "content": TEXT_QA_PROMPT_TMPL.format(context_str=context_str, query_str=query_str)},
  ]

  final_prompt = zephyr_instruct_template(messages)
  return final_prompt

def load_model():
    
    print('Cargando modelo de embeddings...')
    embed_model = LangchainEmbedding(HuggingFaceEmbeddings(
        model_name='sentence-transformers/paraphrase-multilingual-mpnet-base-v2',
        model_kwargs={'device': 'cuda'},
        encode_kwargs={'normalize_embeddings': True}
    )
    )
    print('Indexando documentos...')
    chroma_collection = load_collection()

    # set up ChromaVectorStore and load in data
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=None)
    index = VectorStoreIndex.from_vector_store(
        vector_store, storage_context=storage_context, service_context=service_context, show_progress=True
    )

    retriever = index.as_retriever(similarity_top_k=2)

    return retriever

def clas(query_str: str, clasificador, vectorizer, retriever):
    vectorized_query = vectorizer.transform([query_str])
    prediction = clasificador.predict(vectorized_query)
    print(prediction)
    if prediction[0] == 1:
        print(query_str)
        answer = get_answer(retriever, query_str)
        return answer
    else:
        resultados=[]
        places, keywords, locations = extract_entities(query_str)
        print(places, keywords, locations)
        obtain_places(places[0], " ".join(keywords), locations[0], query_str)
        # Seleccionar los primeros 5 restaurantes

        df = pd.read_csv(os.path.dirname(os.path.abspath(__file__))+"/tabular_data/" + query_str.replace(" ","") + ".csv")

        primeros_5 = df.head(5)
        
        # Generar el resultado escrito
        for index, restaurante in primeros_5.iterrows():
            resultado_escrito = ""
            resultado_escrito += f"Restaurante: {restaurante['name']}\n"
            resultado_escrito += f"Enlace: {restaurante['link']}\n"
            resultado_escrito += f"Calificación: {restaurante['rating']}\n"
            resultado_escrito += f"Dirección: {restaurante['address']}\n\n"
            resultados.append(resultado_escrito)
        return resultados
    
def get_answer(retriever, query_str:str):
    nodes = retriever.retrieve(query_str)
    final_prompt = prepare_prompt(query_str, nodes)
    return generate_answer(final_prompt)