from __future__ import annotations
import streamlit as st
import pymongo
import streamlit.components.v1 as components
import requests


st.set_page_config(
     page_title="Social Computing",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',   # change this part
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    address = st.secrets["mongo"].get('client')
    return pymongo.MongoClient(address)['green']["4subjects_form"]

collection = init_connection()

#  ====================================================  

st.title("Fenêtre d'Overton et NLP")
st.sidebar.image('imgs/logo.png')

tweets = [
    'https://twitter.com/libe/status/1536700149178716171',
    'https://twitter.com/mbompard/status/1536155056092872704',
    'https://twitter.com/AQuatennens/status/1536435081018998786',
    'https://twitter.com/le_gorafi/status/1536376944954064896',
    'https://twitter.com/sandrousseau/status/1536699120458547201',
    'https://twitter.com/MarxFanAccount/status/1536235354809946112',
    'https://twitter.com/mbompard/status/1536586164542529536'
]

with st.form('Voici le formulaire de social computing !'):
    rep1 = st.selectbox(" Diminuer votre consommation de viande ?", ("Oui", "Non", "Peut-être"))

    # A quel point vous considérez vous sensible à la question climatique ?
    rep2 = st.radio("A quel point vous considérez vous sensible à la question climatique ?", 
                ('Indifférent', 'Peu sensisble', 'Neutre', 'Sensible', 'Très sensible'), horizontal=True)

    # Voter pour un parti à tendance écologiste
    rep3 = st.radio("Considérez vous votre vote comme écologique", ('Oui', 'Non'))
    rep4, rep4bis = st.select_slider(
        'Où placez vous votre vote ?',
        options=['Radical Gauche', 'Gauche', 'Centre-gauche', 'Centre', 'Centre-droite', 'Droite', 'Radical droite'],
        value=('Radical Gauche', 'Radical droite'))
    
    
# Etes vous prêts à payer des impôts supplémentaires pour favoriser l'écologie ?

# Cela vaut le coup d'investir dans l'éolien pour lutter contre le changement climatique. (ou le nucléaire)

# Calculer son bilan carbone et l'utiliser pour orienter son mode de vie

# Ne plus avoir de voiture (si j'habite en ville), ou acheter une petite voiture si je suis en campagne.

# Acheter une voiture électrique afin de lutter contre le changement climatique

# Ne plus prendre l'avion

# Devenir végétarien

# Diminuer la vitesse sur les autoroutes

# Télétravail

# Produits Reconditionnés

# Baisser la température de l'eau au quotidien (lave-vaisselle, lave-linge, douche, bain ... )

# Moins utiliser les services de streaming (Netflix, Prime etc)

# Les accords de Paris et les rapports du GIEC sont-ils inutiles ?

# Les conclusions du GIEC indiquant que le réchauffement climatique est une urgence

# La guerre en Ukraine, la crise du covid ont elles modifié votre vision sur l'écologie ?

# Vous considérez vous comme écolo ?

# Si non, est-ce du à un manque de moyen ? connaissance ? intérêt sur le sujet?



    submitted = st.form_submit_button("Submit")
    
    if submitted:
        mydict = {
            "rep1": rep1,
            "rep2": rep2,
            'rep3': rep3,
            'rep4': [rep4, rep4bis],
        }

        collection.insert_one(mydict)
        print('done')
    
annotations = []

c1, c2, c3, c4, c5, c6 = st.columns(6)

#refactor !!
if c1.button("Impensable"): 
    annotations.append({'tweet': tweets[0], 'annotation': 'Impensable'})
if c2.button("Radical"): 
    annotations.append({'tweet': tweets[0], 'annotation': 'Radical'})
if c3.button("Acceptable"): 
    annotations.append({'tweet': tweets[0], 'annotation': 'Acceptable'})
if c4.button("Raisonnable"): 
    annotations.append({'tweet': tweets[0], 'annotation': 'Raisonnable'})
if c5.button("Juste"): 
    annotations.append({'tweet': tweets[0], 'annotation': 'Juste'})
if c6.button("Evidence"): 
    annotations.append({'tweet': tweets[0], 'annotation': 'Evidence'})
print(len(tweets))
response = requests.get(f'https://publish.twitter.com/oembed?url={tweets[0]}')
tweets.pop(0)
res = response.json()['html']
components.html(res, height=700)

if st.button("Stop"):
    collection.insert_many(annotations)
    # showing current position in oeverton window
    
    # viande
    '''premier indicateur'''
    # avion
    '''deuxieme indicateur'''
    
    # nucléaire
    '''troisieme indicateur'''
    
    # croissance verte 
    '''quatrieme indicateur'''
