# OC_Projet10: Créez une API sécurisée RESTful en utilisant Django REST

## Objectif du projet: développer une API de suivi des problèmes pour les trois plateformes (site web, applications Android et iOS), avec des endpoints qui serviront les données

### Cahier des Charges:
[https://s3-eu-west-1.amazonaws.com/course.oc-static.com/projects/Python%20FR/P8%20-%20Cr%C3%A9ez%20une%20API%20s%C3%A9curis%C3%A9e%20RESTful%20en%20utilisant%20Django%20REST%20/Softdesk%20-%20Conception%20de%20la%20mise%20en%20%C5%93uvre.docx]
[https://s3-eu-west-1.amazonaws.com/course.oc-static.com/projects/Python+FR/P8+-+Cr%C3%A9ez+une+API+s%C3%A9curis%C3%A9e+RESTful+en+utilisant+Django+REST+/Softdesk+-+Conception+de+la+mise+en+%C5%93uvre.odt]

#### Architecture du projet:

Le projet est découpé selon les dossiers suivants:

#### Dossier authentication:
Ce dossier contient tous les fichiers de code définissant les interfaces (views) et les procédés de sign up et de login; l'API utiliser les modèles AbstractUser et UserAdmin de Django) 

#### Dossier SoftDesk:
Ce dossier contient le fichier settings.py où est défini notamment le recours à 'rest_framework', 'rest_framework_simplejwt', 'authentication' de Django. 
Il contient également le fichier urls.py, où sont définies les urls de connexion, d'obtention et de rafraîchissement des tokens, et les routers définissant les différents endpoints. La liste des endpoints de cette API est:

- /projects/   ||   /projects/{id}/

- /projects/{id}/users/   ||   /projects/{id}/users/{id}

- /projects/{id}/issues/   ||   /projects/{id}/issues/{id}

- /projects/{id}/issues/{id}/comments   ||   /projects/{id}/issues/{id}/comments/{id}

#### Dossier tickets:
Ce dossier est découpé de la façon suivante:
- un fichier models.py avec les modèles des tables de la base de données
- un fichier serializers.py avec les serializers qui permettent de charger les données dans la base de données et de les rapatrier (au format JSON)
- un fichier permissions.py qui définit les permissions des différents utilisateurs pour les opérations CRUD des ModelViewsets
- un fichier views.py qui définit les fonctions de service des données grâce aux ModelViewsets: Un ModelViewset  est comparable à une super vue Django qui regroupe   à la fois CreateView, UpdateView, DeleteView, ListView  et DetailView

