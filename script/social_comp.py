import json, os, re
import networkx as nx
import networkx.algorithms.community as nx_comm
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import spacy
import unidecode
import pandas as pd
import numpy as np
from tqdm import tqdm
from gensim.models import Word2Vec
from gensim.models.phrases import Phraser, Phrases
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import scipy
import collections
import contextlib
from pprint import pprint
import spacy
'''
- lecture de tous les tweets
- PAS DE RELATION JAIME PRISE EN COMPTE
'''


ROOT='/data/datasets/elyzee_2022'
WRITE_RELATION = True


stop_words =set(stopwords.words('french'))
tk = TweetTokenizer()
nlp = spacy.load('fr_core_news_sm')
keywords = ['climat', 'énergie', 'nature']
ROOT='/data/datasets/elyzee_2022/' 


def list_files(path):
    """get all files in path & subdirectories

    Args:
        path (str): path

    Returns:
        list: path files list
    """
    files = []
    for element in os.listdir(path):
        if os.path.isdir(f'{path}/{element}'):
            files.extend(iter(list_files(f'{path}/{element}')))
            continue
        files.append(f'{path}/{element}')
    return files

def extract_relation_mentions_hashtags(file_list_tweets, restrict_to=None, extract_text=False, prepro=True):
    """
    Input : 
        list_tweets : a filename where each line is a json path containing a tweet
        restrict_to : A list of tweeter usernames -> only read the tweets from these authors;
        extract_text: if True, will build a dictionnary where the keys is the username and value is a list of tweet texts
    Output :
        hashtags : 
        relations, authors, cited
    """
    authors = {}
    cited = set()
    hashtags = {}
    relations = []
    texts = {}

    list_tweets = list(open(file_list_tweets))
    for json_file in tqdm(list_tweets):
        json_file = json_file.replace('\n','')
        author = '_'.join(os.path.basename(json_file).split('_')[:-1])
        if restrict_to is not None and author not in restrict_to:
            continue
        j = json.load(open(json_file))
        tid = j['id']
        if extract_text:
            text = j['text']
            if prepro:
                text = [doc.lemma_ for doc in nlp(text) if not doc.is_stop and not doc.is_punct and not re.match(r'https?://', doc.text)]
            if author not in texts:
                texts[author] = []
            texts[author].append(text)
        if 'in_reply_to_user_id' in j:
            relations.append((tid, author, j['in_reply_to_user_id'],'reply'))
        if 'referenced_tweets' in j:
            for rt in j['referenced_tweets']:
                if rt['type'] == 'retweeted':
                    if 'author' in rt:
                        relations.append((tid, author, rt['author']['username'],'rt'))
        if author not in authors:
            authors[author] = []
        authors[author].append(json_file)
        if 'entities' in j:
            if 'mentions' in j['entities']:
                for m in j['entities']['mentions']:
                    relations.append((tid, author, m['username'],'mention'))
                    cited.add(m['username'])
            if 'hashtags' in j['entities']:
                for has in j['entities']['hashtags']:
                    hashtag = has['tag']
                    if hashtag not in hashtags:
                        hashtags[hashtag] = []
                    hashtags[hashtag].append((author,json_file))
    return hashtags, relations, authors, cited, texts


def read_data(path, select='all'):
    """read relation save before

    Args:
        path (str): data path
        select (str, optional): filter data on relation type ('rt' or 'mention' or 'all'). Defaults to 'all'.

    Returns:
        list: edges relation like [
            [user1, user2],
            [user1, user3],
            ...
        ]
    """
    with open(path, 'r') as f:
        data = [line.replace('\n', '').split(';')[1:] for line in f.readlines()]
    assert len(data[0])==3
    if select in ['rt', 'mention']:
        return list(filter(lambda x: x[2] == select, data))
    return data


