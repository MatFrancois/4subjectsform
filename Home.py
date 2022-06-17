import streamlit as st
# import pymongo
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
#@st.experimental_singleton
#def init_connection():
#    address = st.secrets["mongo"].get('client')
#    return pymongo.MongoClient(address)['green']["4subjects_form"]

#collection = init_connection()

@st.cache(allow_output_mutation=True)
def get_unique_id():
    return str(time.time())
#  ====================================================  
id_session = get_unique_id()

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
col.markdown('''---
**Qu'est ce que la fenêtre d'Overton ?**

> Aussi connue comme la fenêtre de discours, est une allégorie qui situe l'ensemble des idées, opinions ou pratiques considérées comme plus ou moins acceptables dans l'opinion publique d'une société. 

**Que puis-je trouver ici ?**
- Un questionnaire (ci dessous), permettant de mieux comprendre la perception de certains sujets lié à l'écologie et leur évolution dans le temps.
- Une page d'[annotation](https://share.streamlit.io/matfrancois/4subjectsform/main/Home.py/Annotation) permettant de comparer sa perception d'un message avec celle d'un modèle entrainé par nos soins
- Une page proposant les résultats de nos modèles de NLP proposant des individus classés selon la fenêtre d'Overton et renvoyant vers la page d'annotation.

Add graphics
             
### Collecte d'opinion concernant plusieurs discours de société
---
On vous invite à répondre aux questions suivantes toutes liées à l'écologie, puis dans un second temps d'envoyer vos 
réponses à partir du boutton "Envoyer", en bas de la page. Sans ça, les valeurs par défaut 
risqueront d'être utilisées.

Merci de ne répondre qu'une seule fois au questionnaire.

Pour en savoir plus sur notre équipe ou pour nous contacter, merci de vous référez à 
la page [About](https://share.streamlit.io/matfrancois/4subjectsform/main/Home.py/About).

---
''')

idee = col.selectbox("Pour plus de détails sur les niveaux dans la fenêtre d'Overton, sélectionner un niveau.", ['Politique publique', 'Populaire', 'Raisonnable', 'Acceptable', 'Radical', 'Impensable'])
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

# # A quel point vous considérez vous sensible à la question climatique ?
# rep2 = col.radio("A quel point vous considérez vous sensible à la question du changement climatique ?", 
#             ('Indifférent', 'Peu sensisble', 'Neutre', 'Sensible', 'Très sensible'), horizontal=True)


# # Voter pour un parti à tendance écologiste
# rep3 = col.radio("Vous considérez vous comme écolo ?", ('Oui', 'Non'))
# if rep3 == 'Non':
#     with col.expander("Si non, quelles en sont les raisons ?", expanded=True): #qui font que vous ne vous considérez pas comme quelqu'un d'écologique
#         rep3_2 = st.checkbox("Raisons financières", value=False)
#         rep3_3 = st.checkbox("Manque d'intérêts", value=False)
#         rep3_4 = st.checkbox("Manque de connaissances", value=False)
#         rep3_5 = st.checkbox("Manque d'impact", value=False)
#         rep3_6 = st.checkbox("Je ne me sens pas concerné", value=False)
#         rep3_7 = st.checkbox("Autre", value=False)
#         rep3_8 = st.text_input('Autre', '') if rep3_7 else None
# else:
#     rep3_2, rep3_3, rep3_4, rep3_5, rep3_6, rep3_7, rep3_8 =  None, None, None, None, None, None, None

# rep4 = col.radio("Considérez vous votre vote comme oritenté vers l'écologie", ('Oui', 'Non'))
# rep5, rep4bis = col.select_slider(
#     'Où placez vous votre vote ?',
#     options=['Radical gauche', 'Gauche', 'Centre-gauche', 'Centre', 'Centre-droite', 'Droite', 'Radical droite'],
#     value=('Centre-gauche', 'Centre-droite'))

col.markdown('''---
**Comment considérez vous les phrases suivantes ?**
''')

# rajouter des phrases de climatosceptiques ?

