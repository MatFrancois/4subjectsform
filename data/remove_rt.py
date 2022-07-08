# remove path corresponding to rt in paths.txt
# & filter on keywords
import spacy
import numpy as np
import json
import re
from tqdm import tqdm 


# prepocessing du text :
# text_tk = [doc.lemma_ for doc in nlp(tweet.get('text')) if not doc.is_stop and not doc.is_punct and not re.match(r'https?://', doc.text)]
ROOT = "/data/pgay/social_computing/twitter/jordy"
models_dir = f'{ROOT}/fastext'
users_informations_dir = f'{ROOT}/users_text_idcom_rt.json'
nlp = spacy.load('fr_core_news_sm')

def isjson(text: str):
    return text.endswith('.json')

def preprocessing_text(text):
    return [doc.lemma_ for doc in nlp(text) if not doc.is_stop and not doc.is_punct and not re.match(r'https?://', doc.text)]

def read_data():
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
    
    
def main():
    
    paths, users_informations, scores = read_data()
    
    no_rt_paths = {}
    for path in tqdm(paths):
        with open(path, 'r') as f:
            tweet = json.load(f)
        
        user = tweet['author']['username']
        if user not in users_informations.keys(): # si l'utilisateur ne fait partie d'aucune communauté on ne le prend pas en compte
            continue
        
        
        if (not re.search('^RT @(.*?):\s', tweet.get('text'))) \
        and (tweet.get('author').get('username') in scores): # if not a retweet
        # and (re.search('croissance', tweet.get('text').lower()) or re.search('finance', tweet.get('text').lower())) \
        # and (re.search('climat', tweet.get('text').lower()) or re.search('environnement', tweet.get('text').lower()) or re.search('nature', tweet.get('text').lower()) or re.search('verte', tweet.get('text').lower())) \
            if user not in no_rt_paths:
                no_rt_paths[user] = {
                    'id': [],
                    'cluster_id': users_informations.get(user).get('cluster'),
                    'text_tk': [],
                    'text_root': [],
                    'score': {
                        'db': scores.get(user).get('db'),
                        'da': scores.get(user).get('da'),    
                    },
                    'desc': tweet['author']['description'],
                    'profil_image_url': tweet['author']['profile_image_url'],
                }
                
                
            no_rt_paths[user]['id'].append(tweet.get('id'))
            no_rt_paths[user]['text_tk'].append(preprocessing_text(tweet.get('text')))
            no_rt_paths[user]['text_root'].append(tweet.get('text'))
            
    # write json
    with open('users_with_cluster.json', 'w') as f:
        json.dump(no_rt_paths, f)
    
    
if __name__ == "__main__":
    main()
    
