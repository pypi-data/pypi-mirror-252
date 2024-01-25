import uuid

from qdrant_client import QdrantClient

from vecutils.qdrant import index_vectors, iter_points
from vecutils.utils import chunk

qd = QdrantClient("http://localhost:6333")

points = iter_points(qd, "text2", limit=1000, with_payload=True, with_vectors=True)

for batch in chunk((points), 1000):
    batch = list(batch)
    print(batch[0])
    embeddings = [x.vector["text-embedding-ada-002"] for x in batch]
    docs = [x.payload for x in batch]
    for doc in docs:
        doc["id"] = uuid.uuid4().hex
    index_vectors(qd, "text3", docs, embeddings, vector="text-embedding-ada-002")
