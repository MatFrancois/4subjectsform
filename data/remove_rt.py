# remove path corresponding to rt in paths.txt
# & filter on keywords
import json
import re

import fasttext
import numpy as np
import spacy
from scipy.spatial import distance
from tqdm import tqdm

# prepocessing du text :
# text_tk = [doc.lemma_ for doc in nlp(tweet.get('text')) if not doc.is_stop and not doc.is_punct and not re.match(r'https?://', doc.text)]
ROOT = "/data/pgay/social_computing/twitter/jordy"
models_dir = f'{ROOT}/fastext'
users_informations_dir = f'{ROOT}/users_text_idcom_rt.json'
nlp = spacy.load('fr_core_news_sm')

def isjson(text: str):
    '''check if file is json'''
    return text.endswith('.json')

def preprocessing_text(text):
    '''tokenize text and remove stopwords'''
    return [doc.lemma_ for doc in nlp(text) if not doc.is_stop and not doc.is_punct and not re.match(r'https?://', doc.text)]

def sentence_embedder(tokenized_sent, model):
    """embed sentence with a given list of token (mean of each embedded token)

    Args:
        tokenized_sent (list): tokenized sentence
        model (fasttext.model): model fasttext

    Returns:
        np.array: mean of embeddings of tokens
    """
    return np.mean([model[tk] for tk in tokenized_sent], axis=0) 

def read_data():
    '''read each tweet and extract user informations & scores'''
    paths = np.loadtxt('/home/pgay/programmation/social_computing/collect_tweets/liste_tweet.txt', dtype=str) # lecture de tous les paths de tweets
    paths = list(filter(
        isjson, # on ne garde que les fichiers json
        paths
    ))

    # json contenant l'information sur les clusters
    with open(users_informations_dir, 'r') as f:
        users_informations = json.load(f)

    # récupération des scores de similarité 
    with open('croissance/scores.json', 'r') as f:
        scores = json.load(f)

    return paths, users_informations, scores
    
def is_similar(sent, keywords, models, keywords2=None, threshold=0.2):
    """Return True if sent is similar to keywords and keywords2 or croissance in it

    Args:
        sent (np.array): embedding of sentence
        keywords (list): list of keywords to compare with sent
        keywords2 (list): second list of keywords to compare with sent (optional)
        models (dict): _description_
        threshold (float, optional): similarity description. Defaults to 0.2.

    Returns:
        bool: True if similar False otherwise
    """
    
    if keywords2:
        for model in models.values():
            if (min(drop_0(distance.cosine(sentence_embedder(sent, model), sentence_embedder(keywords, model)))) < threshold \
                and min(drop_0(distance.cosine(sentence_embedder(sent, model), model[keyword]) for keyword in keywords2)) < threshold) \
                or ("croissance" in ' '.join(sent).lower()): # corriger
                    
                return True
    else:
        for model in models.values():
            if (min(drop_0(distance.cosine(sentence_embedder(sent, model), sentence_embedder(keywords, model)))) < threshold) \
                or ("croissance" in ' '.join(sent).lower()):
                    
                return True
    return False

def drop_0(dists):
    '''drop 0 from list of distances to avoid min detection'''
    res = list(filter(
        lambda x: x>0,
        dists
    ))
    return res or [1]


def main(
    keywords=['croissance', 'finance', "économie"], # mot de context croissance
    climat_keywords=['climat', 'environnement', 'nature', 'vert', 'decroissance'], # mot de contexte climatique
    cluster_id_to_comp=['3387', '20'], # communauté de références pour les embeddings par défaut => bonpote / macron
):

    models = {clust_id: fasttext.load_model(f'{models_dir}/{clust_id}.bin') for clust_id in cluster_id_to_comp}
    paths, users_informations, scores = read_data()
    
    filtered_users = {}
    n_sent_valid = 0
    
    
    for path in tqdm(paths):
        with open(path, 'r') as f:
            tweet = json.load(f)
        
        user = tweet['author']['username']
        if user not in users_informations.keys(): # si l'utilisateur ne fait partie d'aucune communauté on ne le prend pas en compte
            continue
        
        if (not re.search('^RT @(.*?):\s', tweet.get('text'))) \
        and (tweet.get('author').get('username') in scores):
            
            tweet_tk = preprocessing_text(tweet.get('text'))
            condition = is_similar(tweet_tk, keywords=keywords, keywords2=climat_keywords, models=models, threshold=0.3)
            
            if condition:
                if user not in filtered_users:
                    filtered_users[user] = {
                        'id': [],
                        'cluster_id': users_informations.get(user).get('cluster'),
                        'score': {
                            'db': scores.get(user).get('db'),
                            'da': scores.get(user).get('da'),    
                        },
                        'desc': tweet['author']['description'],
                        'profil_image_url': tweet['author']['profile_image_url'],
                    }
                    
                filtered_users[user]['id'].append(tweet.get('id'))
                n_sent_valid += 1
                
    print(f'{n_sent_valid} tweets valid')
    # write json
    with open('users_with_cluster.json', 'w') as f:
        json.dump(filtered_users, f)
    
    
if __name__ == "__main__":
    main()
    
