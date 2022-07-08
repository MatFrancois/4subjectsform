# script to filter tweet corpus on some keywords
from psutil import users
import fasttext
import os 
import json

ROOT = "/data/pgay/social_computing/twitter/jordy"
models_dir = f'{ROOT}/fastext'
users_informations_dir = f'{ROOT}/users_text_idcom_rt.json'

models = list(filter(lambda x: x.endswith('.bin'), os.listdir(models_dir)))

with open(users_informations_dir, 'r') as f:
    users_informations = json.load(f)

def get_community_users(users_informations, id):
    """filter users_informations on community

    Args:
        users_informations (dict): users_informations
        id (str): community id
    """
    users_informations = dict(filter(
        lambda x: x[1].get('cluster') == id, users_informations.items()
    ))
    
    

def embedding(sentence, model):
    sentence_vector = []
    punctuations = list(string.punctuation)
    sentence_bis = [i for i in word_tokenize(sentence) if i not in punctuations]
    for word in sentence_bis:
        sentence_vector.append(model[word])
    if len(sentence_vector) == 0:
        print('WARNING zero length vector to mean in embedding()')
    res = np.mean(np.array(sentence_vector), axis=0)
    return res

model = fasttext.load_model('../models/model.bin')

