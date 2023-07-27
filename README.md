# OC_Project7
## Projet OpenClassroom parcours Data Scientist

### Description du projet
L'organisme de prêt "Prêt à dépenser" souhaite mettre en place une interface à destination des conseillers clientèle, afin de les aider à décider d'accorder ou non un prêt à un client donné.  
Dans cette perspective, il s'agit de mettre en place un modèle de scoring permettant de décider, en fonction des informations connues du client, s'il existe un risque suffisamment fort d'insolvabilité pour refuser le prêt.  
Il doit être tenu compte du fait que le coût d'un prêt accordé à un "mauvais payeur" est significativement plus grand (10 fois) que le coût d'un prêt refusé à un "bon payeur".  
Afin d'élaborer ce modèle de scoring, un dataset rassemblant des informations de plus de 300 000 clients est mis à disposition. 122 indicateurs sont plus ou moins renseignés selon les clients et l'information du défaut de paiement est connue. Les clients ayant été en défaut de paiement sont nettement moins nombreux, ils représentent environ 8% de l'ensemble des clients.  
Une fois le modèle défini, il s'agit de l'appeler depuis une API (back-end) qui doit renvoyer au conseiller clientèle l'ensemble des informations dont il a besoin pour prendre une décision et l'expliquer.  
Il a accès à une application (front-end) qui ne contient pas de modèle enregistré ni d'information relative aux clients références ou nouveaux, seules des requêtes API permettent d'obtenir les informations strictement nécessaires. Les informations des nouveaux clients (50 000) sont contenues dans un autre dataset, on considère que ces informations préremplies ont été communiquées au préalable via un questionnaire ou une enquête.
Enfin, le déploiement sur le web des deux applications doit se faire dans un cadre permettant une intégration et amélioration continues.

### Analyse exploratoire et feature engineering
L'analyse exploratoire permet déjà de faire apparaître des indicateurs plus ou moins importants, lorsque l'on regarde les corrélations avec les défauts de paiement notamment.
Etapes du nettoyage et du feature engineering :
- suppression des features inconnues pour plus de 60% des clients références --> réduction à 70 features
- suppression des outilers en "applatissant" entre 1er quartile - 1,5*(écart interquartile) et 3ème quartile + 1,5*(écart interquartile)
- complétion des valeurs inconnues en remplaçant par la moyenne pour les features numériques et par le mode pour les features catégorielles
- LabelEncoding des features catégorielles dans le cadre de la préparation à la modélisation
- observation des corrélations après transformation

### Modélisation et MLFlow
Mise en place d'un processus de MLFlow pour enregistrer les expériences (modèles avec éventuels pipelines de transformations supplémentaires, paramètres et hyperparamètres, temps d'entraînement et de validation, différentes métriques de validations : AUC, Accuracy etc.) au travers d'une fonction unique. Dans le cas présenté dans le Notebook, la mise en place du MLFlow est intervenue postérieurement à l'exploration et l'optimisaiton des modèles ; par conséquent, toutes les expériences n'ont pas été enregisrtées : une seule par modèle.
Choix de plusieurs modèles de classification :  
- DummyClassifier pour référence
- LogisticRegressor de SKLearn
- XGBoost
- LightGBM
- AdaBoost
Pour chacun d'eux, une à deux techniques de gestion du déséquilibre des données :
- SMOTE à chaque cross validation dans le cadre d'un pipeline, pour créer des nouveaux clients fictifs non solvables à partir de ceux connus avant l'optimisation des hyperparamètres des modèles avec RandomSearchCV
- pour XGBoost et LigthGBM, les techniques de "class_weight" ou équivalent, intégrées dans les paramètres des modèles
De même, pour chaque approche, l'optimisation du score AUC est d'abord recherchée, puis un nouveau score à minimser est créé, à partir des résultats obtenus pour chaque classe (avec la fonction de coût = 10*Faux positifs + Faux négatifs).  
Enfin, dans chaque cas, un calcul des prédictions sous forme de probabilité est réalisé afin de rechercher le meilleur seuil pour minimiser cette même fonction de coût.
Au regard de l'ensemble des métriques, y compris les temps, et en comparant les ROC curves, le meilleur modèle est retenu : le modèle LightGBM avec paramétrage "class_weight" (hyperparamètres dans le Notebook et dans les mlruns).
Un pipeline de transformation des features et de modélisation est recréé puis réentraîné et enfin enregistré avec Joblib.

### Explicabilité globale et locale
Pour l'explicabilité globale, les Shap values des features sont préférées à l'explicabilité propre du modèle (feature_importance_), en raison de sa plus grande stabilité.
S'agissant de l'explicabilité locale, la problématique réside dans le fait qu'en théorie, les nouveaux clients ne sont pas déjà connus. Ainsi, pour utiliser Shap, il faudrait recalculer systématiquement les Shap values sur le dataset d'entraînement, auquel on ajouterait le nouveau client, afin d'obtenir sa position. Cela nécessiterait un temps de calcul trop lourd pour une bonne expérience utilisateur. Par conséquent, la méthode Lime, qui permet de ne calculer l'explicabilité globale qu'une fois et d'effectuer l'explicabilité locale directement à partir de l'explainer obtenu est retenue pour l'application.

### Analyse du Data Drift

### Description du dossier API

### Description du dossier Streamlit

### Tests et workflow
