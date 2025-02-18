# installer les dépendances :
pip install -r requirements.txt

# Initialiser Alembic :
alembic init alembic

# Créer une migration initiale:
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

Note : Les migrations générées par alembic revision --autogenerate peuvent parfois nécessiter un peu d'ajustement. Alembic ne sera pas toujours capable de tout générer correctement, en particulier si des fonctionnalités comme SQLModel sont utilisées. Mais pour les modèles simples, cela devrait fonctionner correctement. -->
