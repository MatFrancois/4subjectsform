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
    rep3 = st.radio("Vous considérez vous comme quelqu'un d'écologique", ('Oui', 'Non'))
    if rep3 == 'Non':
        rep3_1 = st.write("Cochez les raisons qui font que vous ne vous considérez pas comme quelqu'un d'écologique") 
        rep3_2 = st.checkbox("Raisons financières", value=False)
        rep3_3 = st.checkbox("Manque d'intérêts", value=False)
        rep3_4 = st.checkbox("Manque de connaissances", value=False)
        rep3_5 = st.checkbox("Manque d'impact", value=False)
        rep3_6 = st.checkbox("Je ne me sens pas concerné", value=False)
        rep3_7 = st.checkbox("Autre", value=False)
        rep3_8 = st.text_input('Autre', '') if rep3_7 else None
    else:
        rep3_1, rep3_2, rep3_3, rep3_4, rep3_5, rep3_6, rep3_7, rep3_8 = None, None, None, None, None, None, None, None

        
    rep4 = st.radio("Considérez vous votre vote comme d'écologique", ('Oui', 'Non'))
    rep5, rep4bis = st.select_slider(
        'Où placez vous votre vote ?',
        options=['Radical gauche', 'Gauche', 'Centre-gauche', 'Centre', 'Centre-droite', 'Droite', 'Radical droite'],
        value=('Centre-gauche', 'Centre-droite'))

    st.write('Sur une échelle de 1 à 6 (1 = Ce discours est impenssable, 5 = Ce discours est une évidence) notez les phrases suivantes :')    

    rep6 = st.slider("Il faudrait payer des impôts supplémentaires pour favoriser l'écologie", 1, 5, 3)

    rep7 = st.slider("Cela vaut le coup d'investir dans l'éolien pour lutter contre le changement climatique. (ou le nucléaire)", 1, 5, 3)

    rep8 = st.slider("Il faudrait calculer son bilan carbone et l'utiliser pour orienter son mode de vie", 1, 5, 3)

    rep9 = st.slider("Nous ne devrions plus avoir de voiture (en ville), et des petites voitures en campagne.", 1, 5, 3) 

    rep10 = st.slider("Acheter une voiture électrique afin de lutter contre le changement climatique", 1, 5, 3) # ????

    rep11 = st.slider("Nous ne devrions plus prendre l'avion", 1, 5, 3) 

    rep12 = st.slider("Il faudrait devenir végétarien", 1, 5, 3) 

    rep13 = st.slider("Nous devrions diminuer la vitesse maximale autorisée sur les autoroutes", 1, 5, 3) 

    rep14 = st.slider("Nous devrions intégrer le télétravail dans la loi du travail", 1, 5, 3) 

    rep15 = st.slider("Nous devrions favoriser les produits reconditionnés", 1, 5, 3) 

    rep16 = st.slider("Nous devrions baisser la température de l'eau au quotidien (lave-vaisselle, lave-linge, douche, bain ... )", 1, 5, 3) 

    rep17 = st.slider("Il faudrait limiter l'utilisation des services de streaming (Netflix, Prime etc)", 1, 5, 3) 

#info GIEC

    rep18 = st.radio("Connaissez vous le GIEC ?", ('Oui', 'Non')) 
    if rep18: 
        '''
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
        '''
    rep19 = st.radio("Selon vous, les conclusions du GIEC indiquent elles que le réchauffement climatique est une urgence ?", ('Oui', 'Non')) 

    rep20 = st.radio("Pensez vous que les accords de Paris et les rapports du GIEC sont-ils inutiles ?", ('Oui', 'Non')) 

    rep21 = st.radio("La guerre en Ukraine, la crise du covid ont elles modifié votre vision sur l'écologie ?", ('Oui', 'Non')) 

    submitted = st.form_submit_button("Submit")
    
    if submitted:
        mydict = {
            "rep1": rep1,
            "rep2": rep2,
            'rep3': [rep3, rep3_1, rep3_2, rep3_3, rep3_4, rep3_5, rep3_6, rep3_7, rep3_8],
            'rep4': [rep4, rep4bis],
            "rep4": rep4,
            "rep4bis": rep4bis,
            "rep5": rep5,
            "rep6": rep6,
            "rep7": rep7,
            "rep8": rep8,
            "rep9": rep9,
            "rep10": rep10,
            "rep11": rep11,
            "rep12": rep12,
            "rep13": rep13,
            "rep14": rep14,
            "rep15": rep15,
            "rep16": rep16,
            "rep17": rep17,
            "rep18": rep18,
            "rep18": rep18,
            "rep19": rep19,
            "rep20": rep20,
            "rep21": rep21,
        }

        collection.insert_one(mydict)
        print('done')

    
    

    # viande
    '''indicateur fenetre overton / discours sur la viande sur les réseaux sociaux'''
    
    # avion
    '''indicateur fenetre overton / discours sur l'avion sur les réseaux sociaux'''
    
    # nucléaire
    '''indicateur fenetre overton / discours sur le nucléaire sur les réseaux sociaux'''
    
    # croissance verte 
    '''indicateur fenetre overton / discours sur la croissance verte  sur les réseaux sociaux'''