def build_fasttext(community_file, users_and_text_file, text_dir=None, model_dir=None):
    """

    community_file and users_and_text_file are json file generated with create_community create_community function 

    build the fast text models

    assume text_dir contains files where each file corresponds to one community, and each line contains one preprocessed tweet
    the models are saved in model_dir
    """


def create_graph(data, save=False, path='graph.gml'):
    """create networkx graph

    Args:
        data (list): relation data list from read_data
        save (bool, optional): save graph or not. Defaults to False.
        path (str, optional): path to save if save on true. Defaults to 'graph.gml'.

    Returns:
        nx.Graph: Graph
    """
    g = nx.Graph()
    for edge in data: g.add_edge(*edge)
    if save: nx.write_gml(g, path)
    return g

def create_community(g, return_json=True, resolution=3):
    """create community based on Louvain algorithm

    Args:
        g (nx.Graph): graph data
        return_json (bool, optional): return community in a json. Defaults to True.

    Returns:
        dict: community details as {
            user: {
                edges: number of edges,
                cluster: community id,
            }
        }
    """
    com = nx_comm.louvain_communities(g, resolution=resolution)
    print(f'nb com: {len(com)}')

    print('identifying leaders..')
    print(f'{"name":<20}|{"edges":<20}| commu size')
    print('-'*50)
    
    if return_json:
        community_details = {}
        for i, cluster in enumerate(com):
            if len(cluster)<200: continue
            user_inside_community = []
            for user in cluster:
                community_details[user] = {
                    'edges': len(g[user]),
                    'cluster': i,
                    'text': [],
                    'text_root': []
                }
                user_inside_community.append([user, len(g[user])])
            name, edges = max(user_inside_community, key=lambda x: x[1])

            print(f'{name:<20}|{edges:<20,}| {len(cluster):,}')
        return com, community_details
    return com
    

def add_text_to_community(community_details, text_users, filename=None):
    '''add text for each user in community_details
    
    Args:
        community_details (dict): dictionnary of user from create_community()
        text_users (dict): dictionnary from files with {user: {text: lemmatized text, text_root: original text}}
    '''
    for name in community_details:
        if name in text_users:
            community_details[name]['text'] = text_users.get(name).get('text')
            community_details[name]['text_root'] = text_users.get(name).get('text_root')
    if filename is not None: 
        with open(filename, 'w') as f:
            json.dump(community_details, f)
    
def json_to_df(community_details):
    """convert community_details to dataframe

    Args:
        community_details (dict): community_dict from create_community

    Returns:
        pd.DataFrame: dataframe with username, number of edges and community id
    """
    users = list(community_details.keys())
    edges = [community_details.get(user).get('edges') for user in users]
    clusters = [community_details.get(user).get('cluster') for user in users]

    df = pd.DataFrame()
    df['username'] = users
    df['n_edges'] = edges
    df['i'] = clusters
    return df

def train_word2vec(df, community_details, outputdir=None, lowcase=False):
    """train word2vec skipgram

    Args:
        df (pd.DataFrame): dataframe created with json_to_df()
        community_details (dict): community_details from create_community
        save (bool, optional): save model or not. Defaults to False.

    Returns:
        dict: dictionnary with each model by community {community_number: model}
    """
    models = {}
    for i in tqdm(df.i.unique()):
        
        try:
            if lowcase:
                text_by_community = [[t.lower() for t in txt]  for user in df.username[df['i'] == i] for txt in community_details.get(user).get('text') if len(txt)>0]
            else:
                text_by_community = [txt for user in df.username[df['i'] == i] for txt in community_details.get(user).get('text') if len(txt)>0]
        except AttributeError as e:
            print(e)
            code = input()
            while code != 'stop':
                exec(code)
                code = input()

        bigram = Phrases(text_by_community, min_count=35, threshold=2,delimiter=' ')

        bigram_phraser = Phraser(bigram)
        bigram_token = [bigram_phraser[sen] for sen in text_by_community]
        model = Word2Vec(bigram_token, min_count=1,vector_size= 300,workers=5, window =5, sg = 1)
        models[i] = {'model': model}
        
        if outputdir is not None: model.save(outputdir+"/word2vec_com"+str(i)+".model")
        
    return models

