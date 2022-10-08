# https://discuss.streamlit.io/t/streamlit-docker-nginx-ssl-https/2195/4
import json
import pymongo
import random as r
import time
import requests
import streamlit as st
import streamlit.components.v1 as components


def get_annot_counts_per_user(collection, topic):
    # get annotation from db
    ## read the database to get the annotations already done
    annotations = list(collection.find())
    counts = {}
    for a in annotations:
        if 'username' not in a:
            continue
        user = a['username']
        t = a['topic']
        if t != topic:
            continue
        if user not in counts:
            counts[user] = 0
        counts[user]+=1
    return counts

def random_in_top_n(users, score='da', n=50):
    """Selects a random user from the top n users

    Args:
        users (dict): users_information format
        score (str, optional): score to sort the user from. Defaults to 'da'.
        n (int, optional): number of top n. Defaults to 50.
    """
    sorted_users = sorted(
        users_informations.keys(), key=lambda item: users_informations[item].get('stance').get('da'),reverse=True
    )[:n]
    r.shuffle(sorted_users) # mélange de la liste
    return sorted_users[0]

def random_in_top_n_kw(users, kw, score='da', n=50):
    """Selects a random user from the top n users

    Args:
        users (dict): users_information format
        score (str, optional): score to sort the user from. Defaults to 'da'.
        n (int, optional): number of top n. Defaults to 50.
    """
    user_with_words = dict(filter(
            lambda x: len([1 for t in x[1]['ids'] for w in kw if w in t['text'].lower()])>0, users.items()
        ))
    sorted_users = sorted(
        user_with_words.keys(), key=lambda item: users_informations[item].get('stance').get(score),reverse=True
    )[:n]
    r.shuffle(sorted_users) # mélange de la liste
    return sorted_users[0]


# ==============================================================================
#  Call backs function for the different buttons
def set_topic(): # so when reloading, the code above the button will integrate that the button has been clicked. MAYBE TRY LAMBDA FUNCTION ?
    st.session_state['topic'] = st.session_state.selector


def say_go(): # so when reloading, the code above the button will integrate that the button has been clicked. MAYBE TRY LAMBDA FUNCTION ?
    st.session_state['go'] = True

st.set_page_config(
     page_title="Annotation",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
 )
st.sidebar.image('imgs/logo.png')

# ==============================================================================
# initialise session state variables
if 'chosen_user' not in st.session_state:
    st.session_state['chosen_user'] = []

if 'annotations' not in st.session_state:
    st.session_state['annotations'] = []

if 'num_clic' not in st.session_state:
    st.session_state['num_clic'] = 0

if 'last_user' not in st.session_state:
    st.session_state['last_user'] = ""

if 'username' not in st.session_state:
    st.session_state['username'] = ""

if 'topic' not in st.session_state:
    st.session_state['topic'] = ""

if 'id_session' not in st.session_state:
    st.session_state['id_session'] = str(time.time())

# ==============================================================================
# initialise topic related information
topics = ['Nucleaire', '(Dé)croissance économique', 'Consommation de viande','Aviation']
#r.shuffle(topics)
if st.session_state['topic'] == '':
    topic = topics[0]
else:
    topic = st.session_state['topic']

if topic=='Nucleaire':
    json_file = 'data/nucleaire_tweets_sorted_fasttext.json'
    sen_form = "l'énergie nucléaire est nécessaire pour l'avenir"
    but_pro = "Anti Nucléaire"
    but_anti = "Pro Nucléaire"
    kw = ['nucle','nuclé','radiat','radioa']
elif topic=='(Dé)croissance économique':
    json_file = 'data/croissance_tweets_sorted_fasttext.json'
    sen_form = "la croissance économique est nécessaire pour l'avenir"
    but_pro = "Pro Croissance"
    but_anti = "Anti Croissance"
    kw = ['croiss','économ','financ','dévelop']
elif topic=='Consommation de viande':
    json_file = 'data/viande_tweets_sorted_fasttext.json'
    sen_form = "Réduire la consommation de viande est nécessaire pour l'avenir"
    but_pro = "Pro Viande"
    but_anti = "Anti Viande"
    kw = ['viande','anima','vegan','vegeta','éleva','chasse']
elif topic=='Aviation':
    json_file = 'data/avion_tweets_sorted_fasttext.json'
    sen_form = "Réduire le transport aérien est nécessaire pour l'avenir"
    but_pro = "Pro avion"
    but_anti = "Anti avion"
    kw = ['avia','avion','aéri','hydrog']


# ==============================================================================
# Data loading and mongo db
with open(json_file, 'r') as f:
    users_informations = json.load(f)

@st.cache(allow_output_mutation=True)
def read_data():
    with open(json_file, 'r') as f:
        return json.load(f)

username2name = json.load(open('data/username2name.json'))

# Initialize connection.to mongodb
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    address = st.secrets["mongo"].get('client')
    return pymongo.MongoClient(address)['green']["4subjects_form"]
collection = init_connection()
# obtain number of annotatations already made for each users
counts = get_annot_counts_per_user(collection, topic)
#counts = {}
# ==============================================================================
# définition du squelette de la page
with st.container(): # logging & chargement / filtre des données
    _, col_user, go_further_button, _ = st.columns([1,3,1,1])

with st.container(): # description de la page
    _, col_description, _ = st.columns([1,3,1])

with st.container(): # slider & bouton
    col_slider, col_croissance, col_decroissance,  col_button = st.columns([3,2,1,2])

