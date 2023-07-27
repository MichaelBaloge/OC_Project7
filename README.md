# OC_Project7
## Projet OpenClassroom parcours Data Scientist

### Description du projet
L'organisme de prêt "Prêt à dépenser" souhaite mettre en place une interface à destination des conseillers clientèle, afin de les aider à décider d'accorder ou non un prêt à un client donné.  
Dans cette perspective, il s'agit de mettre en place **un modèle de scoring** permettant de décider, en fonction des informations connues du client, s'il existe un risque suffisamment fort d'insolvabilité pour refuser le prêt.  
Il doit être tenu compte du fait que le coût d'un prêt accordé à un "mauvais payeur" est significativement plus grand (10 fois) que le coût d'un prêt refusé à un "bon payeur".  
Afin d'élaborer ce modèle de scoring, un dataset rassemblant des informations de plus de 300 000 clients est mis à disposition. 122 indicateurs sont plus ou moins renseignés selon les clients et l'information du défaut de paiement est connue. Les clients ayant été en défaut de paiement sont nettement moins nombreux, ils représentent environ 8% de l'ensemble des clients.  
Une fois le modèle défini, il s'agit de l'appeler depuis **une API (back-end)** qui doit renvoyer au conseiller clientèle l'ensemble des informations dont il a besoin pour **prendre une décision et l'expliquer**.  
Il a accès à **une application (front-end)** qui ne contient pas de modèle enregistré ni d'information relative aux clients références ou nouveaux, seules des requêtes API permettent d'obtenir les informations strictement nécessaires. Les informations des nouveaux clients (50 000) sont contenues dans un autre dataset, on considère que ces informations préremplies ont été communiquées au préalable via un questionnaire ou une enquête.
Enfin, le déploiement sur le web des deux applications doit se faire dans un cadre permettant une intégration et amélioration continues.

### Analyse exploratoire et feature engineering
L'analyse exploratoire permet déjà de faire apparaître des indicateurs plus ou moins importants, lorsque l'on regarde les corrélations avec les défauts de paiement notamment.
Etapes du nettoyage et du feature engineering :
- suppression des features inconnues pour plus de 60% des clients références --> **réduction à 70 features**
- **suppression des outilers** en "applatissant" entre 1er quartile - 1,5*(écart interquartile) et 3ème quartile + 1,5*(écart interquartile)
- **complétion des valeurs inconnues** en remplaçant par la moyenne pour les features numériques et par le mode pour les features catégorielles
- **LabelEncoding** des features catégorielles dans le cadre de la préparation à la modélisation
- **observation des corrélations** après transformation

### Modélisation et MLFlow
Mise en place d'un processus de MLFlow pour **enregistrer les expériences** (modèles avec éventuels pipelines de transformations supplémentaires, paramètres et hyperparamètres, temps d'entraînement et de validation, différentes métriques de validations : AUC, Accuracy etc.) au travers d'une fonction unique. Dans le cas présenté dans le Notebook, la mise en place du MLFlow est intervenue postérieurement à l'exploration et l'optimisaiton des modèles ; par conséquent, toutes les expériences n'ont pas été enregisrtées : une seule par modèle.
Choix de plusieurs **modèles de classification** :  
- **DummyClassifier** pour référence
- **LogisticRegresso**r de SKLearn
- **XGBoost**
- **LightGBM**
- **AdaBoost**
Pour chacun d'eux, une à deux techniques de **gestion du déséquilibre des données** :
- **SMOTE à chaque cross validation dans le cadre d'un pipeline**, pour créer des nouveaux clients fictifs non solvables à partir de ceux connus avant l'optimisation des hyperparamètres des modèles avec **RandomSearchCV**
- pour XGBoost et LigthGBM, les techniques de **"class_weight" ou équivalent**, intégrées dans les paramètres des modèles, permettant de gérer le déséquilibre

De même, pour chaque approche, **l'optimisation du score AUC** est d'abord recherchée, puis **un nouveau score à minimser est créé**, à partir des résultats obtenus pour chaque classe avec la **fonction de coût = 10*Faux positifs + Faux négatifs**.
Enfin, dans chaque cas, un calcul des **prédictions sous forme de probabilité** est réalisé afin de rechercher **le meilleur seuil pour minimiser cette même fonction de coût**.
Au regard de l'ensemble des métriques, y compris les temps, et en comparant les ROC curves, le meilleur modèle est retenu : le modèle LightGBM avec paramétrage "class_weight" (hyperparamètres dans le Notebook et dans les mlruns).
Un pipeline de transformation des features et de modélisation est recréé puis réentraîné et enfin enregistré avec Joblib.

### Explicabilité globale et locale
Pour **l'explicabilité globale, les Shap values des features** sont préférées à l'explicabilité propre du modèle (feature_importance_), en raison de sa plus grande stabilité.
S'agissant de **l'explicabilité locale**, la problématique réside dans le fait qu'en théorie, les nouveaux clients ne sont pas déjà connus. Ainsi, pour utiliser Shap, il faudrait recalculer systématiquement les Shap values sur le dataset d'entraînement, auquel on ajouterait le nouveau client, afin d'obtenir sa position. Cela nécessiterait un temps de calcul trop lourd pour une bonne expérience utilisateur. Par conséquent, **la méthode Lime**, qui permet de ne calculer l'explicabilité globale qu'une fois et d'effectuer l'explicabilité locale directement à partir de l'explainer obtenu est retenue pour l'application.