def light_prepro(mot):
    """clean string of accent and useless space

    Args:
        mot (str): string

    Returns:
        str: cleaned string
    """
    return unidecode.unidecode(mot.lower().strip())

def show_closest_hashtags(df, community_details, models, leaders, hashtags, keywords=['climat', 'énergie', 'nature']):
    """add similarity df in a model dict and print them

    Args:
        models (dict): models dict from train_word2vec
    """
    topk_l = 20
    vocab_h = set(hashtags.keys())
    for i, value in models.items():
        similarity_df = pd.DataFrame()
        print(f'---{i}---',sum(df['i']==i),'members')
        topk_leaders = sorted([(v,k) for (k,v) in  leaders[i].items()], reverse=True)[:topk_l]
        vocab = set(value['model'].wv.key_to_index.keys())
        vocab_hc = vocab.intersection(vocab_h) 
        print(' '.join([k+'__'+str(v) for (v,k) in topk_leaders])) 
        for key in keywords:
            if key not in value['model'].wv:
                similarity_df[key] = ['__nokey__' for _ in range(30)]
                continue
            v1 = value['model'].wv.__getitem__(key)
            neighbors = []
            for w2 in vocab_hc:
                try:
                    v2 = value['model'].wv.__getitem__(w2)
                    neighbors.append((w2,1 - scipy.spatial.distance.cosine(v1,v2)))
                except KeyError:
                    neighbors.append('__no match__',0)
            neighbors = sorted(neighbors, key=lambda x: x[1], reverse=True)[:30]
            similarity_df[key] = [light_prepro(mot) for mot, _ in neighbors]
        print(f'    {keywords[0]:<40}|    {keywords[1]:<40}|    {keywords[2]:<40}')
        print('-'*134)
        for j in range(similarity_df.shape[0]): print(f'    {similarity_df[keywords[0]][j]:<40}|    {similarity_df[keywords[1]][j]:<40}|    {similarity_df[keywords[2]][j]:<40}')
        value['similarity_df'] = similarity_df

def get_neighbors_one_model(vocab_com, model, keywords=['climat', 'énergie', 'nature'], topk = 20):
    """add similarity df in a model dict and print them

    Args:
        models (dict): models dict from train_word2vec
    """
    topk_l = 20
    for i, value in models.items():
        similarity_df = pd.DataFrame()
        print(f'---{i}---',sum(df['i']==i),'members')
        topk_leaders = sorted([(v,k) for (k,v) in  leaders[i].items()], reverse=True)[:topk_l]
        
        print(' '.join([k+'__'+str(v) for (v,k) in topk_leaders])) 
        for key in keywords:
            try:
                similarity_df[key] = [light_prepro(mot) for mot, _ in value.get('model').wv.similar_by_word(key, topn=30)]
            except KeyError:
                similarity_df[key] = ['__nokey__' for _ in range(30)]
        print(f'    {keywords[0]:<40}|    {keywords[1]:<40}|    {keywords[2]:<40}')
        print('-'*134)
        for j in range(similarity_df.shape[0]): print(f'    {similarity_df[keywords[0]][j]:<40}|    {similarity_df[keywords[1]][j]:<40}|    {similarity_df[keywords[2]][j]:<40}')
        value['similarity_df'] = similarity_df
        
