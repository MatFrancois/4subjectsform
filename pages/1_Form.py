import streamlit as st
import pymongo
import streamlit.components.v1 as components
import requests


st.set_page_config(
     page_title="Form",
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

st.title("Form")
st.sidebar.image('imgs/logo.png')
# st.sidebar.header("Completing the form")

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

    
    

    # viande
    '''premier indicateur'''
    # avion
    '''deuxieme indicateur'''
    
    # nucléaire
    '''troisieme indicateur'''
    
    # croissance verte 
    '''quatrieme indicateur'''

