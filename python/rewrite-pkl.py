import pickle
from turtle import position
from unicodedata import name
from tqdm import tqdm
import matplotlib.pyplot as plt


def reformat_queries():
    '''Reformat queries'''
    with open(f'data/query_embeddings.pkl', 'rb') as f:
        query = pickle.load(f)


    vectors = []
    for vector in query:
        norm = sum([float(x)**2 for x in vector[0]])**0.5
        vectors.append([float(x) / norm  for x in vector[0]])


    with open(f'data/query_embeddings_list.pkl', 'wb') as f:
        pickle.dump(vectors, f)


def reformat_into_chunks():
    ''' Reformat 10 million entities into chunks of 25000 entities'''
    folder = "entries"
    batch_size = 25000

    for index in range(10):
        number = index * 1000000
        with open(f'data/article_id_to_emb_dict_{number}.pkl', 'rb') as f:
            articles = pickle.load(f)

        id_str_list, vector_list = [], []

        counter = 0
        i = 0
        for str_id, vector in tqdm(articles.items()):
            norm = sum([float(x)**2 for x in vector[0]])**0.5
            try:
                vector_list.append([float(x) / norm for x in vector[0]])
                id_str_list.append(str_id)
            except:
                print(str_id)
                print(vector)
                print(norm)
            counter +=1
            if counter % batch_size == 0:
                with open(f'data/{folder}/article_vector_list_{number}_part_{i}.pkl', 'wb') as f:
                    pickle.dump([id_str_list, vector_list], f)
                i += 1
                vector_list = []
                id_str_list = []

        if vector_list:
            with open(f'data/{folder}/article_vector_list_{number}_part_{i}.pkl', 'wb') as f:
                pickle.dump([id_str_list, vector_list], f)


if __name__ == '__main__':
    reformat_into_chunks()
    reformat_queries()
