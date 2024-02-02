from rdflib import Graph, Namespace

user = "6319966688"
# Cargar el grafo RDF desde un archivo o fuente
g = Graph()
g.parse(f"graph_databases/rdf_{user}_database.ttl", format="turtle")  # Asegúrate de especificar el formato correcto

# Definir el espacio de nombres
ns1 = Namespace("http://example.org/ontology/")

# Consulta SPARQL para obtener la información de la persona
query = """
    SELECT ?nombre ?edad ?alergias ?comidas_preferidas ?comidas_menos_preferidas ?sensibilidad WHERE {
        <http://example.org/node/6319966688> ns1:nombre ?nombre ;
                                            ns1:edad ?edad ;
                                            ns1:alergias ?alergias ;
                                            ns1:comidas_preferidas ?comidas_preferidas ;
                                            ns1:comidas_menos_preferidas ?comidas_menos_preferidas ;
                                            ns1:sensibilidad ?sensibilidad .

        BIND(REPLACE(?comidas_preferidas_raw, " ", "_") AS ?comidas_preferidas)
        BIND(REPLACE(?comidas_menos_preferidas_raw, " ", "_") AS ?comidas_menos_preferidas)
    }
"""

# Ejecutar la consulta
results = g.query(query)

# Imprimir los resultados
for r in results:
    nombre = str(r['nombre'].split('/')[-1])
    edad = str(r['edad'].split('/')[-1])
    alergias = str(r['alergias'].split('/')[-1])
    comidas_preferidas = str(r['comidas_preferidas'].split('/')[-1])
    comidas_menos_preferidas = [str(comida.split('/')[-1]) for comida in r['comidas_menos_preferidas']]
    sensibilidad = str(r['sensibilidad'].split('/')[-1])

    print(f"Nombre: {nombre}")
    print(f"Edad: {edad}")
    print(f"Alergias: {alergias}")
    print(f"Comidas preferidas: {', '.join(comidas_preferidas)}")
    print(f"Comidas menos preferidas: {', '.join(comidas_menos_preferidas)}")
    print(f"Sensibilidad: {sensibilidad}")