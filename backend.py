from qdrant_client import QdrantClient
from flask import Flask, request, jsonify
import requests
from sentence_transformers import SentenceTransformer

app = Flask(__name__)
from flask_cors import CORS
CORS(app)


EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
model = SentenceTransformer(EMBEDDING_MODEL)

client = QdrantClient(url="https://ff289b1a-44e1-47e1-9725-a7cc62f513b2.europe-west3-0.gcp.cloud.qdrant.io:6333", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.DY9s8r-lX8OI1NBe2cCXa3w-HJk3uOm2lxITtiqe9I0")

def ask_question(question):
    try:
        query_vec = model.encode([question])[0]

        results = client.query_points(
            collection_name="docs",
            query=query_vec,
            limit=3
        ).points

        

        context = "\n".join([r.payload["text"] for r in results])

        response = requests.post(
            "http://127.0.0.1:1234/v1/chat/completions",
            json={
                "model": "phi-2",
                "messages" : [
                 {
                   "role": "system",
                   "content": (
                      "Tu es un assistant RAG STRICT.\n"
                      "Réponds uniquement avec les informations présentes dans le contexte. N'ajoute aucun titre, exercice ou contenu externe.\n"
                      "Tu n'as PAS le droit d'utiliser tes connaissances générales.\n"
                      "Réponds toujours en français.\n"
                      "Si la réponse n'est pas explicitement présente dans le contexte, réponds : "
                      "'Information non trouvée dans les documents.'"

                    )
                 },
                 {
                    "role": "user",
                    "content": f"Réponds en français.\n\nContexte:\n{context}\n\nQuestion: {question}"

                 }
                ]
,
                "temperature": 0.0,
                "top_p": 0.9,
                "max_tokens": 120 ,
                "stop": ["##", "\n\n"]

                


            },
            timeout=180

        )

        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        print("❌ BACKEND ERROR:", e)
        return "Erreur backend, regarde le terminal."


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    answer = ask_question(data["question"])
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(port=5000)