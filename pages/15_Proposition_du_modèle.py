import json
import pymongo
import random as r
from plotly.subplots import make_subplots
import time
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

if 'num_clic' not in st.session_state:
    st.session_state['num_clic'] = 0

if 'last_user' not in st.session_state:
    st.session_state['last_user'] = ""
    
if 'username' not in st.session_state:
    st.session_state['username'] = ""

<<<<<<< HEAD

json_file = 'data/users_with_cluster.json' 
sen_form = "la décroissance est nécessaire pour l'avenir"
but_pro = 'Pro Croissance'
but_anti = 'Pro Décroissance'

json_file = 'data/nucleaire_tweets_sorted.json'
sen_form = "l'énergie nucléaire est nécessaire pour l'avenir"
but_pro = "Pro Nucléaire"
but_anti = "Anti Nucléaire"

with open(json_file, 'r') as f:
    users_informations = json.load(f)
=======
if 'log_btn' not in st.session_state:
    st.session_state['log_btn'] = False

@st.cache(allow_output_mutation=True)
def read_data():
    with open('data/users_with_cluster.json', 'r') as f:
        return json.load(f)
>>>>>>> 4f6be782603e1463c617b0918623b6f528ed9331

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    address = st.secrets["mongo"].get('client')
    return pymongo.MongoClient(address)['green']["4subjects_form"]
collection = init_connection()


# get annotation from db
<<<<<<< HEAD
## read the database to get the annotations already done
annotations = list(collection.find())
counts = {}
for a in annotations:
    print(a)
    if 'username' not in a:
        continue
    user = a['username']
    if user not in counts:
        counts[user] = 0
    counts[user]+=1

# only keep the users which are not already annotated
users_informations = dict(filter(
    lambda x: len(x[1].get('id'))>2 and x[0] not in st.session_state['chosen_user'] and not (x[0] in counts and counts[x[0]] > 2), users_informations.items()
))
print(f"nombre d'utilisateurs restant : {len(users_informations)}")
=======


>>>>>>> 4f6be782603e1463c617b0918623b6f528ed9331

# ==============================================================================
# définition du squelette de la page

with st.container(): # logging & chargement / filtre des données
    _, col_user, go_further_button, _ = st.columns([1,3,1,1])

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

<<<<<<< HEAD


idsession = st.experimental_get_query_params()
if 'idsession' not in idsession:
    idsession['idsession'] = time.time()
    username = col_user.text_input('Renseignez votre Username twitter ou inventez un login', value="")
    go_further_button.write('.')
else:
    username = idsession['username'][0]

if username or go_further_button.button('Annoter'):
    st.session_state['username'] = username
    # filter labelled tweets here
=======
st.session_state['username'] = col_user.text_input('Renseignez votre Username twitter ou laissez vide et cliquer sur "Annoter"', value="")
go_further_button.write('.')


if st.session_state['username']!='' or go_further_button.button('Annoter') or st.session_state['log_btn']:
    st.session_state['log_btn'] = True
    users_informations = read_data()
    users_informations = dict(filter(
        lambda x: len(x[1].get('id'))>2 and x[0] not in st.session_state['chosen_user'], users_informations.items()
    ))
    print(f"nombre d'utilisateurs restant : {len(users_informations)}")
    # filter labelled tweets here
    
>>>>>>> 4f6be782603e1463c617b0918623b6f528ed9331
    col_description.markdown(
    '''
---

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

    if st.session_state['num_clic'] != 0:
        # gestion de l'historisation des utilisateurs parcourus
        print(f"add {st.session_state['last_user']}")
        st.session_state['chosen_user'].append(st.session_state['last_user'])

    # choix de personnalité à afficher
    col_button.write('Ou tirer une personnalité')
    if col_button.button('aléatoirement'):
        st.session_state.selector = list(users_informations.keys())[r.randint(1, len(users_informations))]

    col_croissance.write('Ou parmi les', display=None)
    if col_croissance.button(but_pro):
        st.session_state.selector = random_in_top_n(pro_croissance, score='db', n=10)
    col_decroissance.write('Ou parmi les', display=None)
    if col_decroissance.button(but_anti):
        st.session_state.selector = random_in_top_n(pro_decroissance, score='da', n=10)
    selected_user = col_slider.selectbox("Choisir une personnalité", users_informations.keys(), key='selector')
    st.session_state['num_clic'] += 1
    st.session_state['last_user'] = selected_user

    # affichage de la description de la personnalité
    col_image.image(users_informations.get(selected_user)['profil_image_url'])
    col_desc.info(f"**{selected_user}** : {users_informations.get(selected_user)['desc']}")

    ids = users_informations.get(selected_user).get('id')
    if len(ids[0]) > 1:
        ids = [ idi for (idi,s) in sorted(ids, key=lambda x:x[1]) ]
    ids = ids[:3]
    print('ID:',ids)
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
        st.write(f"""Pour {selected_user}, penser que "{sen_form}" est...""")
        for mod in modalities:
            if st.button(mod, key='1'): 
                st.session_state.annotations.append({'tweet': selected_user, 'annotation': mod})
                collection.insert_one({'login':username, 'idsession':idsession['idsession'][0],'username':selected_user,'annotation':mod})
                #figure
                with col_plot:
                    categories = [
                        {'name': but_pro, 'value': users_informations.get(selected_user).get('score').get('db'), 'color': '#296DC0'},
                        {'name': but_anti, 'value': users_informations.get(selected_user).get('score').get('da'), 'color': '#7AB163'},
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

