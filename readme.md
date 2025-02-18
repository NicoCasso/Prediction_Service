# Initialiser Alembic :
alembic init alembic

# Configurer alembic.ini
Dans le fichier alembic.ini qui a été généré, il faut spécifier l'URL de connexion à la base de données. 

sqlalchemy.url = sqlite:///./test.db

# Modifier env.py dans le dossier alembic/

from mymodel import mymodel  # Une ancienne configuration qui ne fonctionnera pas pour SQLModel

Modifie cette ligne pour qu'elle inclut les modèles SQLModel :

from models import Base  # Remplacer par le modèle défini dans ton projet
from sqlmodel import SQLModel

Ensuite, dans la fonction run_migrations_online(), tu dois t'assurer qu'Alembic utilise SQLModel pour récupérer les métadonnées.

Change cette section de code :

target_metadata = mymodel.Base.metadata  # Cela doit pointer vers SQLModel.Base

Par cette ligne :

target_metadata = SQLModel.metadata  # Utilisation de SQLModel pour la récupération des métadonnées

Cela permet à Alembic de savoir comment appliquer les migrations en utilisant les modèles définis avec SQLModel.
Étape 5 : Générer et appliquer les migrations

Une fois que tout est configuré, tu peux maintenant générer des migrations. Voici les étapes :

    Générer une migration : Cette commande va comparer le schéma actuel de la base de données avec le modèle que tu as défini dans ton code, et générer un fichier de migration correspondant.

alembic revision --autogenerate -m "Initial migration"

Cette commande crée un fichier de migration dans le dossier alembic/versions/ avec un nom qui commence par un identifiant unique et se termine par la description du message.

Appliquer la migration : Après avoir généré le fichier de migration, tu peux appliquer cette migration pour mettre à jour la base de données :

    alembic upgrade head

    Cette commande applique toutes les migrations non appliquées (le cas échéant).

Étape 6 : Exemple d'un fichier de migration généré

Si tout est bien configuré, après avoir généré la migration, tu devrais voir un fichier de migration qui ressemble à ceci dans alembic/versions/ :

"""Initial migration

Revision ID: 123456789abc
Revises: 
Create Date: 2025-02-18 12:34:56.789000
"""

# Référence nécessaire à SQLModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlmodel import SQLModel

# Modèles et tables à migrer
def upgrade():
    # Ce code est automatiquement généré par Alembic
    pass

def downgrade():
    # Ce code est également généré par Alembic
    pass

Note : Les migrations générées par alembic revision --autogenerate peuvent parfois nécessiter un peu d'ajustement. Alembic ne sera pas toujours capable de tout générer correctement, en particulier si des fonctionnalités comme SQLModel sont utilisées. Mais pour les modèles simples, cela devrait fonctionner correctement.
