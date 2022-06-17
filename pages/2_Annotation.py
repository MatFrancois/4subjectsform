import streamlit as st
import pymongo
import streamlit.components.v1 as components
import requests

# Améliorations possibles : 
# - Déplacer les boutons sur le côté du tweet
# - Après classification du tweet => impression de la classification faite par le modèle


st.set_page_config(
     page_title="Annotation",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
 )

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    address = st.secrets["mongo"].get('client')
    return pymongo.MongoClient(address)['green']["4subjects_form"]

collection = init_connection()

#  ====================================================  
TWEETS = [
    'https://twitter.com/libe/status/1536700149178716171',
    'https://twitter.com/mbompard/status/1536155056092872704',
    'https://twitter.com/AQuatennens/status/1536435081018998786',
    'https://twitter.com/le_gorafi/status/1536376944954064896',
    'https://twitter.com/sandrousseau/status/1536699120458547201',
    'https://twitter.com/MarxFanAccount/status/1536235354809946112',
    'https://twitter.com/mbompard/status/1536586164542529536'
] # à compléter par la liste de jordy
#  ====================================================  

st.title("Annotate public data")
st.sidebar.image('imgs/logo.png')
# st.sidebar.header("Annotation")

# stockage des variables i / annotations en mémoire => ne sera pas réinitialisée à chaque fois
if 'i' not in st.session_state:
    st.session_state['i'] = 0
if 'annotations' not in st.session_state:
    st.session_state['annotations'] = [] 

# function de création des boutons d'annotation
def annotation_button(label):
    if st.button(label): 
        st.session_state.annotations.append({'tweet': TWEETS[st.session_state.i], 'annotation': label})
    
modalities = [
    'Impensable',
    'Radical',
    'Acceptable',
    'Raisonnable',
    'Populaire',
    'Politique publique',
]

col_tweet, col_button = st.columns([2,4])
# création des boutons d'annotation
with col_button:
    for mod in modalities:
        annotation_button(mod)

# affichage du tweet
response = requests.get(f'https://publish.twitter.com/oembed?url={TWEETS[st.session_state.i]}')
res = response.json()['html']
with col_tweet:
    components.html(res, height=700)

# passage au tweet suivant ou envoie des données si fin de liste
if st.session_state['i'] < len(TWEETS): 
    st.session_state['i'] += 1
else:
    collection.insert_many(st.session_state.annotations)
    st.success("Vous avez annoté tous les tweets, Merci")
    
if st.button("Stop Annotation & Submit"):
    collection.insert_many(st.session_state.annotations)
    # showing current position in oeverton window
    
    # viande
    '''premier indicateur'''
    # avion
    '''deuxieme indicateur'''
    
    # nucléaire
    '''troisieme indicateur'''
    
    # croissance verte 
    '''quatrieme indicateur'''
