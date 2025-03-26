import weaviate
from weaviate.classes.config import Configure, Property, DataType, VectorDistances
from weaviate.embedded import EmbeddedOptions
from typing import Any, Dict, List


class WeaviateClient:

    def __init__(self, store_path: str):

        self.client = weaviate.connect_to_embedded(
            version="1.28.0",
            persistence_data_path=store_path
        )

    def create_collection(self, collection_name: str, vector_name: str) -> None:

        self.client.connect()

        self.client.collections.create(
            collection_name,
            vectorizer_config=[
                Configure.NamedVectors.none(name=vector_name)
            ],
            properties=[
                Property(name="title", data_type=DataType.TEXT),
                Property(name="id", data_type=DataType.TEXT),
            ],
            vector_index_config=Configure.VectorIndex.hnsw(
                distance_metric=VectorDistances.COSINE
            )
        )

        self.client.close()

    def populate_collection(self, collection_name: str, data: List[Dict[str, Any]]) -> None:

        self.client.connect()
        print("Starting populating Weaviate...")

        collection = self.client.collections.get(collection_name)
        for d in data:
            print(f"Inserting {d} into collection {collection_name}...")
            collection.data.insert(
                properties={
                    "id": d["id"],
                    "title": d["title"],
                },
                vector=d["vector"]
            )     
            print(f"{d} inserted!")  

        print("Finished populating Weaviate!")
        self.client.close()