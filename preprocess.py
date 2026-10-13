from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import os

# 1 Paramètres
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
VECTOR_SIZE = 384  # dépend du modèle
CHUNK_SIZE = 500

# 2 Initialiser l'embedding et Qdrant
model = SentenceTransformer(EMBEDDING_MODEL)
client = QdrantClient(url="https://ff289b1a-44e1-47e1-9725-a7cc62f513b2.europe-west3-0.gcp.cloud.qdrant.io:6333", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.DY9s8r-lX8OI1NBe2cCXa3w-HJk3uOm2lxITtiqe9I0")

# 3 Chunking simple
def chunk_text(text, size=CHUNK_SIZE):
    return [text[i:i+size] for i in range(0, len(text), size)]

# 4 Lire tous les fichiers et préparer les points
points = []
id_counter = 0

for filename in os.listdir('data'):
    if filename.endswith('.txt'):
        text = open(os.path.join('data', filename), 'r', encoding='utf-8').read()
        chunks = chunk_text(text)
        embeddings = model.encode(chunks)
        for i, chunk in enumerate(chunks):
            points.append(PointStruct(id=id_counter, vector=embeddings[i], payload={"text": chunk}))
            id_counter += 1

# 5 Créer / mettre à jour la collection
from qdrant_client.http.models import VectorParams, Distance

client.recreate_collection(
    collection_name="docs",
    vectors_config=VectorParams(
        size=VECTOR_SIZE,
        distance=Distance.COSINE
    )
)

client.upsert(collection_name="docs", points=points)

print(" Tous les fichiers ont été chunkés, embeddings générés et uploadés dans Qdrant !")
