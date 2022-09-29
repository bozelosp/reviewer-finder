from pymilvus import connections, CollectionSchema, FieldSchema, DataType, Collection, utility
import time
import pickle
import random
import logging
from tqdm import tqdm

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')
log_template = "=== {:40} ===\n"
search_latency_log_template = "search latency = {:.4f}s"

collection_name = "articles_1mil"
if_field_name = "article_id"
vector_field_name = "article_vector"
consistency_level = "Strong"

entities_size = 1000 * 1000
dims = 700
filename = "data/1million/article_vector_list_1000000"
batch_size = 10 * 1000

index_params = {
    "index_type": "IVF_SQ8",
    "metric_type": "IP",
    "params": {"nlist": 1000}
}


def connect_to_milvus() -> None:
    """ Connect to Milvus server """

    logging.info(log_template.format("start connecting to Milvus"))
    connections.connect(alias="default", host='localhost', port='19530')
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


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield list(range(i, i+n)), l[i: i+n]

def main():
    # connect to Milvus
    connect_to_milvus()

    if has_collection(collection_name):
        drop_collection(collection_name)

    # create collection
    collection = create_collection(collection_name, if_field_name, vector_field_name, dims, consistency_level=consistency_level)

    #show collections
    logging.info(log_template.format(f"Collections on server: {list_collections()}"))

    # create index
    create_index(collection, vector_field_name, index_params)

    # open data
    counter = 0

    for counter in tqdm(range(round(entities_size / batch_size))):

            with open(f'{filename}_part_{counter}.pkl', 'rb') as f:
                vector_list = pickle.load(f)
            
            ids = list(range(counter * batch_size, (counter + 1) * batch_size))
            insert_data(collection, ids, vector_list)

    logging.info(log_template.format(f"Inserted {counter+1} batches"))
            
    # with open(f'data/article_vector_list_{entities_size}.pkl', 'rb') as f:
    #            vector_list = pickle.load(f)

    # # #insert data
    # for ids, vectors in tqdm(divide_chunks(vector_list, 1000)):
    #     insert_data(collection, ids, vectors)

    # get entity num
    logging.info(log_template.format(f"Entity num: {get_entity_num(collection)}"))

    # load collection
    load_collection(collection)

    # disconnect from Milvus
    disconnect_from_milvus()

if __name__ == "__main__":
    main()