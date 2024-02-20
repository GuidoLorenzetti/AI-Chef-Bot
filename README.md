<h1 align="center">
  <br>
  <img src="https://raw.githubusercontent.com/GuidoLorenzetti/AI-Chef-Bot/main/app/styles/logo1-removebg-preview.png" alt="AICHEFBOT" width="200"></a>
  <br>
  AI-Chef-Bot
  <br>
</h1>

<p align="center">
  <a href="#requerimientos">Requerimientos</a> •
  <a href="#¿Cómo-usar?">¿Cómo usar?</a> •
  <a href="#En-Telegram">En Telegram</a> •
  <a href="#Créditos">Créditos</a> •
</p>

<div style="text-align: justify;">

AI Chef Bot es un bot de Telegram que pretende ser tu asistente personal en tus recetas de cocina. Puedes preguntarle por recetas, ingredientes, y mucho más. Además, cuenta con una funcionalidad de búsqueda de restaurantes cercanos a tu ubicación.

</div>

## Requerimientos

- Python 3.10
- pip 23.3.2
- virtualenv 20.6.0

## ¿Cómo usar?

Desde tu consola de comandos

```bash
# Clona el repositorio
$ git clone https://github.com/GuidoLorenzetti/AI-Chef-Bot.git

# Crea un entorno virtual
$ python -m venv chef-bot

# Activa el entorno virtual
$ source chef-bot/bin/activate

# Accede al repositorio
$ cd AI-Chef-Bot

# Instala las dependencias
$ pip install -r requirements.txt

# Corre el bot
$ python bot.py
```

## En Telegram

Busca a `@Linguinia_bot` y comienza a chatear con él, o sigue este [enlace](https://t.me/Linguinia_bot).

![screenshot](https://raw.githubusercontent.com/GuidoLorenzetti/AI-Chef-Bot/main/app/telegram/screenshot%20(1).png)

![screenshot](https://raw.githubusercontent.com/GuidoLorenzetti/AI-Chef-Bot/main/app/telegram/screenshot%20(2).png)

![screenshot](https://raw.githubusercontent.com/GuidoLorenzetti/AI-Chef-Bot/main/app/telegram/screenshot%20(3).png)

![screenshot](https://raw.githubusercontent.com/GuidoLorenzetti/AI-Chef-Bot/main/app/telegram/screenshot%20(4).png)

![screenshot](https://raw.githubusercontent.com/GuidoLorenzetti/AI-Chef-Bot/main/app/telegram/screenshot%20(5).png)

![screenshot](https://raw.githubusercontent.com/GuidoLorenzetti/AI-Chef-Bot/main/app/telegram/screenshot%20(6).png)

## Estructura General

La arquitectura general del bot de Telegram es la siguiente:

![screenshot](https://raw.githubusercontent.com/GuidoLorenzetti/AI-Chef-Bot/main/app/styles/Esquema.png)


## Funcionamiento

<div style="text-align: justify;">

El propósito de este proyecto es desarrollar un bot lo mas amigable con el usuario posible. Para ello, se utilizaron distintas herramientas de **NLP** y **Web Scraping** para obtener información de recetas y restaurantes.
El repositorio cuenta con los siguientes scripts:

* `bot.py`: Script principal que corre el bot de Telegram y gestiona las respuestas a los mensajes. Además es el encargado de obtener las respuestas del usuario al formulario del perfil para generar una base de datos de conocimiento personalizada.
* `chatbot.py`: Es el módulo encargado de gestionar el chatbot de IA. Ingluye los siguientes métodos:
  - load_model: Obtiene la base de datos de chromadb y carga en memoria el retriever.
  - clas: Clasifica el prompt del usuario para elegir que acciones ejecutar.
  - get_answer: Obtiene la respuesta del chatbot a partir de un mensaje de entrada.
* `chromadabase.py`: Se encarga de cargar los documentos de la carpeta llamaindex_data en una base de datos chromadb
* `clasifier.py`: Se utilizó para entrenar un clasificador de texto que clasifica los mensajes de entrada en distintas categorías (Puede ser reutilizado para futuras actualizaciones).
* `graph.py`: Diseña la base de datos rdf del usuario.
* `context.py`: Obtiene la base de datos rdf del usuario y genera un contexto para el chatbot. Esto permite obtener respuestas mas personalizadas.
* `maps_scraper.py`: Este módulo, en conjunto con el repositorio google-maps-scraper, permiten obtener los lugares de comida que especifique el usuario. A partir de ello se guardan en un dataframe en la carpeta tabular_data y se devuelve al usuario los resultados obtenidos. Se puede modificar para mostrar mas o menos resultados en los mensajes.


</div>

## Créditos

<div style="text-align: justify;">

Este proyecto fue creado por [Guido Lorenzetti](https://github.com/GuidoLorenzetti) como trabajo práctico final para la materia **Procesamiento de Lenguaje Natural** de la carrera *Tecnicatura Universitaria en Inteligencia Artificial*.

Agradecimientos especiales a los desarrolladores de [Google Maps Scraper](https://github.com/omkarcloud/google-maps-scraper?tab=readme-ov-file) por crear una herramienta de código abierto de tan alta calidad.

</div>