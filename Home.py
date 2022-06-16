import streamlit as st
import pymongo
import time 
import webbrowser

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

collection = init_connection()

@st.cache(allow_output_mutation=True)
def get_unique_id():
    return str(time.time())
#  ====================================================  

id_session = get_unique_id()

st.title("Fenêtre d'Overton & Social Computing")
st.sidebar.image('imgs/logo.png')

_, col, _ = st.columns([1,3,1])
col.markdown('''---
Qu'est ce que la fenêtre d'Overton ?
La fenêtre d'Overton, aussi connue comme la fenêtre de discours, est une allégorie qui situe 
l'ensemble des idées, opinions ou pratiques considérées comme plus ou moins acceptables dans 
l'opinion publique d'une société. 

Qu'est ce que je peux trouver ici ?
- Un questionnaire (ci dessous), permettant de mieux comprendre la perception de certains sujets lié à l'écologie et leur évolution dans le temps.
- Une page d'[annotation](https://share.streamlit.io/matfrancois/4subjectsform/main/Home.py/Annotation) permettant de comparer sa perception d'un message avec celle d'un modèle entrainé par nos soins

Add graphics
             
### Collecte d'opinion concernant plusieurs discours de société
---
Prenez bien le temps de répondre à toutes les questions. Puis dans un second temps d'envoyer vos 
réponses à partir du boutton "Envoyer", en bas de la page. Sans ça, les valeurs par défaut 
risqueront d'être utilisées.

Merci de ne répondre qu'une seule fois au questionnaire.

Pour en savoir plus sur notre équipe ou pour nous contacter, merci de vous référez à 
la page [About](https://share.streamlit.io/matfrancois/4subjectsform/main/Home.py/About).

---
''')

# A quel point vous considérez vous sensible à la question climatique ?
rep2 = col.radio("A quel point vous considérez vous sensible à la question climatique ?", 
            ('Indifférent', 'Peu sensisble', 'Neutre', 'Sensible', 'Très sensible'), horizontal=True)


# Voter pour un parti à tendance écologiste
rep3 = col.radio("Vous considérez vous comme quelqu'un d'écologique", ('Oui', 'Non'))
if rep3 == 'Non':
    with col.expander("Cochez les raisons qui font que vous ne vous considérez pas comme quelqu'un d'écologique", expanded=True): 
        rep3_2 = st.checkbox("Raisons financières", value=False)
        rep3_3 = st.checkbox("Manque d'intérêts", value=False)
        rep3_4 = st.checkbox("Manque de connaissances", value=False)
        rep3_5 = st.checkbox("Manque d'impact", value=False)
        rep3_6 = st.checkbox("Je ne me sens pas concerné", value=False)
        rep3_7 = st.checkbox("Autre", value=False)
        rep3_8 = st.text_input('Autre', '') if rep3_7 else None
else:
    rep3_2, rep3_3, rep3_4, rep3_5, rep3_6, rep3_7, rep3_8 =  None, None, None, None, None, None, None

    
rep4 = col.radio("Considérez vous votre vote comme d'écologique", ('Oui', 'Non'))
rep5, rep4bis = col.select_slider(
    'Où placez vous votre vote ?',
    options=['Radical gauche', 'Gauche', 'Centre-gauche', 'Centre', 'Centre-droite', 'Droite', 'Radical droite'],
    value=('Centre-gauche', 'Centre-droite'))

col.markdown('''---
**Sur une échelle de 1 à 6 (1 = Ce discours est impensable, 3 = Sans opinion, 5 = Ce discours est une évidence) notez les phrases suivantes**
''')

# rajouter des phrases de climatosceptiques ?

rep6 = col.slider("La croissance verte est une chimaire, nous devons décroitre", 1, 5, 3)

rep7 = col.slider("Nous ne devrions plus prendre l'avion", 1, 5, 3) 

rep8 = col.slider("Devenir végétarien est une nécessité", 1, 5, 3) 

rep9 = col.slider("Il faut limiter l'expansion démographique", 1, 5, 3) 

## ajouter les autres questions présentent dans le doc

col.markdown('''---''')
rep18 = col.radio("Connaissez vous le GIEC ?", ('Oui', 'Non')) 
if rep18 == 'Non': 
    with col.expander('En savoir plus sur le GIEC', expanded=False): 
        st.markdown('''
        Depuis plus de 30 ans, le GIEC (Groupe d'experts intergouvernemental sur l'évolution du climat) 
        évalue l’état des connaissances sur l’évolution du climat, ses causes, ses impacts. Il identifie
        également les possibilités de limiter l’ampleur du réchauffement et la gravité de ses impacts et de 
        s’adapter aux changements attendus. Les rapports du GIEC fournissent un état des lieux régulier 
        des connaissances les plus avancées. Cette production scientifique est au cœur des négociations 
        internationales sur le climat. Elle est aussi fondamentale pour alerter les décideurs et la société 
        civile. En France, de nombreuses équipes de recherche travaillent sur ces sujets, impliquant plusieurs 
        centaines de scientifiques. Certains d’entre eux contribuent à différentes phases d’élaboration des rapports du GIEC.   
        
        [Comprendre le GIEC](https://www.ecologie.gouv.fr/comprendre-giec)
        
        Il y a aujourd'hui 3 groupes de travail :
        - le groupe n°1 étudie les aspects scientifiques du changement climatique
        - le groupe n°2 étudie les conséquences, la vulnérabilité et l'adaptation, pour les systèmes socio-économiques comme pour les systèmes naturels 
        - le groupe n°3 étudie l'atténuation du changement climatique
        Chacun d'eux a publié des rapports sur le sujet.
    ''')
rep19 = col.radio("Selon vous, les conclusions du GIEC indiquent elles que le réchauffement climatique est une urgence ?", ('Oui', 'Non')) 

rep20 = col.radio("Pensez vous que les accords de Paris et les rapports du GIEC sont-ils inutiles ?", ('Oui', 'Non')) 

rep21 = col.radio("La guerre en Ukraine, la crise du covid ont elles modifié votre vision sur l'écologie ?", ('Oui', 'Non')) 

submitted = col.button("Submit & go to annotation")

if submitted:
    mydict = {
        'time': id_session,
        "rep2": rep2,
        'rep3': [rep3, rep3_2, rep3_3, rep3_4, rep3_5, rep3_6, rep3_7, rep3_8],
        'rep4': [rep4, rep4bis],
        "rep4": rep4,
        "rep4bis": rep4bis,
        "rep5": rep5,
        "rep6": rep6,
        "rep7": rep7,
        "rep8": rep8,
        "rep9": rep9,
        "rep18": rep18,
        "rep18": rep18,
        "rep19": rep19,
        "rep20": rep20,
        "rep21": rep21,
    }

    collection.insert_one(mydict)
    webbrowser.open('https://share.streamlit.io/matfrancois/4subjectsform/main/Home.py/Annotation')
    print('done')

# viande
'''indicateur fenetre overton / discours sur la viande sur les réseaux sociaux'''

# avion
'''indicateur fenetre overton / discours sur l'avion sur les réseaux sociaux'''

# nucléaire
'''indicateur fenetre overton / discours sur le nucléaire sur les réseaux sociaux'''

# croissance verte 
'''indicateur fenetre overton / discours sur la croissance verte  sur les réseaux sociaux'''

