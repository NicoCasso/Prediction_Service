from fastapi import FastAPI
from endpoints import auth, loans, admin

from init_user import init

app = FastAPI()

# Inclure les routes définies dans les fichiers séparés
app.include_router(auth.router)
app.include_router(loans.router)
app.include_router(admin.router)


