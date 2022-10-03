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
        print(config["page_name"], standardize_name(config["page_name"]))
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
     initial_sidebar_state="expanded",
 )

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    address = st.secrets["mongo"].get('client')
    return pymongo.MongoClient(address)['green']["4subjects_form"]

#collection = init_connection()

@st.cache(allow_output_mutation=True)
def get_unique_id():
    username = st.experimental_get_query_params().get('username')[0] if "username" in st.experimental_get_query_params().keys() else None 
    return username, str(time.time()) # http://localhost:8501/?username=toto
#  ====================================================  

collection = init_connection()
modalities = (
    'Impensable',
    'Radical',
    'Acceptable',
    'Raisonnable',
    'Populaire',
    'Politique publique',
)

st.title("Fenêtre d'Overton & Social Computing")
st.sidebar.image('imgs/logo.png')

# Intro
_, col, _ = st.columns([1,3,1])

username, id_session = get_unique_id()
if username is None:
    username = col.text_input('Renseignez votre Username twitter ou inventez un login', value="")
    st.session_state['username'] = username

print(f'{username}, {id_session}')
if username: 
  col.markdown('''
  > La **fenêtre d'Overton**, aussi connue comme la fenêtre de discours, est une allégorie qui situe l'ensemble des idées, opinions ou pratiques considérées comme plus ou moins acceptables dans l'opinion publique d'une société. 

  ''')


  idee = col.selectbox("Les 5 niveaux de la fenêtre d'Overton:", ['Politique publique', 'Populaire', 'Raisonnable', 'Acceptable', 'Radical', 'Impensable'])
  if idee == 'Politique publique':
      col.success("L'idée est défendue par la politique publique ou trouve des représentants pour concevoir des projets de loi.")
  elif idee == "Populaire":
      col.success("L'idée s'implante culturellement et est intégrée dans des films, musiques, journaux etc.")
  elif idee == 'Raisonnable':
      col.success("L'idée se justifie (scientifiquement par exemple) et se légitime dans la population.")
  elif idee == 'Acceptable':
      col.success("L'idée progresse dans le débat publique.")
  elif idee == 'Radical':
      col.success("Le sujet est exploré par la science (exacte ou non).")
  elif idee == 'Impensable':
      col.success("L'idée est jugée immorale, elle ou son application est punie par la loi.")


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
      "Le développement du nucléaire.",
      modalities,
      horizontal=True
  ) 

  ## ajouter les autres questions présentent dans le doc

  col.markdown('''---''')
  submitted = col.button("Soumettre & Annoter")

  # création du json de réponses
  if submitted:
      mydict = {
          'time': id_session,
          'login':username,
          "rep6": rep6,
          "rep7": rep7,
          "rep8": rep8,
          "rep9": rep9,
      }
      collection.insert_one(mydict)

      # envoie des données et redirection vers la page d'annotations
      # collection.insert_one(mydict)
      st.success('Votre contribution a bien été enregistrée ! Merci')
      switch_page('Proposition du modèle')
      #webbrowser.open('http://localhost:8501/Proposition_du_modèle?idsession='+id_session+'&username='+username)
      #webbrowser.open('http://51.38.39.210:8501/Proposition_du_modèle?idsession='+id_session+'&username='+username)
      #webbrowser.open('https://share.streamlit.io/matfrancois/4subjectsform/main/Home.py/Proposition_du_modèle?idsession='+id_session)
      print('done')


