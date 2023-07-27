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
- suppression des outilers en "applatissant" à 

### Modélisation et MLFlow

### Analyse du Data Drift

### Description du dossier API

### Description du dossier Streamlit

### Tests et workflow
