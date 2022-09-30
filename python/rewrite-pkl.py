import pickle
from tqdm import tqdm

# entities_size_1 = 100000
# entities_size_2 = 1000000

# with open(f'data/article_vector_search_results_{entities_size_1}.pkl', 'rb') as f:
#     articles1 = pickle.load(f)

# with open(f'data/article_vector_search_results_{entities_size_2}.pkl', 'rb') as f:
#     articles2 = pickle.load(f)

# precision = 0
# for index in range(20):
#     count = 0
#     for result in articles1[index]:
#         if result[1] in [x[1] for x in articles2[index]]:
#             count += 1
#     precision += count / 20
#     print(f"Query number: {index}, similarity: {count} %")
# print(f"precision: {precision}")


####################### Reformat queries ########################3
# with open(f'data/query_embeddings.pkl', 'rb') as f:
#     query = pickle.load(f)


# vectors = []
# for vector in query:
#     norm = sum([float(x)**2 for x in vector[0]])**0.5
#     vectors.append([float(x) / norm  for x in vector[0]])


# with open(f'data/query_embeddings_list.pkl', 'wb') as f:
#     pickle.dump(vectors, f)



###################### Reformat dicts #################
# entities_size = 1000 * 10

# with open(f'data/article_id_to_emb_dict_{entities_size}.pkl', 'rb') as f:
#     articles = pickle.load(f)

# id_str_list, id_int_list, vector_list = [], [], []

# for str_id, vector in tqdm(articles.items()):
#     id_str_list.append(str_id)
#     norm = sum([float(x)**2 for x in vector[0]])**0.5
#     vector_list.append([float(x) / norm for x in vector[0]])

# print(sum([float(x)**2 for x in vector_list[0]]))

# with open(f'data/article_id_list_{entities_size}.pkl', 'wb') as f:
#     pickle.dump(id_str_list, f)

# with open(f'data/article_vector_list_{entities_size}.pkl', 'wb') as f:
#     pickle.dump(vector_list, f)


###################### Reformat 1 million dicts #################
# entities_size = 1000 * 10
# folder = "entries"
# batch_size = 1000

# with open(f'data/article_id_to_emb_dict_{entities_size}.pkl', 'rb') as f:
#     articles = pickle.load(f)

# id_str_list, id_int_list, vector_list = [], [], []

# counter = 0
# i = 0
# for str_id, vector in tqdm(articles.items()):
#     id_str_list.append(str_id)
#     norm = sum([float(x)**2 for x in vector[0]])**0.5
#     vector_list.append([float(x) / norm for x in vector[0]])
#     counter +=1
#     if counter % batch_size == 0:
#         with open(f'data/{folder}/article_vector_list_{entities_size}_part_{i}.pkl', 'wb') as f:
#             pickle.dump(vector_list, f)
#         i += 1
#         vector_list = []

# if vector_list:
#     with open(f'data/{folder}/article_vector_list_{entities_size}_part_{i}.pkl', 'wb') as f:
#         pickle.dump(vector_list, f)

# with open(f'data/article_id_list_{entities_size}.pkl', 'wb') as f:
#     pickle.dump(id_str_list, f)

