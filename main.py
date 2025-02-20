from fastapi import FastAPI
from endpoints import auth, loans, admin

#from init_user import init

app = FastAPI(title="Prediction Service", description="Service en ligne de prédiction de l'accord d'un prêt bancaire")

# Inclure les routes définies dans les fichiers séparés
#app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(auth.router)
app.include_router(loans.router)
app.include_router(admin.router)


