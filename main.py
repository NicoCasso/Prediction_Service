from fastapi import FastAPI
from utils.lifespan_handlers import token_cleaner
from endpoints import auth, loans, admin

app = FastAPI(
    lifespan=token_cleaner, 
    title="Prediction Service", 
    description="Service en ligne de prédiction de l'accord d'un prêt bancaire")

# Inclure les routes définies dans les fichiers séparés
#app.include_router(auth.router, prefix="??", tags=["auth"])
app.include_router(auth.router)
app.include_router(loans.router)
app.include_router(admin.router)




