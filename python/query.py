from typing import List
from pymilvus import connections, CollectionSchema, FieldSchema, DataType, Collection, utility
import time
import pickle
import logging
import json

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')
log_template = "=== {:40} ===\n"
search_latency_log_template = "search latency = {:.4f}s"

with open('settings.json') as f:
    settings = json.load(f)

collection_name = settings['collection_name']
if_field_name = settings['if_field_name']
vector_field_name = settings['vector_field_name']
consistency_level = settings['consistency_level']

entities_size = settings['entities_size']
dims = settings['dims']
batch_size = settings['batch_size']

proxy_ip = settings['proxy_ip']
proxy_port = settings['proxy_port']

top_k = 100

search_params = {
    "metric_type": "IP",
    "params": {"nprobe": 100}
    }

with open(f'data/article_id_list_{entities_size}.pkl', 'rb') as f:
    str_id_list = pickle.load(f)

with open('data/query_embeddings_list.pkl', 'rb') as f:
    query_vectors = pickle.load(f)


def connect_to_milvus_remote(host, port) -> None:
    """ Connect to Milvus server """
    logging.info(log_template.format("start connecting to Milvus"))
    connections.connect(alias=f"default", host=host, port=port)
    logging.info(log_template.format(str(connections.list_connections())))


def connect_to_milvus() -> None:
    """ Connect to Milvus server """

    logging.info(log_template.format("start connecting to Milvus"))
    connections.connect(alias="default", host='localhost', port='19530')
    logging.info(log_template.format(str(connections.list_connections())))


def disconnect_from_milvus() -> None:
    """ Disconnect from Milvus server. """
    logging.info(log_template.format("Disconnecting from Milvus"))
    connections.disconnect(alias="default")

def has_collection(name) -> bool:
    """ Check if a collection with the given name exists. """
    
    return utility.has_collection(name)

def list_collections() -> List:
    """ List all collections. """
    
    return utility.list_collections()


def get_str_id(str_id_list, int_id) -> str:
    return str_id_list[int_id]


def search(collection, vector_field, query, top_k=100, consistency="Strong", params=None) -> None:
    """ Search collection. """
    if not params:
        params = {
            "metric_type": "IP",
            "params": {"nprobe": 5} # default value
        }
    logging.info(log_template.format(f"Search in collection {collection.name}"))
    start_time = time.time()
    results = collection.search(
        data = query,
        anns_field = vector_field,
        limit=top_k,
        param=params,
        consistency = consistency
        )
    end_time = time.time()
    logging.info(search_latency_log_template.format(end_time - start_time))
    return results


def process_results(results, str_id_list, top_k=100, log=False) -> None:
    """ Process search results. """
    results_dict = []
    for i, result in enumerate(results):
        results_dict.append([])
        if log:
            logging.info(f"Top {top_k} results for query {i}:")
        for j, hit in enumerate(result):
            distance = hit.distance
            id = get_str_id(str_id_list, hit.id)
            results_dict[i].append([distance, id])
            if log:
                logging.info(f"Rank {j}: {distance}, {id}")
    return results_dict


def main():
    # connect to Milvus
    connect_to_milvus_remote(proxy_ip, proxy_port)

    #show collections
    logging.info(log_template.format(f"Collections on server: {list_collections()}"))

    collection = Collection(name=collection_name, consistency_level=consistency_level)

    # search
    results = search(collection, vector_field_name, query_vectors, top_k, consistency_level, search_params)

    #process results
    results_dict = process_results(results, str_id_list, top_k)

    with open(f'data/article_vector_search_results_{entities_size}.pkl', 'wb') as f:
        pickle.dump(results_dict, f)

    # disconnect from Milvus
    disconnect_from_milvus()


if __name__ == "__main__":
    main()