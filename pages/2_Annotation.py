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

st.title("Annotate public data")
st.sidebar.image('imgs/logo.png')
# st.sidebar.header("Annotation")

tweets = [
    'https://twitter.com/libe/status/1536700149178716171',
    'https://twitter.com/mbompard/status/1536155056092872704',
    'https://twitter.com/AQuatennens/status/1536435081018998786',
    'https://twitter.com/le_gorafi/status/1536376944954064896',
    'https://twitter.com/sandrousseau/status/1536699120458547201',
    'https://twitter.com/MarxFanAccount/status/1536235354809946112',
    'https://twitter.com/mbompard/status/1536586164542529536'
] # à compléter par la liste de jordy

if 'i' not in st.session_state:
    st.session_state['i'] = 0
if 'annotations' not in st.session_state:
    st.session_state['annotations'] = [] # ajouter la date d'execution ? ou un id unique ? 

c1, c2, c3, c4, c5, c6 = st.columns(6)

#refactor !!
if c1.button("Impensable"): 
    st.session_state.annotations.append({'tweet': tweets[st.session_state.i], 'annotation': 'Impensable'})
if c2.button("Radical"): 
    st.session_state.annotations.append({'tweet': tweets[st.session_state.i], 'annotation': 'Radical'})
if c3.button("Acceptable"): 
    st.session_state.annotations.append({'tweet': tweets[st.session_state.i], 'annotation': 'Acceptable'})
if c4.button("Raisonnable"): 
    st.session_state.annotations.append({'tweet': tweets[st.session_state.i], 'annotation': 'Raisonnable'})
if c5.button("Juste"): 
    st.session_state.annotations.append({'tweet': tweets[st.session_state.i], 'annotation': 'Juste'})
if c6.button("Evidence"): 
    st.session_state.annotations.append({'tweet': tweets[st.session_state.i], 'annotation': 'Evidence'})


response = requests.get(f'https://publish.twitter.com/oembed?url={tweets[st.session_state.i]}')
res = response.json()['html']
components.html(res, height=700)
st.session_state['i'] += 1

if st.button("Stop"):
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
