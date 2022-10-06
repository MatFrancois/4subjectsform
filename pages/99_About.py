import streamlit as st
st.set_page_config(
     page_title="About",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
 )
st.markdown('''
# La fenêtre D'overton
> aussi connue commme la fenêtre de discours, c'est une allégorie qui situe l'ensemble des idées, opinions ou pratiques considérées comme plus ou moins acceptables dans l'opinion publique d'une société.
Elle possède 5 niveaux :
- _Politique publique_ : L'idée est défendue par la politique publique ou trouve des représentants pour concevoir des projets de loi.
- _Populaire_ : L'idée s'implante culturellement et est intégrée dans des films, musiques, journaux etc.
- _Raisonnable_ : L'idée se justifie (scientifiquement par exemple) et se légitime dans la population.
- _Acceptable_ : L'idée progresse dans le débat publique.
- _Radical_ : Le sujet est exploré par la science (exacte ou non).
- _Impensable_ : L'idée est jugée immorale, elle ou son application est punie par la loi.
''')

st.markdown('''Cette page vous propose d'explorer cette fenêtre sur Twitter et d'aider notre équipe à construire un corpus académique sur ce sujet.''')

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

Nous contacter : [Matthieu François](mailto:matthieu.francois@univ-pau.fr)
''', unsafe_allow_html=True)
