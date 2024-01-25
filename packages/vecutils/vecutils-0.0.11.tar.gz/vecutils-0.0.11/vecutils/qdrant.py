import copy
import logging
import uuid
from collections.abc import Awaitable, Callable, Iterable

import tqdm
from qdrant_client import AsyncQdrantClient, QdrantClient, models
from qdrant_client.http.models import PointStruct

from vecutils import batch_create_embeddings
from vecutils.utils import chunk

logger = logging.getLogger(__name__)


def to_dict(x):
    if x is None:
        return {}

    return x.model_dump()


def duplicate_collection(  # noqa: PLR0913
    client: QdrantClient,
    source_colleciton: str,
    target_collection: str,
    delete_vectors: list[str] | None = None,
    add_vectors: dict | None = None,
    indexes: list[dict] | None = None,
    limit: int = 1000,
    timeout: int | None = None,
):
    collection_info = client.get_collection(source_colleciton)
    config = collection_info.config
    logger.info(
        "Duplicating, source: %s, target: %s, vectors_count: %d",
        source_colleciton,
        target_collection,
        collection_info.vectors_count,
    )

    # Update vectors config
    vectors_config = config.params.vectors
    if isinstance(vectors_config, models.VectorParams):
        msg = "Only multi-vector collection is supported"
        raise TypeError(msg)

    if delete_vectors:
        kept_vectors_config = {
            k: v for k, v in vectors_config.items() if k not in delete_vectors
        }
    else:
        kept_vectors_config = vectors_config

    if add_vectors:
        vectors_config = kept_vectors_config | add_vectors

    # Create new collection
    logger.info(
        "Creating collection, name: %s, vectors: %s",
        target_collection,
        list(vectors_config),
    )
    client.create_collection(
        collection_name=target_collection,
        vectors_config=vectors_config,
        shard_number=config.params.shard_number,
        replication_factor=config.params.replication_factor,
        write_consistency_factor=config.params.write_consistency_factor,
        on_disk_payload=config.params.on_disk_payload,
        hnsw_config=to_dict(config.hnsw_config),
        optimizers_config=to_dict(config.optimizer_config),
        wal_config=to_dict(config.wal_config),
        quantization_config=config.quantization_config,
        timeout=timeout,
    )

    # Update payload index
    if indexes:
        indexes = copy.deepcopy(indexes)
        for key, value in collection_info.payload_schema.items():
            indexes += [
                {
                    "field_name": key,
                    "field_type": value.data_type.value,
                },
            ]
        for index in indexes:
            logger.info(
                "Creating payload index, name: %s, schema: %s",
                index["field_name"],
                index["field_type"],
            )
            client.create_payload_index(target_collection, **index)

    # Upserting points
    batches = iter_points(
        client,
        source_colleciton,
        limit=limit,
        with_payload=True,
        with_vectors=list(kept_vectors_config),
    )
    progress_bar = tqdm.tqdm(
        batches,
        total=collection_info.points_count,
        desc="Upserting points",
        leave=False,
    )
    for batch in progress_bar:
        points = [
            models.PointStruct(id=x.id, payload=x.payload, vector=x.vector)
            for x in batch
        ]

        client.upsert(collection_name=target_collection, points=points)
        progress_bar.update(len(points))
    progress_bar.close()


def iter_points(qdrant: QdrantClient, index: str, **kwargs) -> Iterable:
    kwargs.pop("offset", None)
    offset = None

    while True:
        records, offset = qdrant.scroll(collection_name=index, offset=offset, **kwargs)
        yield records

        if not offset:
            break


def get_existed_point_ids(
    qdrant: QdrantClient,
    index: str,
    id_field: str = "id",
    limit: int = 10000,
) -> set[str | int]:
    iterator = iter_points(
        qdrant,
        index,
        limit=limit,
        with_payload=True,
        with_vectors=False,
    )

    return {x.payload[id_field] for batch in iterator for x in batch}


async def index_vectors(
    client: AsyncQdrantClient,
    index: str,
    docs: list[dict],
    embeddings: list[list[float]],
    vector: str | None = None,
) -> None:
    def _get_vector(embedding):
        if not vector:
            return embedding

        return {
            vector: embedding,
        }

    if len(docs) != len(embeddings):
        msg = "mismatched lengths of documents and embeddings: %d != %d"
        raise ValueError(msg, len(docs), len(embeddings))

    points = [
        PointStruct(
            id=uuid.uuid4().hex,
            vector=_get_vector(embedding),
            payload=doc,
        )
        for embedding, doc in zip(embeddings, docs, strict=True)
    ]
    await client.upsert(collection_name=index, wait=True, points=points)


async def batch_index_vectors(  # noqa: PLR0913
    client: AsyncQdrantClient,
    index: tuple[str, str],
    docs: list[dict],
    embedding_fn: Callable[[list[str]], Awaitable[list[list[float]]]],
    format_fn: Callable[[dict], str],
    index_chunk_size: int = 256,
    embedding_batch_size: int = 16,
    embedding_concurrency: int = 10,
) -> None:
    index_name, vector_name = index

    for batch in chunk(docs, size=index_chunk_size):
        batch_texts = list(map(format_fn, batch))
        batch_embeddings = await batch_create_embeddings(
            batch_texts,
            embedding_fn=embedding_fn,
            batch_size=embedding_batch_size,
            concurrency=embedding_concurrency,
        )
        if len(batch_embeddings) != len(batch):
            logger.warning(
                "%d / %d docs failed to create embeddings",
                len(batch) - len(batch_embeddings),
                len(batch),
            )

        if not batch_embeddings:
            continue

        indices, embeddings = zip(*batch_embeddings, strict=True)
        filtered_batch = [batch[i] for i in indices]

        logger.info("update %d embeddings to qdrant", len(indices))
        await index_vectors(client, index_name, filtered_batch, embeddings, vector_name)