### Analyse du Data Drift
Avec la librairie Evidency, le drift peut être mesuré pour **évaluer la pertinence du modèle dans le temps**. Cette analyse peut être effectuée à chaque fois qu'on enregistre un certain nombre de nouveaux clients (nombre ou période à déterminer). Ici on effectue l'analyse sur les données connues des 50 000 nouveaux clients que l'on compare aux 300 000 initiaux (références).  
Malgré une modification légèrement significative de la distribution des nouveaux clients comparée à celle des clients références pour 9 indicateurs, le score du drift reste très faible et l'on peut considérer qu'il n'y a pas de Data Drift dans notre cas présent, comme le montre le rapport, donc **pas besoin de chercher un nouveau modèle à entraîner**. On peut le "vérifier" intuitivement en regardant le "rang" des features concernées dans l'explicabilité globale.  
A noter que dans notre cas, compte tenu du fait que la modélisation est effectuée sur 70 indicateurs, on a réduit les données comparées à ces indicateurs (il n'y a pas non plus de drift lorsque l'on les conserve tous (voir le deuxième rapport).

### Description du dossier API
Le choix a été fait de construire une **API Flask**.  
En plus du dossier (fichier Yaml) de workflows, décrivant les différentes tâches à effectuer, 7 fichiers sont nécessaires :
- **le script python de l'API** détaillé plus bas
- **les deux datasets** contenant respectivement les informations des clients références et celles des nouveaux clients. Ces datasets sont amenés à changer avec le temps et ne seront modifiés qu'ici.
- **le fichier png contenant l'image de l'explicabilité globale Shap**
- **le fichier joblib dans lequel le modèle entraîné est enregistré**. Si le modèle change, le fichier sera changé.
- **le fichier requirements.txt contenant les librairies nécessaires** à contruire l'environnement dans lequel l'API peut fonctionner (à modifier en cas d'utilisation de nouveaux modèles de références par exemple).
- **un fichier startup.sh, que la plateforme d'hébergement est forcée à lancer au démarrage** de l'application (configuration personnalisée sur l'hébergeur). Ce fichier est nécessaire car il oblige à installer un module supplémentaire nécessaire au fonctionnement du modèle, et que l'hébergeur ne reconnaît pas naturellement.

Concernant le script de l'API,** 7 "routes" sont mises en place** pour interagir avec l'utilisateur de l'application (interface du conseiller clientèle).
**Trois méthodes GET** pour obtenir :
- la liste des ids des nouveaux clients pour vérifier que le client est bien enregistré
- la liste des features qui sont utilisées pour la modélisation. Si jamais le modèle devait être revu, cette liste pourrait être amenée à évoluer sans pour autant affecter le script de l'interface utilisateur.
- l'image de l'explicabilté globale
**Quatre méthodes POST** pour :
- envoyer le numéro du client sélectionné et recevoir ses informations (données pour les indicateurs)
- envoyer le numéro du client sélectionné et recevoir la prédiction (probabilité d'insolvabilité, décision, explicabilité Lime)
- envoyer, pour un client sélectionné, des données modifiées pour certains indicateurs choisis par le conseiller clientèle, et recevoir la nouvelle prédiciton
- envoyer une liste d'indicateurs et recevoir les données des clients références pour ces indicateurs, ainsi que leur probabilité d'insolvabilité si on leur appliquait la modélisation.

### Description du dossier Streamlit
L'interface utilisateur est une application Streamlit.  
En plus du dossier (fichier Yaml) de workflows, décrivant les différentes tâches à effectuer, 3 fichiers seulement sont nécessaires :
- **le script de l'application** détaillé plus bas
- **le fichier png contenant le logo** de l'organisme de prêt avec l'intitulé de l'interface
- **le fichier des requirements** limités à l'application

Description de l'expérience utilisateur pour un client :
- le conseiller est invité à entrer le numéro d'un client et d'entrer pour vérifier que le client existe bien
- si tel est le cas, il est invité à valider le numéro client pour obtenir un certain nombre d'informations :
  - les données statiques du client
  - des menus de sélection pour afficher et éventuellement modifier ou compléter respectivement les informations renseignées et non renseignées
  - l'explicabilité globale (image png des features importances de Shap) et l'explicabilité locale (retour de l'API des features importances au sens de Lime pour le client)
  - des graphs montrant, pour 2 indicateurs par défaut (faisant le plus augmenter la probabilité d'insolvabilité pour le client) modifiables, la position du client au regard de sa probabilité au regard des clients références (nuage de points), et, selon la nature de l'indicateur choisi, deux boîtes à moustache ou histogrammes, après application du seuil de décision.
- l'utilisateur peut alors soit modifier (ou compléter) des informations concernant le client et obtenir les nouvelles prédictions (probabilité, décision et graphs montrant les positions initiales et nouvelles pour les indicateurs modifiés - nuages de points) si jamais ces modifications étaient validées
- il peut également sélectionner n'importe quel indicateur à afficher. A noter que si 2 sont sélectionnés, un cinquième graph s'affiche (en plus des 2*2) montrant la position du client vis à vis des deux indicateurs, en comparaison des clients références (nuage de points).

NB : l'explicabilité n'est pas toujours évidente, le conseiller doit être formé pour bien comprendre la valeur des indicateurs ainsi que le sens des graphiques (ils ne sont pas tous pertinents...) et savoir restituer l'explication de la décision. Une interrogation à ChatGPT pourrait par exemple être ajoutée pour que soit générée, automatiquement, en fonction de l'explicabilité globale et locale, un texte que lequel il pourrait s'appuyer...

### Tests et workflow