def add_similar_words_df(df, community_details, models, leaders, hashtags, keywords=['climat', 'énergie', 'nature']):
    """add similarity df in a model dict and print them

    Args:
        models (dict): models dict from train_word2vec
    """
    topk_l = 20
    vocab = set(hashtags.keys())
    for i, value in models.items():
        similarity_df = pd.DataFrame()
        print(f'---{i}---',sum(df['i']==i),'members')
        topk_leaders = sorted([(v,k) for (k,v) in  leaders[i].items()], reverse=True)[:topk_l]
        
        print(' '.join([k+'__'+str(v) for (v,k) in topk_leaders])) 
        for key in keywords:
            try:
                similarity_df[key] = [light_prepro(mot) for mot, _ in value.get('model').wv.similar_by_word(key, topn=30)]
            except KeyError:
                similarity_df[key] = ['__nokey__' for _ in range(30)]
        print(f'    {keywords[0]:<40}|    {keywords[1]:<40}|    {keywords[2]:<40}')
        print('-'*134)
        for j in range(similarity_df.shape[0]): print(f'    {similarity_df[keywords[0]][j]:<40}|    {similarity_df[keywords[1]][j]:<40}|    {similarity_df[keywords[2]][j]:<40}')
        value['similarity_df'] = similarity_df
        
def jaccard_score(A, B, column, n=0):
    """calcul jaccard_score between A and B dataframe regarding to a selected column and n neighbors

    Args:
        A (pd.DataFrame): first dataframe with neighbors words
        B (pd.DataFrame): second dataframe with neighbors words
        column (str): column to compare
        n (int, optional): number of neighbors to calc Jaccard score. Defaults to 0.

    Returns:
        float: return jaccard score
    """
    if A[column][0] == '__nokey__' or B[column][0] == '__nokey__': return 0 # le mot n'est jamais cité par la communauté
    if n == 0: n = min(len(A), len(B))
    a = A[column].tolist()[:n]
    b = B[column].tolist()[:n]
    union = len(set(a + b))
    inter = len([e for e in a if e in b])
    return inter/union

def calc_aj_and_plot(models, df, keywords, save=True):
    """calculate average jaccard for multiple keywords and plot matrix with plotly

    Args:
        models (dict): models dict from train_word2vec
        df (pd.DataFrame): df from json_to_df
        keywords (list): list of keywords (refered to columns in df) to compute aj on
        save (bool, optional): save plotly image. Defaults to True.
    """
    for key in keywords:
        aj_matrix = []
        for community in models:
            ajs = []
            for to_compare in models:
                if community == to_compare: ajs.append(1); continue
                ajs.append(np.mean([jaccard_score(models.get(community).get('similarity_df'), models.get(to_compare).get('similarity_df'), column=key, n=n) for n in range(1,31)]))
            aj_matrix.append(ajs)

        print('ploting..')
        leaders = [df[df.i==comu_i][df[df.i==comu_i].n_edges == max(df[df.i==comu_i].n_edges)].username.tolist()[0] for comu_i in df.i.unique()]

        fig = go.Figure(data=go.Heatmap(
                        z=aj_matrix,
                        x=leaders,
                        y=leaders,
                        colorscale='Viridis'))
        fig.update_layout(
            title=f'AJ score for {key}',
            xaxis_nticks=36)

        if save: fig.write_image(f"/data/mfrancois/social_computing/aj4{key}.png")

def precompute_leaders(data, com):
    sources = {}
    leaders = {}
    for src, dst, typ in data:
        if src not in sources:
            sources[src] = set()
        sources[src].add(dst)
    print('relation ordering done')
    for i, members in enumerate(com):
        print('doing community',i,'over',len(com))
        leaders_this_com = {}
        members_set = set(members)
        for member in members:
            if member not in sources:
                leaders_this_com[member] = 0
            else:
                nrt = len(members_set.intersection(sources[member]))
                leaders_this_com[member] = nrt
        leaders[i] = leaders_this_com
    return leaders


