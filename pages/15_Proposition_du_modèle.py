import json
import random as r
from plotly.subplots import make_subplots

import requests
import streamlit as st
# import pymongo
import streamlit.components.v1 as components

st.set_page_config(
     page_title="Annotation",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
 )
st.sidebar.image('imgs/logo.png')

# ==============================================================================
if 'chosen_user' not in st.session_state:
    st.session_state['chosen_user'] = []
    
if 'annotations' not in st.session_state:
    st.session_state['annotations'] = []

with open('data/filtered_user_and_score.json', 'r') as f:
    users_informations = json.load(f)

users_informations = dict(filter(
    lambda x: len(x[1].get('id'))>2 and x[0] not in st.session_state['chosen_user'], users_informations.items()
))
print(f"nombre d'utilisateurs restant : {len(users_informations)}")

# ==============================================================================
# définition du squelette de la page

with st.container(): # description de la page
    _, col_description, _ = st.columns([1,3,1]) 

with st.container(): # slider & bouton
    col_slider, col_button, col_croissance, col_decroissance = st.columns([4,2,1,1])
    
cont_selected_user = st.container()

with st.container(): # information sur l'utilisateur choisi
    col_image, col_desc = st.columns([1,9])
    
with st.container():# afficher les 3 tweets et le choix d'annotation global pour le user => suite à l'annotation afficher les résultats du modele
    col_tweet, col_annotation, col_plot = st.columns([3,1,3])
# ==============================================================================

col_description.markdown(
'''

##### Visualiser ci-dessous des comptes Twitter placé par notre modèle sur l'échelle d'Overton. Nous vous demandons d'évaluer ces comptes pour participer à l'amélioration de notre modèle et construire un corpus académique sur ce sujet.

---''')

def random_in_top_n(users, score='da', n=50):
    """Selects a random user from the top n users

    Args:
        users (dict): users_information format 
        score (str, optional): score to sort the user from. Defaults to 'da'.
        n (int, optional): number of top n. Defaults to 50.
    """
    sorted_users = dict(sorted(
        users.items(), key=lambda item: item[1].get('score').get(score)
    ))
    sorted_users = list(sorted_users.keys())[n:] # on ne garde que les 50 meilleurs
    r.shuffle(sorted_users) # mélange de la liste
    return sorted_users[0]

# filtre de score
pro_croissance = dict(filter(
    lambda x: x[1].get('score').get('db') > x[1].get('score').get('da'), users_informations.items()
)) 

pro_decroissance = dict(filter(
    lambda x: x[1].get('score').get('db') < x[1].get('score').get('da'), users_informations.items()
)) 

# choix de personnalité à afficher
col_button.write('Ou tirer une personnalité')
if col_button.button('aléatoirement'):
    print('aléatoirement')
    st.session_state.selector = list(users_informations.keys())[r.randint(1, len(users_informations))]
    
col_croissance.write('Ou parmi les', display=None)
if col_croissance.button('Pro-Croissance'):
    print('Pro-Croissance')
    st.session_state.selector = random_in_top_n(pro_croissance, score='db', n=10)
    
col_decroissance.write('Ou parmi les', display=None)
if col_decroissance.button('Pro-Décroissance'):
    print('Pro-Décroissance')
    st.session_state.selector = random_in_top_n(pro_decroissance, score='da', n=10)
selected_user = col_slider.selectbox("Choisir une personnalité", users_informations.keys(), key='selector')
 

# affichage de la description de la personnalité
col_image.image(users_informations.get(selected_user)['profil_image_url'])
col_desc.info(f"**{selected_user}** : {users_informations.get(selected_user)['desc']}")

ids = users_informations.get(selected_user).get('id')[:3]
list_response = [requests.get(f"https://publish.twitter.com/oembed?url=https://twitter.com/{selected_user}/status/{id_tweet}&hide_thread=1&hide_media=1") for id_tweet in ids]
embedded_tweets = [response.json()['html'] for response in list_response]

modalities = [
    'Impensable',
    'Radical',
    'Acceptable',
    'Raisonnable',
    'Populaire',
    'Politique publique',
]

# zone d'annotation
with col_annotation : 
    st.write(f"""Pour {selected_user}, penser que "la croissance verte est nécessaire pour l'avenir" est...""")
    for mod in modalities:
        if st.button(mod, key='1'): 
            st.session_state.annotations.append({'tweet': selected_user, 'annotation': mod})
            
           # gestion de l'historisation des utilisateurs parcourus
            st.session_state['chosen_user'].append(selected_user) 
    
            #figure
            with col_plot:
                categories = [
                    {'name': 'Pro Croissance', 'value': users_informations.get(selected_user).get('score').get('db'), 'color': '#296DC0'},
                    {'name': 'Pro Decroissance', 'value': users_informations.get(selected_user).get('score').get('da'), 'color': '#7AB163'},
                ]
                
                subplots = make_subplots(
                    rows=len(categories),
                    cols=1,
                    column_titles=["Qu'en pense notre modèle ?"],
                    shared_xaxes=True,
                    print_grid=False,
                )
                _ = subplots['layout'].update(
                    width=550,
                )
                for k, x in enumerate(categories):
                    subplots.add_trace(dict(
                        type='bar',
                        orientation='h',
                        y=[x["name"]],
                        x=[x["value"]],
                        width=0.5,
                        hoverinfo='text',
                        textposition='auto',
                        showlegend=False,
                        marker=dict(
                            color=x["color"],
                        ),
                    ), k+1, 1)
                st.plotly_chart(subplots)
                
                
 

with col_tweet:
    for embedded_tweet in embedded_tweets:
        components.html(embedded_tweet, height=380)
        
st.markdown('''---''')
