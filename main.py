from fastapi import FastAPI
from sqlalchemy.orm import Session
from endpoints import auth, loans, admin

from db.session_provider import get_db_session
from db.token_white_list import clean_tokens

app = FastAPI(title="Prediction Service", description="Service en ligne de prédiction de l'accord d'un prêt bancaire")

# Inclure les routes définies dans les fichiers séparés
#app.include_router(auth.router, prefix="??", tags=["auth"])
app.include_router(auth.router)
app.include_router(loans.router)
app.include_router(admin.router)

async def lifespan_handler(app: FastAPI):
    # Appel au démarrage de l'application (équivalent à startup)
    with next(get_db_session()) as db_session:
        clean_tokens(db_session)  

    yield  # Indiquer que l'application fonctionne maintenant


