import pickle
from turtle import position
from unicodedata import name
from tqdm import tqdm
import matplotlib.pyplot as plt

def compare():
    entities_size_1 = 100000
    entities_size_2 = 10000000

    with open(f'data/article_vector_search_results_{entities_size_1}.pkl', 'rb') as f:
        articles1 = pickle.load(f)

    with open(f'data/article_vector_search_results_{entities_size_2}.pkl', 'rb') as f:
        articles2 = pickle.load(f)

    precision = 0
    distances1, distances2 = [], []
    for index in range(20):
        count = 0
        distances1 = distances1 + [x[0] for x in articles1[index]]
        distances2 = distances2 + [x[0] for x in articles2[index]]
        for result in articles1[index]:
            if result[1] in [x[1] for x in articles2[index]]:
                count += 1
        precision += count / 20
        print(f"Query number: {index}, similarity: {count} %")
    print(f"precision: {precision}")

    fig, axes = plt.subplots(1, 2, figsize=(10, 5), sharey=True)
    
    plt.suptitle('Histogram of distances for all 20 queries', position=(0.5, 0.99))
    axes[0].hist(distances1, rwidth=0.9)
    avg0 = sum(distances1) / len(distances1)
    axes[0].set_title('Results from 100k entities\n average distance: ' + str(round(avg0,3)), fontsize=10)
    axes[0].set_xlabel('Distance')

    axes[1].hist(distances2, rwidth=0.9)
    avg1 = sum(distances2) / len(distances2)
    axes[1].set_title('Results from 10M entities\n average distance: ' + str(round(avg1, 3)), fontsize=10)
    axes[1].set_xlabel('Distance')
    plt.show()

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


def reformat_dicts_chunks():
    ''' Reformat 1 million dicts '''
    entities_size = 1000 * 100
    folder = "entries"
    batch_size = 10000

    with open(f'data/article_id_to_emb_dict_{entities_size}.pkl', 'rb') as f:
        articles = pickle.load(f)

    id_str_list, id_int_list, vector_list = [], [], []

    counter = 0
    i = 0
    for str_id, vector in tqdm(articles.items()):
        id_str_list.append(str_id)
        norm = sum([float(x)**2 for x in vector[0]])**0.5
        vector_list.append([float(x) / norm for x in vector[0]])
        counter +=1
        if counter % batch_size == 0:
            with open(f'data/{folder}/article_vector_list_{entities_size}_part_{i}.pkl', 'wb') as f:
                pickle.dump(vector_list, f)
            i += 1
            vector_list = []

    if vector_list:
        with open(f'data/{folder}/article_vector_list_{entities_size}_part_{i}.pkl', 'wb') as f:
            pickle.dump(vector_list, f)

    with open(f'data/article_id_list_{entities_size}.pkl', 'wb') as f:
        pickle.dump(id_str_list, f)


def reformat_into_chunks():
    ''' Reformat any dixt into lists '''
    folder = "entries"
    batch_size = 25000

    for index in [3, 6, 9]: #range(9,10):
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
    compare()
