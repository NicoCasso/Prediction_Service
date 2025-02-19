from fastapi import FastAPI
from fastapi.testclient import TestClient
from endpoints import auth, loans, admin

import pytest
from unittest.mock import patch, MagicMock
from dependencies import get_current_admin, get_current_user, verify_token
from db_session_provider import get_db_session

app = FastAPI()

# Inclure les routes définies dans les fichiers séparés
app.include_router(auth.router)
app.include_router(loans.router)
app.include_router(admin.router)

# Client de test FastAPI
@pytest.fixture
def client():
    return TestClient(app)

# Fixture pour un utilisateur avec un rôle 'admin'
@pytest.fixture
def mock_admin_user():
    return {
        "email": "nicolas.cassonnet@wanadoo.fr",
        "password": "nicolas.cassonnet@wanadoo.fr"  # Le mot de passe en clair pour se connecter
    }

# Fixture pour mocker la session de base de données
@pytest.fixture
def mock_db_session():
    mock_session = MagicMock()
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    yield mock_session

# Fixture pour simuler un utilisateur actuel
@pytest.fixture
def mock_current_user():
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.email = "nicolas.cassonnet@wanadoo.fr"
    return mock_user

# Fixture pour mocker `verify_token`
@pytest.fixture
def mock_verify_token():
    return "mocked_token"

# Reset des overrides après chaque test
@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    app.dependency_overrides = {}
    yield
    app.dependency_overrides = {}

#______________________________________________________________________________
#
# region 1 : auth login
#______________________________________________________________________________
def test_login_OK(client: TestClient, mock_admin_user, mock_db_session):
    """Test pour obtenir un token d'accès valide"""

    # Simuler la récupération de l'utilisateur dans la base de données
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_admin_user
    mock_admin_user["verify_password"] = lambda password: password == mock_admin_user["password"]

    # Envoie une requête POST pour se connecter et obtenir un token d'accès
    response = client.post("/auth/login",
        json= {
            "email": mock_admin_user["email"],
            "password": mock_admin_user["password"]
        })

    assert response.status_code == 200
    assert "access_token" in response.json()
    access_token = response.json()["access_token"]
    return access_token

#______________________________________________________________________________
#
# region 2 : auth activation
#______________________________________________________________________________
def test_activation_OK(client: TestClient, mock_db_session, mock_current_user):
    # Données d'activation
    activation_data = {"email": mock_current_user.email, "password": "new_password"}

    # Mock de `get_current_user` pour renvoyer l'utilisateur en cours
    app.dependency_overrides[get_current_user] = lambda: mock_current_user  # L'utilisateur courant est un admin

    # Mock de la fonction `verify_token`
    app.dependency_overrides[verify_token] = lambda: "valid_token"

    # Mock de la session de base de données
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_current_user  # L'utilisateur existe dans la base

    # Simuler l'appel à la route d'activation
    response = client.post("/auth/activation", json=activation_data)

    # Vérifications
    assert response.status_code == 200
    assert response.json()["msg"] == "Account activated and password updated successfully."
    assert mock_db_session.commit.called
    assert mock_db_session.refresh.called

    # Vérification que l'utilisateur est activé et que le mot de passe a été changé
    updated_user = mock_db_session.query.return_value.filter.return_value.first.return_value
    assert updated_user.is_active is True
    assert updated_user.password == "new_password"

#______________________________________________________________________________
#
# region 3 : auth logout
#______________________________________________________________________________
def test_logout_OK(client: TestClient):
    # Mock de la fonction `verify_token` pour valider le token
    app.dependency_overrides[verify_token] = lambda: "valid_token"

    # Simuler l'appel à la route de déconnexion
    response = client.post("/auth/logout")

    # Vérifications
    assert response.status_code == 200
    assert response.json()["msg"] == "Logged out successfully. Token is invalidated."

#______________________________________________________________________________
#
# region 4 : loans predict
#______________________________________________________________________________
def test_loans_predict_OK(client: TestClient, mock_verify_token):
    # Mock de la fonction `get_current_user` pour retourner un utilisateur simulé
    client.app.dependency_overrides[verify_token] = lambda: mock_verify_token

    # Simuler l'appel à la route de prédiction d'éligibilité
    response = client.get("/loans/predict", headers={"Authorization": "Bearer mock_token"})

    # Vérifications
    assert response.status_code == 200
    assert response.json() == {"eligibility": "Eligible"}  # Vérifie que l'éligibilité est "Eligible"

