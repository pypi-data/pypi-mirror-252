import argparse
import logging
import os

from qdrant_client import QdrantClient

from vecutils.qdrant import duplicate_collection


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--url", type=str, default=None)
    parser.add_argument("--source", type=str, required=True)
    parser.add_argument("--target", type=str, required=True)
    parser.add_argument("--delete-vectors", type=str, nargs="*")
    parser.add_argument("--add-vectors", type=str, nargs="*")
    parser.add_argument("--indexes", type=str, nargs="*")
    parser.add_argument("--chunk-size", type=int, default=500)

    args = parser.parse_args()  # pylint: disable=redefined-outer-name
    if not args.url:
        args.url = os.getenv("QDRANT_URL")

    add_vectors = {}
    if args.add_vectors:
        for spec in args.add_vectors:
            remaining, distance = spec.rsplit("/", 1)
            name, size = remaining.rsplit("/", 1)
            add_vectors[name] = {
                "size": int(size),
                "distance": distance,
            }
    args.add_vectors = add_vectors

    indexes = []
    if args.indexes:
        for spec in args.indexes:
            name, type_ = spec.split("/")
            indexes += [
                {
                    "field_name": name,
                    "field_type": type_,
                },
            ]
    args.indexes = indexes

    return args


def main():
    args = parse_args()

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.basicConfig(level=logging.INFO, force=True)

    client = QdrantClient(args.url)

    duplicate_collection(
        client,
        args.source,
        args.target,
        delete_vectors=args.delete_vectors,
        add_vectors=args.add_vectors,
        indexes=args.indexes,
        limit=args.chunk_size,
    )


if __name__ == "__main__":
    main()
