import streamlit as st
st.set_page_config(
     page_title="About",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
 )
st.markdown('''
# Qui sommes nous ? 

L'équipe GreenAIUppa de l'Université de Pau et des Pays de l'Adour est un laboratoire engagé qui améliore 
les algorithmes d'apprentissage automatique de pointe. Soucieux de notre impact sur la planète, nous 
développons des algorithmes à faible consommation d'énergie et relevons les défis environnementaux. 
Contrairement à d'autres groupes de recherche, nos activités sont dédiées à l'ensemble du pipeline, 
depuis les bases mathématiques jusqu'au prototype de R&D et au déploiement en production avec des partenaires 
industriels. Nous sommes basés à Pau, en France, en face des Pyrénées.         

<center>
    <img src="https://miro.medium.com/max/700/0*X36NgC4u0VJBQwF6.png"  alt="centered image" style="text-align: center;">
</center>

[Visiter notre page](https://greenai-uppa.github.io/) 

Nous contacter : [Matthieu François](mailto:matthieu.francois@yahoo.fr)
''', unsafe_allow_html=True)