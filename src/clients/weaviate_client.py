import weaviate
from weaviate.classes.config import Configure, Property, DataType, VectorDistances
from weaviate.classes.init import AdditionalConfig, Timeout
from typing import Any, Dict, List
from dotenv import load_dotenv
import os

load_dotenv()


class WeaviateClient:

    def __init__(self):

        self.client = weaviate.connect_to_local(
            host="localhost",
            port=os.getenv("WEAVIATE_HTTP_PORT"),
            grpc_port=os.getenv("WEAVIATE_GRPC_PORT"),
            additional_config=AdditionalConfig(
                timeout=Timeout(init=30, query=60, insert=120)
            )
        )

    def create_collection(self, collection_name: str, vector_name: str) -> None:

        self.client.connect()

        self.client.collections.create(
            collection_name,
            vectorizer_config=[
                Configure.NamedVectors.none(
                    name=vector_name,
                    vector_index_config=Configure.VectorIndex.hnsw(distance_metric=VectorDistances.COSINE)
                )
            ],
            properties=[
                Property(name="title", data_type=DataType.TEXT),
                Property(name="track_id", data_type=DataType.TEXT),
                Property(name="jazzy", data_type=DataType.INT),
            ]
        )

        self.client.close()

    def populate_collection(self, collection_name: str, jazzy: bool, data: List[Dict[str, Any]]) -> None:

        self.client.connect()
        print("Starting populating Weaviate...")

        collection = self.client.collections.get(collection_name)
        for d in data:
            if jazzy:
                print(f"Inserting jazzy song {d} into collection {collection_name}...")
                collection.data.insert(
                    properties={
                        "track_id": d["id"],
                        "title": d["title"],
                        "jazzy": 1
                    },
                    vector=d["vector"]
                )     
                print(f"{d} inserted!")  
            else:
                print(f"Inserting jazzy song {d} into collection {collection_name}...")
                collection.data.insert(
                    properties={
                        "track_id": d["id"],
                        "title": d["title"],
                        "jazzy": 0
                    },
                    vector=d["vector"]
                )     
                print(f"{d} inserted!") 
        print("Finished populating Weaviate!")
        self.client.close()