# script to filter user_with_cluster.json on keyword cosin dstance to tweets 
import json
import os

import fasttext
import numpy as np
from scipy.spatial import distance
from tqdm import tqdm

# suppress warning at loading fasttext model
fasttext.FastText.eprint = lambda x: None

ROOT = "/data/pgay/social_computing/twitter/jordy"
models_dir = f'{ROOT}/fastext'
seuil = 0.1
models_name = list(filter(lambda x: x.endswith('.bin'), os.listdir(models_dir)))

keywords = ['croissance', 'finance', "économie"]
climat_keywords = ['climat', 'environnement', 'nature', 'vert', 'decroissance']
# à tester avec une phrase telle que "Nous devons décroitre pour respecter limiter notre impact sur la planète"

def read_data():
    with open('users_with_cluster.json', 'r') as f:
        return json.load(f)

def sentence_embedder(tokenized_sent, model):
    return np.mean([model[tk] for tk in tokenized_sent], axis=0) 

def is_similar(embedded_sent, keywords, model, threshold=0.2):
    for keyword in keywords:
        # print(distance.cosine(embedded_sent, model[keyword]))
        if distance.cosine(embedded_sent, model[keyword]) < threshold:
            return True
    return False

def main():
    print('begin')
    users_with_cluster = read_data()
    for name in tqdm(models_name):
        id_cluster = name.split('.')[0]
        # print(id_cluster, type(id_cluster))
        # print(users_with_cluster[list(users_with_cluster.keys())[0]].get('cluster_id'))
        # filter on id cluster
        users_in_cluster = dict(filter(
            lambda x: x[1].get('cluster_id') == int(id_cluster),
            users_with_cluster.items()
        ))
        model = fasttext.load_model(f'{models_dir}/{name}')
        id_tweets_to_keep = []
        text_tweets_to_keep = []
        for user, user_att in tqdm(users_in_cluster.items()):
            # print(user)
            for id_tweet, text_tk in zip(user_att.get('id'), user_att.get('text_tk')):
                
                # moyenne des plongements d'une phrase
                embedded_sent = sentence_embedder(text_tk, model)
                # print(distance.cosine(embedded_sent, model['croissance']))
                if is_similar(embedded_sent=embedded_sent, keywords=keywords, model=model, threshold=seuil) and is_similar(embedded_sent=embedded_sent, keywords=climat_keywords, model=model, threshold=seuil):
                    id_tweets_to_keep.append(id_tweet)
                    text_tweets_to_keep.append(text_tk)

    print(f'longueur de id_tweets_to_keep   :  {len(id_tweets_to_keep):,}')
    print(f'longueur de text_tweets_to_keep :  {len(text_tweets_to_keep):,}')

    np.savetxt(f'{seuil}_id_tweets_to_keep.txt', id_tweets_to_keep, fmt='%s')
    np.savetxt(f'{seuil}_text_tweets_to_keep.txt', text_tweets_to_keep, fmt='%s')

        
    
if __name__ == "__main__":
    main()



