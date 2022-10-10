import streamlit as st
import pymongo
import time
import webbrowser


def switch_page(page_name: str):
    from streamlit import _RerunData, _RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")
    page_name = standardize_name(page_name)

    pages = get_pages("Home.py")  # OR whatever your main page is called

    for page_hash, config in pages.items():
        #print(config["page_name"], standardize_name(config["page_name"]))
        if standardize_name(config["page_name"]) == page_name:
            raise _RerunException(
                _RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")

st.set_page_config(
     page_title="Fenêtre d'Overton & Social Computing",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="collapsed",
 )

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    address = st.secrets["mongo"].get('client')
    return pymongo.MongoClient(address)['green']["4subjects_form"]


#@st.cache(allow_output_mutation=True)
def get_unique_id():
    id_session = str(time.time())
    st.session_state['username'] = id_session
    st.session_state['id_session'] = id_session
    #username = st.experimental_get_query_params().get('username')[0] if "username" in st.experimental_get_query_params().keys() else None
    #return username, str(time.time()) # http://localhost:8501/?username=toto
#  ====================================================

collection = init_connection()
modalities = (
    'Impensable',
    'Radical',
    'Acceptable',
    'Raisonnable',
    'Populaire',
    'Déjà intégré comme politique publique',
)

st.title("Fenêtre d'Overton")
st.markdown('''
#### _Ou l'étude de l'acceptabilité d'un sujet dans notre société..._
---
''')
st.sidebar.image('imgs/logo.png')

# Intro
_, col, _ = st.columns([1,3,1])

if 'id_session' not in st.session_state:
    col.markdown('''
    Observez et évaluez les prédictions automatiques du positionnement des influenceurs sur Twitter pendant la campagne prédidentielle de 2017.

    Premièrement, donnez votre opinion pour nous permettre de controler les biais de l'évaluation.
    ''')
    #username = col.text_input('Renseignez votre Username twitter ou inventez un login', value="")
    col.button("Ok!", on_click=get_unique_id)

if 'id_session' in st.session_state:

  col.markdown('''---
  **Comment évaluez-vous ces différents choix de société ?**
  ''')

  # rajouter des phrases de climatosceptiques ?

  rep6 = col.radio(
      "La décroissance (par opposition à la croissance économique)",
      modalities,
      horizontal=True
  )

  #col.markdown('Voici la définition de croissance verte selon [OECD](https://www.oecd.org/fr/croissanceverte/quest-cequelacroissanceverteetcommentpeut-elleaideraassurerundeveloppementdurable.htm).')
  #col.info('La **croissance verte** signifie *promouvoir la croissance économique et le développement* tout en veillant à ce que les actifs naturels continuent de fournir les ressources et services environnementaux dont dépend notre bien-être.')
  rep7 = col.radio(
      "La diminution du transport aérien",
      modalities,
      horizontal=True
  )

  rep8 = col.radio(
      "La diminution de la consommation de viande.",
      modalities,
      horizontal=True
  )

  rep9 = col.radio(
      "Le développement de l'énergie nucléaire.",
      modalities,
      horizontal=True
  )
  col.markdown('''---''')
  submitted = col.button("Soumettre & Annoter")
  # création du json de réponses
  if submitted:
      mydict = {
          'time': st.session_state['id_session'],
          'login':st.session_state['username'],
          "rep6": rep6,
          "rep7": rep7,
          "rep8": rep8,
          "rep9": rep9,
      }
      # envoie des données et redirection vers la page d'annotations
      collection.insert_one(mydict)
      st.success('Votre contribution a bien été enregistrée ! Merci')
      switch_page('Proposition du modèle')
      print('done')