rep6 = col.radio(
    "La croissance verte est nécessaire pour l'avenir.",
    modalities,
    horizontal=True
)
col.markdown('Voici la définition de croissance verte selon [OECD](https://www.oecd.org/fr/croissanceverte/quest-cequelacroissanceverteetcommentpeut-elleaideraassurerundeveloppementdurable.htm).') 
col.info('La **croissance verte** signifie *promouvoir la croissance économique et le développement* tout en veillant à ce que les actifs naturels continuent de fournir les ressources et services environnementaux dont dépend notre bien-être.')

rep7 = col.radio(
    "Nous ne devrions plus prendre l'avion.",
    modalities,
    horizontal=True
) 

rep8 = col.radio(
    "Diminuer sa consommation de viande voire la stopper est une nécessité écologique ou envionnementale.",
    modalities,
    horizontal=True
) 

rep9 = col.radio(
    "Le nucléaire est la solution à la transition écologique.",
    modalities,
    horizontal=True
) 

## ajouter les autres questions présentent dans le doc

col.markdown('''---''')
# rep18 = col.radio("Connaissez vous le GIEC ?", ('Oui', 'Non')) 
# if rep18 == 'Non': 
#     with col.expander('En savoir plus sur le GIEC :', expanded=False): 
#         st.markdown('''
#         Depuis plus de 30 ans, le GIEC (Groupe d'experts intergouvernemental sur l'évolution du climat) 
#         évalue l’état des connaissances sur l’évolution du climat, ses causes, ses impacts. Il identifie
#         également les possibilités de limiter l’ampleur du réchauffement et la gravité de ses impacts et de 
#         s’adapter aux changements attendus. Les rapports du GIEC fournissent un état des lieux régulier 
#         des connaissances les plus avancées. Cette production scientifique est au cœur des négociations 
#         internationales sur le climat. Elle est aussi fondamentale pour alerter les décideurs et la société 
#         civile. En France, de nombreuses équipes de recherche travaillent sur ces sujets, impliquant plusieurs 
#         centaines de scientifiques. Certains d’entre eux contribuent à différentes phases d’élaboration des rapports du GIEC.   
        
#         [Comprendre le GIEC](https://www.ecologie.gouv.fr/comprendre-giec)
        
#         Il y a aujourd'hui 3 groupes de travail :
#         - le groupe n°1 étudie les aspects scientifiques du changement climatique
#         - le groupe n°2 étudie les conséquences, la vulnérabilité et l'adaptation, pour les systèmes socio-économiques comme pour les systèmes naturels 
#         - le groupe n°3 étudie l'atténuation du changement climatique
#         Chacun d'eux a publié des rapports sur le sujet.
#     ''')
# rep19 = col.radio("Selon vous, les conclusions du GIEC indiquent elles que le réchauffement climatique est une urgence ?", ('Oui', 'Non')) 

# rep20 = col.radio("Pensez vous que les accords de Paris et les rapports du GIEC sont-ils utiles?", ('Oui', 'Non')) 

# rep21 = col.radio("La guerre en Ukraine, la crise du Covid-19 ont elles modifié votre vision sur l'écologie ?", ('Oui', 'Non')) 

submitted = col.button("Soumettre & Annoter")

# création du json de réponses
if submitted:
    mydict = {
        'time': id_session,
        # "rep2": rep2,
        # 'rep3': [rep3, rep3_2, rep3_3, rep3_4, rep3_5, rep3_6, rep3_7, rep3_8],
        # 'rep4': [rep4, rep4bis],
        # "rep4": rep4,
        # "rep4bis": rep4bis,
        # "rep5": rep5,
        "rep6": rep6,
        "rep7": rep7,
        "rep8": rep8,
        "rep9": rep9,
        # "rep18": rep18,
        # "rep18": rep18,
        # "rep19": rep19,
        # "rep20": rep20,
        # "rep21": rep21,
    }

    # envoie des données et redirection vers la page d'annotations
    # collection.insert_one(mydict)
    webbrowser.open('https://share.streamlit.io/matfrancois/4subjectsform/main/Home.py/Annotation')
    print('done')


