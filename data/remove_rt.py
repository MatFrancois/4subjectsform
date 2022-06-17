# remove path corresponding to rt in paths.txt
# & filter on keywords

import numpy as np
import json
import re
from tqdm import tqdm 

def isjson(text: str):
    return text.endswith('.json')

paths = np.loadtxt('paths.txt', dtype=str) # lecture de tous les paths de tweets
paths = list(filter(
    isjson, # on ne garde que les fichiers json
    paths
))

# récupération des scores de similarité 
with open('croissance/scores.json', 'r') as f:
    scores = json.load(f)

no_rt_paths = {}
for path in tqdm(paths):
    with open(path, 'r') as f:
        tweet = json.load(f)
        
    if (not re.search('^RT @(.*?):\s', tweet.get('text'))) \
    and (re.search('croissance', tweet.get('text').lower()) or re.search('finance', tweet.get('text').lower())) \
    and (re.search('climat', tweet.get('text').lower()) or re.search('environnement', tweet.get('text').lower()) or re.search('nature', tweet.get('text').lower()) or re.search('verte', tweet.get('text').lower())) \
    and (tweet.get('author').get('username') in scores): # if not a retweet
        user = tweet['author']['username']
        if user not in no_rt_paths:
            no_rt_paths[user] = {
                'id': [],
                'score': {
                    'db': scores.get(user).get('db'),
                    'da': scores.get(user).get('da'),    
                },
                'desc': tweet['author']['description'],
                'profil_image_url': tweet['author']['profile_image_url'],
            }
        no_rt_paths[user]['id'].append(tweet['id'])
        

with open('filtered_user_and_score.json', 'w') as f:
    json.dump(no_rt_paths, f)