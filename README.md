# OC_Projet10: Créez une API sécurisée RESTful en utilisant le Framework Django REST

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

- /projects/   ainsi que   /projects/{id}/:

liste complète des projets; vue d'un projet selon son id

- /projects/{id}/users/   ainsi que   /projects/{id}/users/{id}

liste complète des contributeurs d'un projet; détail d'un utilisateur d'un projet selon son id

- /projects/{id}/issues/   ainsi que    /projects/{id}/issues/{id}

liste complète des problèmes d'un projet; vue d'un problème d'un projet selon son id

- /projects/{id}/issues/{id}/comments   ainsi que    /projects/{id}/issues/{id}/comments/{id}

liste complète des commentaires d'un problème; vue d'un commentaire d'un problème selon son id

#### Dossier tickets:
Ce dossier est découpé de la façon suivante:
- un fichier models.py avec les modèles des tables de la base de données
- un fichier serializers.py avec les serializers qui permettent de charger les données dans la base de données et de les rapatrier (au format JSON)
- un fichier permissions.py qui définit les permissions des différents utilisateurs pour les opérations CRUD des ModelViewsets
- un fichier views.py qui définit les fonctions de service des données grâce aux ModelViewsets: Un ModelViewset  est comparable à une super vue Django qui regroupe   à la fois CreateView, UpdateView, DeleteView, ListView  et DetailView

#### db.sqlite3:
C'est la base de données de Django

#### Fichier manage.py:
Ce fichier contient le script utilitaire de ligne de commande de Django

#### Permissions: 
Les utilisateurs ont les permissions suivantes:
- Un projet ne doit être accessible qu'à son responsable et aux contributeurs. 
- Seuls les contributeurs sont autorisés à créer ou à consulter les problèmes d'un projet.
- Seuls les contributeurs peuvent créer (Create) et lire (Read) les commentaires relatifs à un problème. 
- En outre, ils ne peuvent les actualiser (Update) et les supprimer (Delete) que s'ils en sont les auteurs.
- Un commentaire doit être visible par tous les contributeurs du projet, mais il ne peut être actualisé ou supprimé que par son auteur.

## Comment installer cette Appli sur votre ordinateur:
(i) Requis: téléchargez **[Python 3.10](https://www.python.org/downloads/)**

(ii) puis, avec les commandes du terminal, positionnez-vous sur le dossier dans lequel vous souhaitez installer l'Appli

(iii) pour importer les fichiers de ce repository, tapez la commande git:

`git clone https://github.com/MargueriteEffren/OC_Projet10.git`

(iv) puis positionnez vous dans le dossier OC_Projet10 (`cd OC_Projet10`)

(v) créez votre environnement virtuel, par exemple avec la commande:

`python3 -m venv env`

(vi) à l'aide des commandes du terminal, activez votre environnement virtuel 
(si votre environnement virtuel s'appelle env):
> Sur Windows  
- terminal de type bash : `source env/Scripts/activate`
- terminal de type shell : `env\Scripts\activate`
  
> Sur Mac ou Linux
- `source env/bin/activate`

(vii) puis installez les packages requirements du projet à l'aide de la commande:

`pip install -r requirements.txt`

## Comment utiliser l'Appli:

### Expérience Admin:

Pour avoir une vue admin de la base de données, vous pouvez utiliser directement dans votre navigateur l'url http://127.0.0.1:8000/admin, et vous connecter en tant que superuser avec les identifiants:

username: Admin

password: Admin-OC

### Expérience Développeur:

(i) avec votre terminal, positionnez vous dans le dossier dans lequel vous avez installé l'Appli

(ii) activez l'environnement virtuel

(iii) ensuite tapez la commande 

`python3 manage.py runserver`

pour exécuter le serveur de développement

(iv) puis, avec Postman par exemple, vous pouvez vous connecter avec l'url http://127.0.0.1:8000/softdesk/login, en remplissant les champs username et password;
- quelques exemples d'utilisateurs de Softdesk API:

username: Kate

password: S3cretpassword1

username: Ares

password: S3cretpassword5

username: Elaine

password: S3cretpassword3

username: Lenny

password: S3cretpassword2


(v) vous pouvez exécuter des requêtes (Postman) vers  http://127.0.0.1:8000/softdesk/, suivi de l'url des différents endpoints:

Exemple: http://127.0.0.1:8000/softdesk/projects/1/ pour requêter le projet 1