#______________________________________________________________________________
#
# region 5 : loans request
#______________________________________________________________________________
def test_loans_request_OK(client: TestClient, mock_verify_token, mock_db_session, mock_current_user):
    # Mock de la fonction `get_current_user` pour retourner un utilisateur simulé
    client.app.dependency_overrides[verify_token] = lambda: mock_verify_token
    client.app.dependency_overrides[get_current_user] = lambda: mock_current_user
    client.app.dependency_overrides[get_db_session] = lambda: mock_db_session

    # Données de la demande de prêt
    loan_request_data = {"amount": 10000, "term": 12}

    # Simuler l'appel à la route de soumission de la demande de prêt
    response = client.post("/loans/request", json=loan_request_data, headers={"Authorization": "Bearer mock_token"})

    # Vérifications
    assert response.status_code == 200
    assert response.json() == {"msg": "Loan request submitted successfully."}

    # Vérifie que la demande de prêt a bien été ajoutée à la base de données
    mock_db_session.add.assert_called_once()  # Vérifie que `add` a été appelé une fois
    mock_db_session.commit.assert_called_once()  # Vérifie que `commit` a été appelé une fois

#______________________________________________________________________________
#
# region 6 : loans history
#______________________________________________________________________________
def test_loans_history_OK(client: TestClient, mock_verify_token, mock_db_session, mock_current_user):
    # Mock de la fonction `get_current_user` pour retourner un utilisateur simulé
    client.app.dependency_overrides[verify_token] = lambda: mock_verify_token
    client.app.dependency_overrides[get_current_user] = lambda: mock_current_user
    client.app.dependency_overrides[get_db_session] = lambda: mock_db_session

    # Simuler l'appel à la route d'historique des demandes de prêt
    response = client.get("/loans/history", headers={"Authorization": "Bearer mock_token"})

    # Vérifications
    assert response.status_code == 200
    loan_history = response.json()["loan_history"]
    assert len(loan_history) == 2  # Vérifie que deux demandes de prêt sont retournées
    assert loan_history[0]["amount"] == 10000  # Vérifie que la première demande a bien le montant attendu
    assert loan_history[1]["amount"] == 5000  # Vérifie que la deuxième demande a bien le montant attendu

#______________________________________________________________________________
#
# region 7 : admin users après une connexion réussie
#______________________________________________________________________________
def test_get_users_OK(client: TestClient, mock_admin_user, mock_db_session):
    """Test pour récupérer la liste des utilisateurs avec un token d'accès"""

    # Utilisation du token obtenu de la méthode de connexion pour accéder à la ressource protégée
    access_token = test_login_OK(client, mock_admin_user, mock_db_session)

    # Simuler la récupération des utilisateurs dans la base de données
    mock_db_session.query.return_value.all.return_value = [
        {"email": "user1@example.com"},
        {"email": "user2@example.com"}
    ]

    # Envoie une requête GET pour récupérer la liste des utilisateurs
    response = client.get(
        "/admin/users",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Vérifie la réponse et les résultats attendus
    assert response.status_code == 200
    assert "users" in response.json()
    assert len(response.json()["users"]) == 2
    assert response.json()["users"][0]["email"] == "user1@example.com"

#______________________________________________________________________________
#
# region 8 : Test de la création d'un utilisateur
#______________________________________________________________________________
def test_create_user_OK(client: TestClient, mock_db_session, mock_admin_user):
    # Données utilisateur à envoyer
    user_data = {
        "email": "new_user@example.com",
        "password": "password123"
    }

    # Mock de la fonction `get_current_admin` pour retourner un utilisateur admin simulé
    client.app.dependency_overrides[get_current_admin] = lambda: mock_admin_user

    # Mock de la méthode `session.add` et `session.commit`
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()

    # Simuler l'appel à la route de création d'utilisateur
    response = client.post("/admin/users", json=user_data)

    # Vérifications
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]
    assert mock_db_session.add.called
    assert mock_db_session.commit.called

    # Vérifier que l'utilisateur a bien été créé dans la base de données
    created_user = mock_db_session.add.call_args[0][0]
    assert created_user.email == user_data["email"]

