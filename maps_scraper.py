import sys
import os
import shutil
import spacy


def obtain_places(place, características, city, name):

    tabular_data_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tabular_data")

    if os.path.exists(tabular_data_directory):
        shutil.rmtree(tabular_data_directory)

    os.makedirs(tabular_data_directory)

    current_directory = os.path.dirname(os.path.realpath(__file__))

    google_maps_scraper_directory = os.path.join(current_directory, "google-maps-scraper")
    sys.path.append(google_maps_scraper_directory)
    output_directory = os.path.join(google_maps_scraper_directory, "output")

    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)

    os.chdir(google_maps_scraper_directory)

    import main
    
    if place and características:
        query = f"{place} {características}"
    else:
        query = place

    main.obtain_restaurants(query, city)

    # Obtener el directorio actual
    current_directory = os.getcwd()

    # Formatear el nombre del directorio específico
    city_formatted = city.lower().replace(" ", "-")
    query = query.replace(" ", "-")
    specific_output_directory = os.path.join(current_directory,"output",f"{query}-in-{city_formatted}", "csv")

    try:
        # Obtener la lista de archivos en la carpeta de origen
        archivos = os.listdir(specific_output_directory)

        for file_name in archivos:
            source_path = os.path.join(specific_output_directory, file_name)
            destination_path = os.path.join(os.path.dirname(current_directory), "tabular_data")
            shutil.move(source_path, destination_path)

        archivos= os.listdir(destination_path)
        primer_archivo = archivos[0]
        nuevo_nombre = name.replace(" ","") + ".csv"
        ruta_original = os.path.join(destination_path, primer_archivo)
        nueva_ruta = os.path.join(destination_path, nuevo_nombre)
        os.rename(ruta_original, nueva_ruta)

    except Exception as e:
        print(f"Error al mover y renombrar archivos: {e}")

def extract_entities(text):
    nlp = spacy.load("es_core_news_sm")
    # Procesar la frase con spaCy
    doc = nlp(text)

    # Filtrar sustantivos, adjetivos y palabras clave específicas
    places = ["restaurantes", "comida", "restaurante", "cafetería", "pizzería", "panadería", "pastelería", "bar", "pub", "taberna", "brasería", "asador", "churrería", "heladería", "food truck", "food court", "bufé", "cantina", "chiringuito", "casa de té", "sushi bar", "tapería", "crepería", "delicatessen", "brunch", "fonda", "hamburguesería", "izakaya", "marisquería", "mesón", "noodle bar", "parrilla", "parrillada", "puesto de tacos", "ramen shop", "salad bar", "steakhouse", "taco stand", "taquería", "teatro restaurante", "vinoteca"]
    keywords = []
    capturing_keywords = False

    for token in doc:
        if capturing_keywords and (token.pos_ == "NOUN" or token.pos_ == "ADJ" or token.text.lower() in ["y", "con"]):
            keywords.append(token.text)
        elif token.text.lower() in places:
            capturing_keywords = True

    places = [token.text for token in doc if token.pos_ == "NOUN" or token.text.lower() in ["restaurantes", "comida", "restaurante", "cafetería", "pizzería", "panadería", "pastelería", "bar", "pub", "taberna", "brasería", "asador", "churrería", "heladería", "food truck", "food court", "bufé", "cantina", "chiringuito", "casa de té", "sushi bar", "tapería", "crepería", "delicatessen", "brunch", "fonda", "hamburguesería", "izakaya", "marisquería", "mesón", "noodle bar", "parrilla", "parrillada", "puesto de tacos", "ramen shop", "salad bar", "steakhouse", "taco stand", "taquería", "teatro restaurante", "vinoteca"]]
    # Extraer entidades de tipo LOC (ubicación)
    locations = [ent.text for ent in doc.ents if ent.label_ == "LOC"]

    return places, keywords, locations