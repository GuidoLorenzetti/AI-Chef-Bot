from rdflib import Graph, Namespace

def generate_context(user):
    # Cargar el grafo RDF desde un archivo o fuente
    g = Graph()
    g.parse(f"graph_databases/rdf_{user}_database.ttl", format="turtle")  # Asegúrate de especificar el formato correcto

    ns1 = Namespace("http://example.org/ontology/")

    # Construir la consulta SPARQL con el número de usuario
    query = f"""
        SELECT ?nombre ?edad ?alergias ?comidas_preferidas ?comidas_menos_preferidas ?sensibilidad WHERE {{
            <http://example.org/node/{user}> ns1:nombre ?nombre ;
                                                ns1:edad ?edad ;
                                                ns1:alergias ?alergias ;
                                                ns1:comidas_preferidas ?comidas_preferidas ;
                                                ns1:comidas_menos_preferidas ?comidas_menos_preferidas ;
                                                ns1:sensibilidad ?sensibilidad .
        }}
    """

    # Ejecutar la consulta
    results = g.query(query)

    # Imprimir los resultados
    for r in results:
        nombre = str(r['nombre'].split('/')[-1])
        edad = str(r['edad'].split('/')[-1])
        alergias = str(r['alergias'].split('/')[-1]).replace('_', ', ')
        
        # Obtener los valores directos para comidas_preferidas y comidas_menos_preferidas
        comidas_preferidas = str(r['comidas_preferidas'].split('/')[-1]).replace('_', ', ')
        comidas_menos_preferidas = str(r['comidas_menos_preferidas'].split('/')[-1]).replace('_', ', ')
        
        sensibilidad = str(r['sensibilidad'].split('/')[-1])

        context = f"""
        Nombre: {nombre}
        Edad: {edad}
        Alergias: {alergias}
        Comidas preferidas: {comidas_preferidas}
        Comidas menos preferidas: {comidas_menos_preferidas}
        Sensibilidad: {sensibilidad}
        """

        return context