def main():
    data = read_data(path=PATH, select='rt') # all, rt, mention
    """
    sources = {}
    for tweet, src, dst in data:
        if src not in sources:
            sources[src] = []
    """
    
    # keep only relation
    print('========= Manage graph =========')
    edges = list(map(lambda x: x[:2], data))
    g = create_graph(edges, save=True, path='/data/pgay/social_computing/twitter/rt.gml')

    com, community_details = create_community(g)
    leaders = precompute_leaders(data, com)
    print(sorted([len(c) for c in com]))
    print(len(com),'communities')
    
    # get user and text (lighter)
    with open('/data/pgay/social_computing/twitter/community_details.json', 'r') as f:
        text_users = json.load(f)
        
    print('====== Manage communities ======')
    add_text_to_community(community_details=community_details, text_users=text_users, filename='/data/pgay/social_computing/twitter/users_text_idcom_rt.json')
       
    community_details = json.load(open('/data/pgay/social_computing/twitter/users_text_idcom_rt.json'))
    # train word embedding
    df = json_to_df(community_details=community_details) 
    print('====== Training WordToVec ======')
    models = train_word2vec(df=df, community_details=community_details, outputdir='/data/pgay/social_computing/twitter/rt')

    #print('===== Similarity and Plots =====')
    #add_similar_words_df(df, community_details, models, leaders, hashtags, keywords=['climat', 'énergie', 'nature'])    

    # average jaccard score
    #calc_aj_and_plot(models=models, df=df, keywords=keywords, save=True) 


def list_files(path):
    """get all files in path & subdirectories

    Args:
        path (str): path

    Returns:
        list: path files list
    """
    files = []
    for element in os.listdir(path):
        if os.path.isdir(f'{path}/{element}'):
            files.extend(iter(list_files(f'{path}/{element}')))
            continue
        files.append(f'{path}/{element}')
    return files


def extract_relation(files, relation_file=None, write_relation=False, nlp=None):
    relation = []
    users = {}
    for file in tqdm(files):
        with open(file, 'r') as f:
            try:
                tweet = json.load(f)
            except Exception:
                continue
            create_relation(relation, tweet, write_relation, relation_file)
            extract_user_and_text(users, tweet, nlp)
    return relation, users 

def create_relation(relation, tweet, save, relation_file):
    author = tweet.get('author').get('username')
    identifiant = tweet.get('id')
    if re.search('^RT @(.*?):\s', tweet.get('text')):
        relation.append([identifiant, re.findall(r'^RT @(.*?):\s', tweet.get('text'))[0], author, 'rt'])
        if save: 
            RT = re.findall(r'^RT @(.*?):\s', tweet.get('text'))[0]
            relation_file.write(f"{identifiant};{RT};{author};rt\n") # write data
    else:
        with contextlib.suppress(AttributeError, TypeError):
            for mention in tweet.get('entities').get('mentions'):
                muser = mention.get('username')
                if muser is not None:
                    relation.append([identifiant, author, muser, 'mention'])
                    if save:
                        relation_file.write(f"{identifiant};{author};{muser};mention\n") # write data
            
def extract_user_and_text(users, tweet, nlp):
    if not re.search('^RT @(.*?):\s', tweet.get('text')):
        author = tweet.get('author').get('username')

        text_tk = [doc.lemma_ for doc in nlp(tweet.get('text')) if not doc.is_stop and not doc.is_punct and not re.match(r'https?://', doc.text)]
        if author in users:
            users[author]['text'].append(text_tk)
            users[author]['text_root'].append(tweet.get('text'))
        else:
            users[author] = {
                'text': [text_tk],
                'text_root': [tweet.get('text')]
            }


def load_json(ROOT, output_relation_file, user_and_text_file, WRITE_RELATION=True):
    """
    extract the relation in a list of tweets from the ROOT directory and the tweet for each user

    will write the results in the files output_relation_file and user_and_text_file
    """
    files = list_files(path=ROOT)

    if WRITE_RELATION: relation_file = open(output_relation_file, 'w')

    relation, users = extract_relation(files, relation_file=relation_file, write_relation=True, nlp=nlp) # get and write relation

    with open(user_and_text_file, 'w') as f:
        json.dump(users, f)


    print(f'longueur relation: {len(relation)}')

    if WRITE_RELATION: relation_file.close()

