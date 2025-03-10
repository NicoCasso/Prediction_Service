import sys
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

from alembic import context
import urllib.parse
from typing import Any
from core.config import CONNECTION_STRING, CONNECTION_ARGS

# C'est important d'ajouter le chemin vers le dossier principal de l'application pour importer correctement les modèles
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import des modèles à inclure dans les migrations
from models.models import UserInDb, LoanRequestInDb, TokenInDB # Attention au chemin d'acces

#______________________________________________________________________________
#
# Lire la configuration de la base de données depuis le fichier alembic.ini
#______________________________________________________________________________
def adapt_config() -> dict[str, Any]:
    config = context.config

    connection_string = (
        f"{CONNECTION_STRING}"
        f"&Encrypt={CONNECTION_ARGS['Encrypt']}"
        f"&TrustServerCertificate={CONNECTION_ARGS['TrustServerCertificate']}"
        f"&Connection Timeout={CONNECTION_ARGS['Connection Timeout']}"
    )

    ini_section = config.get_section(config.config_ini_section)
    ini_section['sqlalchemy.url'] = connection_string
    return ini_section

#______________________________________________________________________________
#
# Configuration de de la base de données 
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

    config = adapt_config()
    url = config['sqlalchemy.url']

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

    config = adapt_config()

    connectable = engine_from_config(
        config,
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
