from unittest import result
from pymilvus import connections, CollectionSchema, FieldSchema, DataType, Collection, utility
import time
import pickle
import random
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')
log_template = "=== {:40} ===\n"
search_latency_log_template = "search latency = {:.4f}s"
entities_size = 100000
shards = 2


# Connect to Milvus server
logging.info(log_template.format("start connecting to Milvus"))
connections.connect(alias="default", host='localhost', port='19530')

#drop old collection
logging.info(log_template.format("drop old collection"))
utility.drop_collection("articles")

# Create collection
logging.info(log_template.format(f"Create collection of size {entities_size}"))

article_int_id = FieldSchema(name="article_int_id", dtype=DataType.INT64, is_primary=True, max_length=41)
arcticle_vector = FieldSchema(name="article_vector", dtype=DataType.FLOAT_VECTOR, dim=700)

schema = CollectionSchema(fields=[article_int_id, arcticle_vector], description="test articles search")
articles_collection = Collection(name="articles", schema=schema, shards_num=shards, consistency_level="Strong")
#Eventually

# Insert data
logging.info(log_template.format(f"Insert data of size {entities_size}"))

with open(f'data/article_id_to_emb_dict_{entities_size}.pkl', 'rb') as f:
    articles = pickle.load(f)

article_str_id_list, vector_list = [], []
for id, vector in articles.items():
    article_str_id_list.append(id)
    vector_list.append([float(x) for x in vector[0]])

article_int_id_list = list(range(entities_size))

articles_collection.insert([article_int_id_list, vector_list])

# Create vector index
logging.info(log_template.format(f"Create vector index"))
index_params = {"index_type": "IVF_SQ8", "metric_type": "IP", "params": {"nlist": 1024}}
# IVF_SQ8
articles_collection.create_index(field_name="article_vector", index_params=index_params)

# Load collection
logging.info(log_template.format(f"Load collection"))
articles_collection.load()

# Perform similarity search
logging.info(log_template.format(f"Perform similarity search"))
search_params = {"metric_type": "IP", "params": {"nprobe": 512}}

with open('data/query_embeddings.pkl', 'rb') as f:
    query_vectors = pickle.load(f)

for vector in query_vectors:
    start_time = time.time()
    results = articles_collection.search(
        data = [[float(x) for x in vector[0]]],
        anns_field = "article_vector",
        param = search_params,
        output_fields=["article_int_id"],
        consistency_level="Strong",
        limit=2
        )
    end_time = time.time()
    logging.info(search_latency_log_template.format(end_time - start_time))


# Disconnect from Milvus server
logging.info(log_template.format("disconnecting from Milvus"))
connections.disconnect("default")