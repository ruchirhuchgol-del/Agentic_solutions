
import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# --- Configuration ---
KNOWLEDGE_BASE_DIR = "knowledge_base"
COLLECTION_NAME = "statistical_knowledge"
EMBEDDING_MODEL = "all-MiniLM-L6-v2" # A good, lightweight model

# --- Initialization ---
client = QdrantClient(url="http://localhost:6333")
encoder = SentenceTransformer(EMBEDDING_MODEL)

# --- Create Collection ---
if client.collection_exists(COLLECTION_NAME):
    print(f"Collection '{COLLECTION_NAME}' already exists. Deleting it.")
    client.delete_collection(COLLECTION_NAME)

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=encoder.get_sentence_embedding_dimension(), distance=Distance.COSINE),
)
print(f"Collection '{COLLECTION_NAME}' created.")

# --- Ingest Documents ---
points = []
point_id = 0

for root, _, files in os.walk(KNOWLEDGE_BASE_DIR):
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Simple chunking by paragraph
            chunks = text.split('\n\n')
            for chunk in chunks:
                if len(chunk.strip()) > 50: # Ignore small chunks
                    vector = encoder.encode(chunk).tolist()
                    points.append(PointStruct(id=point_id, vector=vector, payload={"text": chunk, "source": file}))
                    point_id += 1

# --- Upload to Qdrant ---
client.upsert(collection_name=COLLECTION_NAME, points=points)
print(f"Successfully ingested {len(points)} chunks into '{COLLECTION_NAME}'.")