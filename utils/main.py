from fastapi import FastAPI
from alembic.models.endpoints.user import auth, loans, admin

app = FastAPI()

# Inclure les routes définies dans les fichiers séparés
app.include_router(auth.router)
app.include_router(loans.router)
app.include_router(admin.router)
