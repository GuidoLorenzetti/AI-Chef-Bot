from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.embeddings import LangchainEmbedding
from llama_index import ServiceContext
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from jinja2 import Template
import requests
from decouple import config

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
      "Dada la información de contexto anterior, y sin utilizar conocimiento previo, responde en español la siguiente pregunta. Agrega en caso de que se necesite la receta, con título, ingredientes, procedimiento y meciona en que página de que libro se encuentra sin agregarle al título el nombre de la carpeta que es llamaindex_data. No debes agregar recetas de otros libros ni material adicional. En caso de que la receta pedida no se encuentre en el material provisto debes aclararlo. No añadas el nombre de la carpeta de los libros en las respuestas\n"
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
    # Cargamos nuestro modelo de embeddings
    print('Cargando modelo de embeddings...')
    embed_model = LangchainEmbedding(
        HuggingFaceEmbeddings(model_name='sentence-transformers/paraphrase-multilingual-mpnet-base-v2'))

    # Construimos un índice de documentos a partir de los datos de la carpeta llamaindex_data
    print('Indexando documentos...')
    # Create a service context with the custom embedding model
    documents = SimpleDirectoryReader("llamaindex_data").load_data()
    index = VectorStoreIndex.from_documents(documents, show_progress=True,
                                            service_context=ServiceContext.from_defaults(embed_model=embed_model, llm=None))

    # Construimos un retriever a partir del índice, para realizar la búsqueda vectorial de documentos
    retriever = index.as_retriever(similarity_top_k=2)

    return retriever

def get_answer(retriever, query_str:str):
    nodes = retriever.retrieve(query_str)
    final_prompt = prepare_prompt(query_str, nodes)
    return generate_answer(final_prompt)