from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import nltk
import joblib

# Descargamos los stopwords que necesitaremos luego
nltk.download('stopwords')
from nltk.corpus import stopwords

# Obtenemos las stopwords para español
spanish_stop_words = stopwords.words('spanish')
labels = [(1, "receta"), (2, "restaurante")]
dataset = []

# Textos de "recetas de comida"
dataset_recetas = [
    (1, "Me encantaría probar una receta de pasta al pesto."),
    (1, "¿Tienes alguna receta fácil y deliciosa de pollo asado?"),
    (1, "Estoy buscando una receta de ensalada fresca y nutritiva."),
    (1, "¿Puedes recomendarme una receta de postre con chocolate?"),
    (1, "Me gustaría cocinar algo diferente con salmón. ¿Tienes alguna receta?"),
    (1, "Necesito una receta vegetariana para sorprender a mis amigos."),
    (1, "¿Cuál es tu receta favorita de tacos?"),
    (1, "Quiero aprender a hacer sushi en casa. ¿Tienes una receta simple?"),
    (1, "¿Conoces alguna receta tradicional de tu país que sea fácil de preparar?"),
    (1, "Estoy buscando una receta de smoothie saludable para el desayuno."),
    (1, "¿Tienes alguna receta especial de pasta con mariscos?"),
    (1, "Me gustaría probar una receta auténtica de curry. ¿Puedes recomendarme alguna?"),
    (1, "¿Cuál es tu receta preferida de pizza casera?"),
    (1, "Estoy buscando recetas de platos típicos de diferentes regiones del mundo."),
    (1, "¿Tienes alguna receta de cocina rápida para días ocupados?")
]

dataset_restaurantes = [
    (2, "¿Conoces algún buen restaurante de sushi cerca de aquí?"),
    (2, "Estoy buscando un lugar para cenar con amigos. ¿Alguna recomendación de restaurante?"),
    (2, "¿Cuál es el mejor restaurante de comida italiana en esta zona?"),
    (2, "Necesito encontrar un restaurante con opciones vegetarianas para una cena especial."),
    (2, "¿Puedes sugerirme un restaurante con terraza para disfrutar del buen clima?"),
    (2, "Estoy antojado de comida mexicana. ¿Conoces algún restaurante auténtico?"),
    (2, "¿Hay algún restaurante de comida rápida cercano que recomiendes?"),
    (2, "Quiero probar algo nuevo. ¿Algún restaurante con cocina asiática que sea bueno?"),
    (2, "¿Cuáles son los mejores restaurantes de mariscos en esta área?"),
    (2, "Estoy buscando un lugar acogedor para un almuerzo tranquilo. ¿Algún restaurante así?"),
    (2, "¿Conoces algún restaurante con opciones veganas y sin gluten?"),
    (2, "Quiero llevar a mi familia a un buen restaurante para celebrar una ocasión especial."),
    (2, "¿Hay algún restaurante de comida local que deba probar durante mi visita?"),
    (2, "Necesito encontrar un buen restaurante para un desayuno abundante. ¿Algún lugar recomendado?"),
    (2, "¿Cuál es tu restaurante favorito en esta área?")
]

dataset = dataset_recetas + dataset_restaurantes

# Preparar X e y
X = [text.lower() for label, text in dataset]
y = [label for label, text in dataset]
# División del dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Vectorización de los textos con eliminación de palabras vacías
vectorizer = TfidfVectorizer(stop_words=spanish_stop_words)
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)
# Creación y entrenamiento del modelo de Regresión Logística con multinomial
modelo_LR = LogisticRegression(max_iter=1000, multi_class='multinomial', solver='lbfgs')
modelo_LR.fit(X_train_vectorized, y_train)

# Supongamos que 'modelo_LR' es tu modelo entrenado
modelo_LR.fit(X_train_vectorized, y_train)

# Guardar el modelo en un archivo
joblib.dump(modelo_LR, 'clasificador.pkl')