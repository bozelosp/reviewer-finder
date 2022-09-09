from typing import List
from unittest import result
from pymilvus import connections, CollectionSchema, FieldSchema, DataType, Collection, utility
import time
import pickle
import random
import logging
from tqdm import tqdm

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')
log_template = "=== {:40} ===\n"
search_latency_log_template = "search latency = {:.4f}s"

collection_name = "articles"
if_field_name = "article_id"
vector_field_name = "article_vector"
consistency_level = "Strong"

entities_size = 10000
dims = 700

_host = "ec2-3-122-177-176.eu-central-1.compute.amazonaws.com"
_port = "19530"


def connect_to_milvus(host, port) -> None:
    """ Connect to Milvus server """

    logging.info(log_template.format("start connecting to Milvus"))
    connections.connect(alias="default", host=host, port=port, secure=True, ca_pem_path="C:\\Users\\Volodymyr\\Documents\\ISTA\\AWS\\test-key.pem", server_name="localhost")
    logging.info(log_template.format(str(connections.list_connections())))


def disconnect_from_milvus() -> None:
    """ Disconnect from Milvus server. """
    logging.info(log_template.format("Disconnecting from Milvus"))
    connections.disconnect(alias="default")


def create_collection(name, id_field, vector_field, dim=700, consistency_level="Strong") -> Collection:
    """ Create a collection with the given name and fields. """
    
    logging.info(log_template.format(f"Create collection {name}"))

    id = FieldSchema(name=id_field, dtype=DataType.INT64, is_primary=True)
    vector = FieldSchema(name=vector_field, dtype=DataType.FLOAT_VECTOR, dim=dim)

    schema = CollectionSchema(fields=[id, vector])
    collection = Collection(name=name, schema=schema, consistency_level=consistency_level)

    return collection


def has_collection(name) -> bool:
    """ Check if a collection with the given name exists. """
    
    return utility.has_collection(name)


def drop_collection(name) -> None:
    """ Drop a collection with the given name. """
    
    logging.info(log_template.format(f"Drop collection {name}"))
    utility.drop_collection(name)


def list_collections() -> List:
    """ List all collections. """
    
    return utility.list_collections()


def insert_data(collection, id_data, vector_data) -> None:
    """ Insert data into the given collection. """
    logging.info(log_template.format(f"Insert data of size {len(id_data)} into collection {collection.name}"))
    collection.insert([id_data, vector_data])


def get_entity_num(collection) -> int:
    """ Get the number of entities in a collection. """

    return collection.num_entities


def create_index(collection, field_name, index_params=None) -> None:
    """ Create index for a collection. """
    if not index_params:
        index_params = {
            "index_type": "IVF_SQ8",
            "metric_type": "IP",
            "params": {"nlist": 1024}
        }
    logging.info(log_template.format(f"Create index for collection {collection.name}"))
    collection.create_index(field_name=field_name, index_params=index_params)


def drop_index(collection) -> None:
    """ Drop index for a collection. """
    logging.info(log_template.format(f"Drop index for collection {collection.name}"))
    collection.drop_index()


def load_collection(collection) -> None:
    """ Load collection. """
    logging.info(log_template.format(f"Load collection {collection.name}"))
    collection.load()


def release_collection(collection) -> None:
    """ Release collection. """
    logging.info(log_template.format(f"Release collection {collection.name}"))
    collection.release()


def main():
    # connect to Milvus
    connect_to_milvus(_host, _port)


    # disconnect from Milvus
    disconnect_from_milvus()


if __name__ == "__main__":
    main()