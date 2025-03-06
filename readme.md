# installer les dépendances :
pip install -r requirements.txt

# Initialiser Alembic :
alembic init alembic

# Créer une migration initiale:
alembic revision --autogenerate -m "Initial migration"

# mettre à jour : 
alembic upgrade head

# peupler la base : 
lancer populate_db.py

# lancer les tests :
lancer test_app.py

