# Hackathon

![hkt.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/4e8c04dc-fc73-4d71-98b1-c9a775156b9a/39fd531e-09c6-49ea-a91f-9cfa4bf1375d/hkt.png)

<aside>
💡  **Ressources :**

- **Pour vous aider :**
    
    https://nbhosting.inria.fr/builds/ue12-p23-numerique/handouts/latest/_downloads/d7e00a6ac60d14256515f7c2cafd935b/cheatsheet-pandas.pdf
    
    https://images.datacamp.com/image/upload/v1676302389/Marketing/Blog/Scikit-Learn_Cheat_Sheet.pdf
    
</aside>

# Data : [120 years of Olympic history](https://1drv.ms/f/c/06c6d756296d4662/EmJGbSlW18YggAZIQw0AAAABmyzirqdnx4gmnY-C0VLeJw?e=mIhmgt)

- Les données ont été scrapées à partir de https://olympics.com/ et constituent l’historique des JO d’Athènes de 1896 à ceux de Pékin en 2022, aussi bien d’hiver que d’été.
- **4 Datasets :**
    - Médailles : + de 21 000
    - Résultats : + de 162 000
    - Athlètes : + de 74 000
    - Hôtes : 53 pays

# Langages et Technos à utiliser :

[]()

- **Langage** :
    
    [Welcome to Python.org](https://www.python.org/)
    
- **Base de données** :
    
    [Supabase | The Open Source Firebase Alternative](https://supabase.com/) (PostgreSQL)
    
    - Référence aux modules :
        1. Révision `SQL` 
        2. Conception et Intégration d’un Cluster de BD : `PostGres`
- **Exploration et Visualisation des données :**
    
    
    [pandas - Python Data Analysis Library](https://pandas.pydata.org/)
    
    [Plotly: Low-Code Data App Development](https://plotly.com/)
    
    - `Pandas` et `Plotly` est commun à tous ! ****
- **IA :**
    
    
    [scikit-learn: machine learning in Python — scikit-learn 1.4.2 documentation](https://scikit-learn.org/stable/)
    
    - Les M1 mettrons en place des modèles de `Machine Learning`.
- WebApp :
    
    
    [React – Une bibliothèque JavaScript pour créer des interfaces utilisateurs](https://fr.legacy.reactjs.org/)
    
    [JavaScript With Syntax For Types.](https://www.typescriptlang.org/)
    
    [Express - Node.js web application framework](https://expressjs.com/)
    

# Missions

## Créer dans l’art la base des données des JO :

- Un membre du groupe (de préf. en M1) prendra la casquette d’un DBA (DataBase Adminstrator), mettra en production la BD et accordera les accès aux autres membres de son groupe en gérant les privilèges (`root`, `read only`, …) :
    - Sur **Supabase** (PostgreSQL).
    - En veillant :
        - au bon typage des colonnes
        - Clés primaires et étrangères
        - Contraintes d’unicité
        - …
        - Voir modules M1 : Révision SQL et Conception et Intégration Cluster MariaDB et PostGres

## Explorer et visualiser les données :

- Produire un `notebook` où :
    - Vous vous connectez avec `Python-Pandas` à la BD
    - Vous confirmez (ou non) les évènements marquants suivants en accompagnant votre réponse avec du `code` et la visualisation appropriée (lorsque c’est possible) :
    - Evènements marquants aux JO :
        1. La France a organisé 6 JO : 3 d’hiver et 3 d’été (en comptant celui de 2024) ?
        2. La France est le 2è pays qui a organisé le plus de JO après les USA (8 JO) ?
        3. Les JO d’hiver sont nés à Chamonix en 1924 ?
        4. JO de Paris, en 1900 : les femmes peuvent participer aux JO ?
        5. Seuls 4 athlètes ont remporté des médailles à la fois aux JO d’hiver et d’été. Une seule d’entre eux, Christa Ludinger-Rothenburger, a remporté des médailles au cours de la même année ?
        6. De 1924 à 1992, les JO d’hiver et d’été avaient lieu au cours de la même année. Désormais, ils sont organisés selon des cycles distincts avec une alternance de 2 ans ?
        7. Tarzan lui-même a participé aux JO. En effet, Johnny Weissmuller, ancien athlète devenu acteur et ayant interprété 12 films de Tarzan, a remporté 5 médailles d’or en natation dans les années 1920 ?
        8. Les JO de Londres de 2012 ont été les 1ers JO durant lesquels tous les pays participants ont envoyé des athlètes de sexe féminin ?
        9. Les sports suivants ne font (malheureusement) plus partie des J.O : la natation synchronisée en solo, le tir à la corde, la corde à grimper, la montgolfière, le duel au pistolet, le vélo tandem, la course d’obstacles à la nage et le plongeon à distance. Par chance, le tir au pigeon n’a été mis en place qu’une seule fois pendant les Jeux Olympiques de Paris de 1900 ? 
        10. Les Jeux de 2016, à Rio, marqueront la 1è manifestation des JO en Amérique du Sud ? 
        11. Pendant les 17 jours des JO d’été de 2016, 10 500 athlètes, originaires de 205 pays, représenteront 42 sports différents et participeront à 306 épreuves, à Rio ?
    - Questions ouvertes :
        1. Combien de médailles la France a remporté : en tout, en Or, en argent et en Bronze (depuis le début des JO) ?
        2. Lors de quelle JO la France a eu le plus (le moins) de succès ?
        3. Peut-on considérer que la France est la grande spécialiste de certaine(s) discipline(s) sportive(s), comparativement aux autres notions ? Laquelle / Lesquelles ?
        4. Quelles sont les sports les plus dominants dans les JO au fil des ans ?
    - Question Bonus :
        1. Y a-t-il une corrélation entre le nombre de médailles remportées et des facteurs économiques tel que le montant du Produit Intérieur Brut (PIB) ? Pour cela, vous pouvez `scraper` le tableau présent sur la page Web ci-dessus et avancez votre analyse ? Le tableau est spécifique à 2020. Vous pouvez avancer sur 2021-2022-2023. 
        
        [GDP Indicators 2020 - StatisticsTimes.com](https://statisticstimes.com/economy/gdp-indicators-2020.php)
        

## Retenir les IA les plus performantes pour :

- Prédire les résultats des JO Paris 2024 :
    - Nombre de médaille d’Or, d’Argent et de Bronze qui seront gagné par la France ?
    - Le nombre de médaille d’Or, d’Argent et de Bronze qui seront gagné par le Top 25 des pays participants ?
    - Prédire les athlètes qui vont remporter des médailles ?
    
    <aside>
    📢 Très important : vous pouvez faire du `Web Scraping` pour récupérer des données à partir de sites spécifiques ET/OU télécharger de l’`Open data` le tout dans l’objectif d’avoir des données additionnelles qui peuvent améliorer la précision de vos IA
    
    </aside>
    
- Clustering
    - Sans être un expert des JO, votre objectif est de classer les pays en k classes (k à trouver ?) au sein desquelles les pays sont le plus semblables en termes de performance ?
- N’oublier pas :
    - d’entraîner / expérimenter au moins 3 modèles : de `Machine Learning`
    - d’optimiser la performance de différents modèles (`Kmeans`, `Decision Tree`, `RondomForest`, `Support Vector Machine`, `CNN`, …) en se basant sur les métriques
    adéquates (`elbow method`, `confusion matrix`, `accuracy`, …) et en ajustant les hyperparamètres en utilisant des techniques telles que le `GridSearch`
    - **Note :** L'entraînement des modèles se fera sur **Kaggle**, le modèle entraîné sera ensuite importé dans le projet.

# WebApp :

- L’objectif est de mettre en place un site qui ressemble **en termes de fonctionnalités** à celui-ci :
    
    [Olympics - Visualization & Prediction](https://diannejardinez.github.io/Olympic_Data_machine_learning/Flask-API/templates/data.html)
    

- Où nous pouvons trouver dessus dessus des analyses, des viz interactives (éventuellement des gif animés) et la prédiction
- Le design du site web est laissé complètement libre. Néanmoins, il faudra que le site soit consultable aussi bien sur un ordinateur que sur mobile (téléphone mobile, tablette, phablette…).
- Il faut que les URL de page permettent une compréhension rapide de ce que la page représente !
- Respecter les bonnes pratiques de code !

# IA Livrable attendu :

- Un repo Github où on trouve :
    - Un fichier README où vous expliquez :
        - Comment lancer les scripts ?
        - Mentionnez le lien de votre trello avec la répartition des tâches à travers les
        membres de votre groupe (à faire/en cours/fait)
        - …
        - L’URL de la WebApp mise en ligne
        - Lien vers le support de présentation (par exemple google slides)
    - Un notebook (non cleané pour comprendre votre démarche)
        - Les problèmes rencontrés sur le jeu de données
        - Comment vous avez nettoyé les données ?
        - Votre modélisation (du preprocessing à la prédiction)
    - Le code générant la WebApp et permettant de déployer le modèle sous forme d’API
    - Un support de présentation (environ 10-15 slides)
        - La première slide doit inclure :
            - Votre numéro de groupe
            - Nom et prénom des membres du groupe
            - Le logo de l’école
            - Un titre bref de la présentation de votre projet

# Modalités de présentation du travail :

- Votre présentation pourra prendre cette forme (à titre indicatif) :
    
    
    | 5 min | Rappel de la problématique, présentation du jeu de données, de l’exploration, du cleaning, … |
    | --- | --- |
    | 15 min | Explication de votre approche pour mettre en place votre solution (méthodo, code, interprétation des résultats, modèle final sélectionné ainsi que les
    améliorations effectuées pour augmenter les performances, … ?) ET Démo |
    | 10 min | Séance de questions-réponses |

# Ressources :
https://www.nielsen.com/fr/news-center/2022/nielsen-gracenote-releases-final-virtual-medal-table-forecast/
https://fonseca-carlos.medium.com/predicting-tokyo-2020-total-medal-count-f808e80e4406
https://s03.s3c.es/imag/doc/2016-08-01/olympic-games-report-goldman-sachs.pdf
https://towardsdatascience.com/going-for-gold-predicting-medal-outcomes-in-the-olympics-using-generalized-linear-modeling-e6e9d4837ae8