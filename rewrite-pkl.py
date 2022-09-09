import pickle
from tqdm import tqdm

entities_size_1 = 10000

entities_size_2 = 100000


# with open(f'data/query_embeddings.pkl', 'rb') as f:
#     query = pickle.load(f)


# vectors = []
# for vector in query:
#     vectors.append([float(x) for x in vector[0]])

# with open(f'data/query_embeddings_list.pkl', 'wb') as f:
#     pickle.dump(vectors, f)


with open(f'data/article_vector_search_results_{entities_size_1}.pkl', 'rb') as f:
    articles1 = pickle.load(f)

with open(f'data/article_vector_search_results_{entities_size_2}.pkl', 'rb') as f:
    articles2 = pickle.load(f)


for index in range(20):
    count = 0
    for result in articles1[index]:
        if result[1] in [x[1] for x in articles2[index]]:
            count += 1

    print(f"Query number: {index}, similarity: {count} %")

# id_str_list, id_int_list, vector_list = [], [], []
# for id, vector in tqdm(articles.items()):
#     id_str_list.append(id)
#     vector_list.append([float(x) for x in vector[0]])

# print(vector_list[0])

# with open(f'data/article_id_list_{size}.pkl', 'wb') as f:
#     pickle.dump(id_str_list, f)

# with open(f'data/article_vector_list_{size}.pkl', 'wb') as f:
#     pickle.dump(vector_list, f)
