
# script to filter user_with_cluster.json on keyword cosin dstance to tweets 
import json
import os

import fasttext
import numpy as np
from scipy.spatial import distance
from tqdm import tqdm
import pandas as pd
# suppress warning at loading fasttext model
fasttext.FastText.eprint = lambda x: None

cluster_id_to_comp = ['3387', '20']
ROOT = "/data/pgay/social_computing/twitter/jordy"
models_dir = f'{ROOT}/fastext'
# seuil = 0.6
models_name = list(filter(lambda x: x.endswith('.bin'), os.listdir(models_dir)))

keywords = ['croissance', 'finance', "économie"]
climat_keywords = ['climat', 'environnement', 'nature', 'vert', 'decroissance']
# à tester avec une phrase telle que "Nous devons décroitre pour respecter limiter notre impact sur la planète"

def read_data():
    with open('users_with_cluster.json', 'r') as f:
        return json.load(f)

def sentence_embedder(tokenized_sent, model):
    return np.mean([model[tk] for tk in tokenized_sent], axis=0) 

# def is_similar(embedded_sent, keywords, model, threshold=0.2):
#     dist = min(distance.cosine(embedded_sent, model[keyword]) for keyword in keywords)
#     # if dist < threshold:
#     return dist
    # return 0

def drop_0(dists):
    res = list(filter(
        lambda x: x>0,
        dists
    ))
    return res or [1]

def is_similar(sent, keywords, keywords2, models, threshold=0.2):
    if keywords2:
        for model in models.values():
            if (min(drop_0(distance.cosine(sentence_embedder(sent, model), model[keyword]) for keyword in keywords)) < threshold and min(drop_0(distance.cosine(sentence_embedder(sent, model), model[keyword]) for keyword in keywords2)) < threshold) or ("croissance" in ' '.join(sent).lower()):
                return True
    else:
        for model in models.values():
            if (min(drop_0(distance.cosine(sentence_embedder(sent, model), model[keyword]) for keyword in keywords)) < threshold) or ("croissance" in ' '.join(sent).lower()):
                return True
    return False

def main():
    print('begin')
    users_with_cluster = read_data()

    models = {clust_id: fasttext.load_model(f'{models_dir}/{clust_id}.bin') for clust_id in cluster_id_to_comp}

    id_list = []
    for _, user_att in tqdm(users_with_cluster.items()):
        id_list.extend(tweet_id for tweet_id, tweet_tk in zip(user_att.get('id'), user_att.get('text_tk')) if is_similar(tweet_tk, keywords=keywords, keywords2=climat_keywords, models=models, threshold=0.3))

    print(
        f'''
        Done
====================
len: {len(id_list)}
        
saving...
        ''')

    np.savetxt('id_list.txt', id_list, fmt='%s')
    
if __name__ == "__main__":
    main()



