from fastapi import FastAPI
from utils.lifespan_handlers import token_cleaner
from endpoints import auth, loans, admin, sync

app = FastAPI(
    lifespan=token_cleaner,
    title="Prediction Service",
    description="Service en ligne de prédiction de l'accord d'un prêt bancaire",
    openapi_tags=[
        {
            "name": "auth",
            "description": "Authentication endpoints."
        },
        {
            "name": "loans",
            "description": "Loan request and history endpoints."
        },
        {
            "name": "admin",
            "description": "Admin-related endpoints."
        },
        {
            "name": "sync",
            "description": "Admin-sync related endpoints."
        }
    ]
)

# Include the routers with unique prefixes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(loans.router, prefix="/loans", tags=["loans"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(sync.router, prefix="/sync", tags=["sync"])

# Optional: Add middleware for CORS if needed
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)