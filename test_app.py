from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordBearer

from endpoints import auth, loans, admin

from utils.jwt_handlers import verify_token
from core.user_role_tools import get_current_admin, get_current_user
from core.password_tools import verify_password
from db.session_provider import get_db_session
from schemas.auth_data import AuthData
from schemas.users_data import UserActivationData, UserInfoData, UserCreationData
from schemas.loans_data import LoanRequestData, LoanResponseData, LoanPredictData, LoanInfoData

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
def test_login():
    """Test pour obtenir un token d'accès valide"""

    user = admin_user
    response = get_login_response(admin_user)

    if response.status_code == 200 :
        print ("test_login : OK")
    else : 
        print ("test_login : errors / ko")
    #assert "access_token" in response.json()

def get_login_response(user) :
    
    auth_data = AuthData(
        email=admin_user.email, 
        password=admin_user.password)
    
    response = client.post("/auth/login", data = auth_data.model_dump_json())
    return response
    
def get_token(loginresponse):
    access_token = loginresponse.json().get("access_token")
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
def test_activation():
    
    user_login_response = get_login_response(client_user_1)
    jwt_token = get_token(user_login_response)
    headers = get_headers(jwt_token)

    # Données d'activation
    activation_data = UserActivationData(
        email=client_user_1.email, 
        is_active=True,
        new_password= "otherpass1")
    
    # Appel à la route d'activation
    response = client.post(
        "/auth/activation", 
        data=activation_data.model_dump_json(), 
        headers= headers)

    # Vérifications
    if response.status_code == 200 :
        print ("test_activation : OK")
    else : 
        print ("test_activation : errors / ko")
    #assert response.json()["msg"] == "Account activated and password updated successfully."


#______________________________________________________________________________
#
# region 3 : auth logout
#______________________________________________________________________________
def test_logout():

    admin_login_response = get_login_response(client_user_1)
    jwt_token = get_token(admin_login_response)
    headers = get_headers(jwt_token)

    # Appel à la route de déconnexion
    response = client.post(
        "/auth/logout", 
        headers=headers)

    # Vérifications

    if response.status_code == 200 :
        print ("test_logout: OK")
    else : 
        print ("test_logout : errors / ko")

    # assert response.json()["msg"] == "Logged out successfully. Token is invalidated."

#______________________________________________________________________________
#
# region 4 : loans predict
#______________________________________________________________________________
def test_loans_predict():

    user_login_response = get_login_response(client_user_1)
    jwt_token = get_token(user_login_response)
    headers = get_headers(jwt_token)

    # Appel à la route de prédiction d'éligibilité
    response = client.get(
        "/loans/predict", 
        headers=headers)

    # Vérifications
    if response.status_code == 200 :
        print ("test_loans_predict: OK")
    else : 
        print ("test_loans_predict : errors / ko")

    #assert response.json() == {"eligibility": "Eligible"}  # Vérifie que l'éligibilité est "Eligible"

#______________________________________________________________________________
#
# region 5 : loans request
#______________________________________________________________________________
def test_loans_request():

    user_login_response = get_login_response(client_user_1)
    jwt_token = get_token(user_login_response)
    headers = get_headers(jwt_token)

    # Données de la demande de prêt
    loan_request_data = LoanRequestData(
        amount = 100000, 
        term=12
    )

    # Appel à la route de soumission de la demande de prêt
    response = client.post(
        "/loans/request", 
        data=loan_request_data.model_dump_json(), 
        headers={"Authorization": "Bearer mock_token"})

    # Vérifications
    if response.status_code == 200 :
        print ("test_loans_request: OK")
    else : 
        print ("test_loans_request : errors / ko")

    # assert response.json() == {"msg": "Loan request submitted successfully."}


#______________________________________________________________________________
#
# region 6 : loans history
#______________________________________________________________________________
def test_loans_history():

    user_login_response = get_login_response(client_user_1)
    jwt_token = get_token(user_login_response)
    headers = get_headers(jwt_token)

    # Appel à la route d'historique des demandes de prêt
    response = client.get(
        "/loans/history", 
        headers=headers)

    # Vérifications
    if response.status_code == 200 :
        print ("test_loans_history : OK")
    else : 
        print ("test_loans_history : errors / ko")

    # loan_history = response.json()["loan_history"]
    # assert len(loan_history) == 2  # Vérifie que deux demandes de prêt sont retournées
    # assert loan_history[0]["amount"] == 10000  # Vérifie que la première demande a bien le montant attendu
    # assert loan_history[1]["amount"] == 5000  # Vérifie que la deuxième demande a bien le montant attendu

#______________________________________________________________________________
#
# region 7 : admin users
#______________________________________________________________________________
def test_get_users():

    admin_login_response = get_login_response(admin_user)
    jwt_token = get_token(admin_login_response)
    headers = get_headers(jwt_token)

    # Envoie une requête GET pour récupérer la liste des utilisateurs
    response = client.get(
        "/admin/users", 
        headers=headers )

    # Vérifie la réponse et les résultats attendus
    if response.status_code == 200 :
        print ("test_get_users : OK")
    else : 
        print ("test_get_users : errors / ko")
    
    # assert "users" in response.json()
    # assert len(response.json()["users"]) == len(users)
    # assert response.json()["users"][1]["email"] == client_user_1["email"]

#______________________________________________________________________________
#
# region 8 : create_user
#______________________________________________________________________________
def test_create_user():
    
    admin_login_response = get_login_response(admin_user)
    jwt_token = get_token(admin_login_response)
    headers = get_headers(jwt_token)

    # Données utilisateur à envoyer
    user_data = UserCreationData(
        email = "user3.fakemail@fakeprovider.com",
        username="User3", 
        is_active=False,
        role = "user",
        password= "initialpass3")
    
    users.append(user_data)

    # Simuler l'appel à la route de création d'utilisateur
    response = client.post(
        "/admin/users", 
        data=user_data,
        headers=headers)

    # Vérifications
    if response.status_code == 200 :
        print ("test_create_user : OK")
    else : 
        print ("test_create_user : errors / ko")

    #assert response.json()["email"] == user_data["email"]

if __name__ == "__main__" :
    test_login()
    test_get_users()
    test_create_user()
    test_activation()
    test_loans_predict()
    test_loans_history()
    test_loans_request()
    test_logout()

