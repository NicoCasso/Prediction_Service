import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel

from alembic import context

# C'est important d'ajouter le chemin vers le dossier principal de l'application pour importer correctement les modèles
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import des modèles à inclure dans les migrations
from models.models import UserInDb, LoanRequestInDb, TokenInDB # Attention au chemin d'acces

#______________________________________________________________________________
#
# Lire la configuration de la base de données depuis le fichier alembic.ini
#______________________________________________________________________________
config = context.config

# Lire le fichier de configuration .ini pour les paramètres de connexion à la base de données
fileConfig(config.config_file_name)

#______________________________________________________________________________
#
# Configuration de l'URL de la base de données (elle peut être définie dans alembic.ini)
#______________________________________________________________________________
target_metadata = SQLModel.metadata  # Cela pointe vers les métadonnées des modèles SQLModel


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
