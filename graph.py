import networkx as nx
import matplotlib.pyplot as plt
from rdflib import Graph, URIRef, RDF, RDFS
import urllib.parse
import os

def create_graph(datos_usuario, usuario):

    # Crear un grafo dirigido
    G = nx.DiGraph()

    # # Obtener el nombre del usuario
    # usuario = list(datos_usuario.keys())[0]

    # # Obtener el subdiccionario
    # datos_usuario = datos_usuario[usuario]

    # Agregar el nodo principal
    G.add_node(usuario, label="Usuario")

    # Agregar nodos secundarios y ejes con etiquetas
    for key, value in datos_usuario.items():
        # Convertir listas a cadenas
        if isinstance(value, list):
            value = ', '.join(value)
        
        G.add_node(value, label=key)
        G.add_edge(usuario, value, label=key)

    datos_usuario = obtain_non_consumible_ingredients(datos_usuario)

    value = ', '.join(datos_usuario['ingredientes_no_consumir'])
    value1 = ', '.join(datos_usuario['alergias'])
    G.add_node(value, label="Ingredientes no consumir")
    G.add_edge(datos_usuario['dieta'], value, label="Ingredientes no consumir")
    G.add_edge(datos_usuario['sensibilidad'], value, label="Ingredientes no consumir")
    G.add_edge(value1, value, label="Ingredientes no consumir")

    # pos = nx.spring_layout(G, seed=42)
    # labels = nx.get_edge_attributes(G, 'label')
    # nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=8, font_color="black", font_weight="bold", font_family="sans-serif")
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # # Mostrar el grafo
    # plt.show()

    # Create an RDF graph
    rdf_graph = Graph()

    # Define vocabulary prefixes
    rdf_graph.bind("rdf", RDF)
    rdf_graph.bind("rdfs", RDFS)

    # Transform nodes to RDF resources
    for node in G.nodes:
        # Convert node to string
        node_str = str(node)
        encoded_node = urllib.parse.quote(node_str, safe='')
        subject_uri = URIRef(f"http://example.org/node/{encoded_node}")

        rdf_graph.add((subject_uri, RDF.type, URIRef("http://example.org/ontology/Node")))

    # Transform edges to RDF triples
    for edge in G.edges:
        # Convert nodes to strings
        subject_str = str(edge[0])
        object_str = str(edge[1])

        # Codify directly without the need for encode
        encoded_subject = urllib.parse.quote(subject_str, safe='')
        encoded_object = urllib.parse.quote(object_str, safe='')

        subject_uri = URIRef(f"http://example.org/node/{encoded_subject}")
        object_uri = URIRef(f"http://example.org/node/{encoded_object}")

        # Use the same relation label as in NetworkX (edge[2])
        relation_label = str(G[edge[0]][edge[1]]['label']) if 'label' in G[edge[0]][edge[1]] else "knows"

        # Replace spaces and commas with underscores in the relation label
        relation_label = relation_label.replace(' ', '_').replace(',', '_')

        rdf_graph.add((subject_uri, URIRef(f"http://example.org/ontology/{relation_label}"), object_uri))

    # Crear la carpeta si no existe
    folder_path = 'graph_databases'
    os.makedirs(folder_path, exist_ok=True)

    # Serialise and print the RDF graph (Turtle format)
    rdf_graph.serialize(destination=os.path.join(folder_path, f'rdf_{usuario}_database.ttl'), format='turtle')

def obtain_non_consumible_ingredients(dict):
    dict['ingredientes_no_consumir'] = []

    if dict['dieta'] == 'Vegana':
        dict['ingredientes_no_consumir'].append('Productos de origen animal')

    elif dict['dieta'] == 'Vegetariana':
        dict['ingredientes_no_consumir'].append('Carne')

    elif dict['dieta'] == 'Cetogenica':
        dict['ingredientes_no_consumir'].append('Carbohidratos')

    if dict['sensibilidad'] == 'Celiaquia':
        dict['ingredientes_no_consumir'].append('Gluten')

    elif dict['sensibilidad'] == 'Sensibilidad':
        dict['ingredientes_no_consumir'].append('Ingredientes específicos que causan sensibilidad al gluten')

    if 'Ninguna' not in dict['alergias']:
        dict['ingredientes_no_consumir'].extend(dict['alergias'])

    return dict