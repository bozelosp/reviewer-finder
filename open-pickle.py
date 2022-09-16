import pickle
with open(f'data/article_vector_list_1000000_part_100.pkl', 'rb') as f:
    data = pickle.load(f)

print(data)