with st.container(): # information sur l'utilisateur choisi
    _, col_desc = st.columns([1,9])

with st.container():# afficher les 3 tweets et le choix d'annotation global pour le user
    _, col_tweet, _ = st.columns([1,6,1])

with st.container():# afficher les 3 tweets et le choix d'annotation global pour le user => suite à l'annotation afficher les résultats du modele
    _, col_question = st.columns([1,9])
    _, col_b1, col_b2, col_b3, col_b4, col_b5, col_b6, _ = st.columns([1,1,1,1,1,1,2,1])
    col_bs = [col_b1, col_b2, col_b3, col_b4, col_b5, col_b6]
# ==============================================================================

# get parameter from the url, in case we are coming from the home page
idsession = st.experimental_get_query_params()

if 'username' in idsession and st.session_state['username']=="": # username given by the url
    st.session_state['username'] = idsession['username'][0]
elif 'login' in st.session_state: # login text input field has been used
    st.session_state['username'] = st.session_state['login']
    st.session_state['go'] = True
elif st.session_state['username']=="":# no username available, display the text input field
    idsession['idsession'] = time.time()
    st.session_state['username'] = col_user.text_input('Renseignez votre Username twitter ou inventez un login', value="", key="login")


# ==============================================================================
# First landing on the page : gives instructions
if 'go' not in st.session_state:
    col_description.markdown(
    '''
##### Découvrez maintenant les prédictions de notre modèle d'IA, et aidez-nous à l'évaluer en classant chaque compte prédit selon votre opinion.
---''')

    if 'username' in idsession or st.session_state['username']!="": # don't display the button, the app will start on the input text field
        col_description.button("C'est parti!", on_click=say_go)




# ==============================================================================
# Username given, and instruction validated, let's go on the annotations
if 'go' in st.session_state:
    users_informations = read_data()
    # only keep users with more than two tweets AND not already annotated in this session AND not annotated more than 2 times in the mongodb
    users_informations_f = dict(filter(
        lambda x: len(x[1].get('ids'))>2 and x[0] not in st.session_state['chosen_user'] and not (x[0] in counts and counts[x[0]] >= 3) , users_informations.items()
    ))
    print('prop', 'voixdunucleaire' in users_informations_f)
    #users_informations = dict(filter(
    #    lambda x: len(x[1].get('ids'))>2 and x[0] not in st.session_state['chosen_user'], users_informations.items()
    #))
    print(f"nombre d'utilisateurs restant : {len(users_informations_f)}")

    # choix de personnalité à afficher
    col_button.selectbox("Ou changez de sujet", topics, key='topic')
    col_croissance.write('Ou une personnalité prédite comme', display=None)
    if st.session_state['last_user'] == '':
        st.session_state.selector = random_in_top_n_kw(users_informations_f, kw, score='db', n=10)
    if col_croissance.button(but_pro):
        st.session_state.selector = random_in_top_n_kw(users_informations_f, kw, score='db', n=10)
    col_decroissance.write('Ou comme', display=None)
    if col_decroissance.button(but_anti):
        st.session_state.selector = random_in_top_n_kw(users_informations_f, kw, score='da', n=10)
    if 'changed_on_annotation' in st.session_state and st.session_state['changed_on_annotation'] != '':
        st.session_state.selector = st.session_state['changed_on_annotation']
        st.session_state['changed_on_annotation'] = ''
    selected_user = col_slider.selectbox("Affichez les tweets d'une personnalité de votre choix sur le sujet '"+topic+"'", users_informations.keys(), key='selector')
    st.session_state['num_clic'] += 1
    st.session_state['last_user'] = selected_user

    if st.session_state['num_clic'] > 1:
        # affichage de la description de la personnalité
        col_desc.info(f"**{username2name[selected_user]} ({selected_user})** : {users_informations.get(selected_user)['desc']}")

        selected_tweets = sorted(users_informations[selected_user]['ids'], key=lambda x:x['s'] ) [:3]
        modalities = [
            'Impensable',
            'Radical',
            'Acceptable',
            'Raisonnable',
            'Populaire',
            'Politique publique',
        ]
        def annotate():
            """
            when button modalities are pressed, add the annotated user to the
             annotations and change the selected user
            """
            label = None
            for mod in modalities:
                if st.session_state[mod]:
                    label = mod
                    break
            st.session_state.annotations.append({'tweet': selected_user, 'annotation': label})
            st.session_state['changed_on_annotation'] = random_in_top_n(users_informations, score='db', n=10)
            st.session_state['chosen_user'].append(selected_user)
            my_dict = {
              'time': st.session_state['id_session'],
              'login':st.session_state['username'],
              'topic':topic,
              'username':selected_user,
              'annotation':label,
            }
            collection.insert_one(my_dict)

        for tweet in selected_tweets:
            col_tweet.markdown(f"""{tweet['date']}""")
            text = tweet['text'].replace('\n',' ')
            col_tweet.markdown(f"""*{text}* ({tweet['rt']} retweets, {tweet['likes']} likes) """)

        col_question.markdown('''---''')
        col_question.error(f"""**À VOUS D'EVALUER** : pour *@{selected_user}*, penser que "{sen_form}" est...""")
        for i, mod in enumerate(modalities):
            if col_bs[i].button(mod, on_click=annotate, key=mod):
                col_bs[i].success('Merci pour Votre contribution !')

