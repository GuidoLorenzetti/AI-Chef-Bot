import os
import pandas as pd

tabular_data_directory = os.path.join("tabular_data")

# Obtén la lista de archivos en la carpeta
archivos = os.listdir(tabular_data_directory)

# Verifica si hay archivos en la carpeta
if archivos:
    # Toma el primer archivo de la lista
    primer_archivo = archivos[0]
    
    # Forma la ruta completa del archivo
    archivo_path = os.path.join(tabular_data_directory, primer_archivo)

    # Lee el DataFrame desde el archivo
    df = pd.read_csv(archivo_path)
primeros_5 = df.head(5)
resultados=[]
# Generar el resultado escrito
resultado_escrito = ""
for index, restaurante in primeros_5.iterrows():
    resultado_escrito += f"Restaurante: {restaurante['name']}\n"
    resultado_escrito += f"Enlace: {restaurante['link']}\n"
    resultado_escrito += f"Calificación: {restaurante['rating']}\n"
    resultado_escrito += f"Dirección: {restaurante['address']}\n\n"
    resultados.append(resultado_escrito)
print(resultado_escrito)