import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect


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

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)


#  ====================================================  

st.title("Fenêtre d'Overton et NLP")
st.sidebar.image('imgs/logo.png')

@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
for row in rows:
    st.write(f"{row.name} has a :{row.pet}:")


with st.form('Voici le formulaire de social computing !'):
    st.selectbox(" Diminuer votre consommation de viande ?", ("Oui", "Non", "Peut-être"))
    
    # A quel point vous considérez vous sensible à la question climatique ?
    st.radio("A quel point vous considérez vous sensible à la question climatique ?", ('Indifférent', 'Peu sensisble', 'Neutre', 'Sensible', 'Très sensible'), horizontal=True)
    
    # Voter pour un parti à tendance écologiste
    st.radio("Considérez vous votre vote comme écologique", ('Oui', 'Non'))
    
    
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
    # if submitted:
    #     st.write(" Voici la liste de vos réponses :" )
    #     st.write("Réponse 1 : ", resp1)
    #     st.write("Réponse 2 : ", resp2)
