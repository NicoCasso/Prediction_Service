from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordBearer

from endpoints import auth, loans, admin

from utils.jwt_handlers import get_current_admin, get_current_user, verify_token
from db.session_provider import get_db_session
import core.password_management as pm
import populate_db as populate_db 

# Créer une instance de l'application FastAPI
app = FastAPI()

# Inclure les routes définies dans les fichiers séparés
app.include_router(auth.router)
app.include_router(loans.router)
app.include_router(admin.router)


# # Définir un schéma d'authentification
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

client = TestClient(app)

users = populate_db.users_list
admin_user = users[0]
client_user_1 = users[1]
client_user_2 = users[2]

#______________________________________________________________________________
#
# region 1 : auth login
#______________________________________________________________________________
def test_login_OK():
    """Test pour obtenir un token d'accès valide"""

    user = admin_user
    response = get_login_response(admin_user)

    assert response.status_code == 200
    assert "access_token" in response.json()

def get_login_response(user) :
    
    payload = {
        "username": str(admin_user["email"]),
        "password": str(admin_user["password"])
    }

    response = client.post("/auth/login", data = payload)
    return response
    
def get_token(loginresponse):
    access_token = loginresponse.json()["access_token"]
    return access_token

def get_headers(jwt_token) :
    str_token = str(jwt_token)
    headers = {
        'Authorization': f'Bearer {str_token}',  # Ajout du token dans l'en-tête Authorization
    }
    return headers

#______________________________________________________________________________
#
# region 2 : auth activation
#______________________________________________________________________________
def test_activation_OK():
    
    user_login_response = get_login_response(client_user_1)
    jwt_token = get_token(user_login_response)
    headers = get_headers(jwt_token)

    # Données d'activation
    activation_data = {"email": str(client_user_1["email"]), "password": "otherpass1"}
    
    # Appel à la route d'activation
    response = client.post("/auth/activation", json=activation_data, headers= headers)

    # Vérifications
    assert response.status_code == 200
    assert response.json()["msg"] == "Account activated and password updated successfully."


#______________________________________________________________________________
#
# region 3 : auth logout
#______________________________________________________________________________
def test_logout_OK():

    admin_login_response = get_login_response(client_user_1)
    jwt_token = get_token(admin_login_response)
    headers = get_headers(jwt_token)

    # Appel à la route de déconnexion
    response = client.post("/auth/logout", headers=headers)

    # Vérifications
    assert response.status_code == 200
    assert response.json()["msg"] == "Logged out successfully. Token is invalidated."

#______________________________________________________________________________
#
# region 4 : loans predict
#______________________________________________________________________________
def test_loans_predict_OK():

    user_login_response = get_login_response(client_user_1)
    jwt_token = get_token(user_login_response)
    headers = get_headers(jwt_token)

    # Appel à la route de prédiction d'éligibilité
    response = client.get("/loans/predict", headers=headers)

    # Vérifications
    assert response.status_code == 200
    assert response.json() == {"eligibility": "Eligible"}  # Vérifie que l'éligibilité est "Eligible"

#______________________________________________________________________________
#
# region 5 : loans request
#______________________________________________________________________________
def test_loans_request_OK():

    user_login_response = get_login_response(client_user_1)
    jwt_token = get_token(user_login_response)
    headers = get_headers(jwt_token)

    # Données de la demande de prêt
    loan_request_data = {"amount": 10000, "term": 12}

    # Appel à la route de soumission de la demande de prêt
    response = client.post("/loans/request", json=loan_request_data, headers={"Authorization": "Bearer mock_token"})

    # Vérifications
    assert response.status_code == 200
    assert response.json() == {"msg": "Loan request submitted successfully."}


#______________________________________________________________________________
#
# region 6 : loans history
#______________________________________________________________________________
def test_loans_history_OK():

    user_login_response = get_login_response(client_user_1)
    jwt_token = get_token(user_login_response)
    headers = get_headers(jwt_token)

    # Appel à la route d'historique des demandes de prêt
    response = client.get("/loans/history", headers=headers)

    # Vérifications
    assert response.status_code == 200
    loan_history = response.json()["loan_history"]
    assert len(loan_history) == 2  # Vérifie que deux demandes de prêt sont retournées
    assert loan_history[0]["amount"] == 10000  # Vérifie que la première demande a bien le montant attendu
    assert loan_history[1]["amount"] == 5000  # Vérifie que la deuxième demande a bien le montant attendu

#______________________________________________________________________________
#
# region 7 : admin users
#______________________________________________________________________________
def test_get_users_OK():

    admin_login_response = get_login_response(admin_user)
    jwt_token = get_token(admin_login_response)
    headers = get_headers(jwt_token)

    # Envoie une requête GET pour récupérer la liste des utilisateurs
    response = client.get("/admin/users", headers=headers )

    # Vérifie la réponse et les résultats attendus
    assert response.status_code == 200
    assert "users" in response.json()
    assert len(response.json()["users"]) == len(users)
    assert response.json()["users"][1]["email"] == client_user_1["email"]

#______________________________________________________________________________
#
# region 8 : create_user
#______________________________________________________________________________
def test_create_user_OK():
    
    admin_login_response = get_login_response(admin_user)
    jwt_token = get_token(admin_login_response)
    headers = get_headers(jwt_token)

    # Données utilisateur à envoyer
    user_data = {
        "username" : "User3",
        "email" : "user3.fakemail@fakeprovider.com",
        "is_active" : False, 
        "password" : "initialpass3",
        "role"  : "user"
    }
    users.append(user_data)

    # Simuler l'appel à la route de création d'utilisateur
    response = client.post("/admin/users", json=user_data)

    # Vérifications
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]

if __name__ == "__main__" :
    test_login_OK()
    #test_logout_OK()
    #test_activation_OK()

    test_get_users_OK()
    test_create_user_OK()

    test_loans_predict_OK()
    test_loans_history_OK()
    test_loans_request_OK()

