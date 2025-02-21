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
from schemas.loans_data import LoanRequestData, LoanResponseData, LoanInfoData

import populate_db as populate_db 

import json
from typing import List
import random

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

    user_data = admin_user
    response = get_login_response(user_data)

    if response.status_code == 200 :
        print ("test_login : OK")
        print (response.json().get("access_token"))
    else : 
        print ("test_login : errors / ko")
        

def get_login_response(user_data : UserCreationData) :
    
    auth_data = AuthData(
        email=user_data.email, 
        password=user_data.password)
    
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
# region auth logout
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
        print(response.json())
    else : 
        print ("test_logout : errors / ko")

    # assert response.json()["msg"] == "Logged out successfully. Token is invalidated."

#______________________________________________________________________________
#
# region 3 : loans request
#______________________________________________________________________________
def test_loans_request():

    user_login_response = get_login_response(client_user_1)
    jwt_token = get_token(user_login_response)
    headers = get_headers(jwt_token)

    # Données de la demande de prêt
    loan_request_data = LoanRequestData(
        state = loan_request_data.state,
        bank = loan_request_data.bank,
        naics = loan_request_data.naics,
        term = loan_request_data.term,
        no_emp = loan_request_data.no_emp,
        new_exist = loan_request_data.new_exist,
        create_job = loan_request_data.create_job,
        retained_job = loan_request_data.create_job,
        urban_rural = loan_request_data.urban_rural,
        rev_line_cr= loan_request_data.rev_line_cr,
        low_doc = loan_request_data.low_doc,
        gr_appv = loan_request_data.gr_appv,
        recession = loan_request_data.recession,
        has_franchise = loan_request_data.has_franchise
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
# region 4 : loans history
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
# region 5 : admin users
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
    
    users = []
    try : 
        json_data = response.json()
        users : List[UserInfoData] = [UserInfoData.model_validate(user_data) for user_data in json_data]
    except:
        pass
    
    for user in users : 
        print(user)

#______________________________________________________________________________
#
# region 6 : create_user
#______________________________________________________________________________
def test_create_user():
    
    admin_login_response = get_login_response(admin_user)
    jwt_token = get_token(admin_login_response)
    headers = get_headers(jwt_token)
    
    n = str(random.randint(3, 99))

    # Données utilisateur à envoyer
    user_data = UserCreationData(
        email = f"user{n}.fakemail@fakeprovider.com",
        username=f"User{n}", 
        is_active=False,
        role = "user",
        password= f"initialpass{n}")
    
    users.append(user_data)

    # Simuler l'appel à la route de création d'utilisateur
    response = client.post(
        "/admin/users", 
        data = user_data.model_dump_json(),
        headers = headers)

    # Vérifications
    if response.status_code == 200 :
        print ("test_create_user : OK")
        print(response.json())
    else : 
        print ("test_create_user : errors / ko")

    #assert response.json()["email"] == user_data["email"]

if __name__ == "__main__" :

    tests = []
    tests.append(test_login)
    tests.append(test_get_users)
    tests.append(test_create_user)
    tests.append(test_activation)
    tests.append(test_loans_history)
    tests.append(test_loans_request)
    tests.append(test_logout)

    print("_________________________________________________________")
    for test in tests:
        test()
        print("_________________________________________________________")

