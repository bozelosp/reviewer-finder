from random import random
from pymilvus import connections, CollectionSchema, FieldSchema, DataType, Collection, utility
import pickle
import logging
from tqdm import tqdm
import json

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')
log_template = "=== {:40} ===\n"
search_latency_log_template = "search latency = {:.4f}s"

with open('settings.json') as f:
    settings = json.load(f)

collection_name = settings['collection_name']
id_field_name = settings['if_field_name']
vector_field_name = settings['vector_field_name']
consistency_level = settings['consistency_level']

entities_size = settings['entities_size']
dims = settings['dims']
batch_size = settings['batch_size']

proxy_ip = settings['proxy_ip']
proxy_port = settings['proxy_port']

index_params = {
    "index_type": "IVF_SQ8",
    "metric_type": "IP",
    "params": {"nlist": settings['nlist']}
}


def connect_to_milvus() -> None:
    """ Connect to Milvus server """

    logging.info(log_template.format("start connecting to Milvus"))
    connections.connect(alias="default", host='localhost', port='19530')
    logging.info(log_template.format(str(connections.list_connections())))


def connect_to_milvus_remote(host, port) -> None:
    """ Connect to Milvus server """
    logging.info(log_template.format("start connecting to Milvus"))
    connections.connect(alias=f"default", host=host, port=port)
    logging.info(log_template.format(str(connections.list_connections())))


def disconnect_from_milvus() -> None:
    """ Disconnect from Milvus server. """
    logging.info(log_template.format("Disconnecting from Milvus"))
    connections.disconnect(alias="default")


def list_collections() -> list:
    """ List all collections. """
    
    return utility.list_collections()


def insert_data(collection, id_data, vector_data, log=False) -> None:
    """ Insert data into the given collection. """
    if log:
        logging.info(log_template.format(f"Insert data of size {len(id_data)} into collection {collection.name}"))
    collection.insert([id_data, vector_data])


def get_entity_num(collection) -> int:
    """ Get the number of entities in a collection. """

    return collection.num_entities


def main():
    # connect to Milvus
    connect_to_milvus_remote(proxy_ip, proxy_port)

    collection = Collection(name=collection_name, consistency_level=consistency_level)

    # open data
    filenames = ["data/entries/article_vector_list_9000000_part_11.pkl",
                 "data/entries/article_vector_list_6000000_part_14.pkl",
                 "data/entries/article_vector_list_3000000_part_34.pkl",]
    for filename in filenames:
        with open(filename, 'rb') as f:
            vector_data = pickle.load(f)
        try:
            insert_data(collection, vector_data[0], vector_data[1])
            logging.info(log_template.format(f"Inserted batch"))
        except:
            logging.info(log_template.format(f"Errored inserting file {filename}"))


    # get entity num
    logging.info(log_template.format(f"Entity num: {get_entity_num(collection)}"))

    # disconnect from Milvus
    disconnect_from_milvus()

if __name__ == "__main__":
    main()