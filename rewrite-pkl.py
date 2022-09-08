import pickle
from tqdm import tqdm

size = 10000


# with open(f'data/query_embeddings.pkl', 'rb') as f:
#     query = pickle.load(f)


# vectors = []
# for vector in query:
#     vectors.append([float(x) for x in vector[0]])

# with open(f'data/query_embeddings_list.pkl', 'wb') as f:
#     pickle.dump(vectors, f)


with open(f'data/article_id_to_emb_dict_{size}.pkl', 'rb') as f:
    articles = pickle.load(f)

id_str_list, id_int_list, vector_list = [], [], []
for id, vector in tqdm(articles.items()):
    id_str_list.append(id)
    vector_list.append([float(x) for x in vector[0]])

print(vector_list[0])

# with open(f'data/article_id_list_{size}.pkl', 'wb') as f:
#     pickle.dump(id_str_list, f)

# with open(f'data/article_vector_list_{size}.pkl', 'wb') as f:
#     pickle.dump(vector_list, f)
