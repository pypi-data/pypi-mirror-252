import json

from qdrant_client import QdrantClient

from vecutils.qdrant import iter_points

qdrant = QdrantClient("http://129.226.212.197.ipssh.net:36333")


examples = []
for i, points in enumerate(
    iter_points(
        qdrant,
        "similarity_dispatcher_examples",
        with_payload=True,
        with_vectors=True,
        limit=10000,
    ),
):
    examples += [x.model_dump() for x in points]

with open(f"data/points-{i:0>10}.json", mode="w") as f:
    json.dump(examples, f)

questions = [x["payload"]["question"] for x in examples]

with open("data/questions.txt", mode="w") as f:
    f.writelines("\n".join(questions))
