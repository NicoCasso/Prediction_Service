import pickle
from catboost import CatBoostClassifier
import pandas as pd
import numpy as np

# Chemin vers votre fichier pickle
pickle_file_path = 'api/models/endpoints/cat_boost_model.pkl'

# Charger le modèle à partir du fichier pickle
with open(pickle_file_path, 'rb') as file:
    model = pickle.load(file)

# Vérifier si le modèle est bien un modèle CatBoost
if isinstance(model, CatBoostClassifier):
    # Afficher les paramètres du modèle
    params = model.get_params()
    print("Paramètres du modèle :")
    for param, value in params.items():
        print(f"{param}: {value}")

    # Afficher la configuration du modèle (par exemple, les features importances)
    feature_importances = model.get_feature_importance()
    print("\nImportance des features :")
    for feature, importance in zip(model.feature_names_, feature_importances):
        print(f"{feature}: {importance}")
else:
    print("Le modèle n'est pas CatBoost.")

def validate_and_transform_input_data(data):
    # Convertir les données d'entrée en DataFrame
    df = pd.DataFrame([data])

    # Vérifier que les colonnes requises sont présentes
    required_features = [
        "State", "Bank", "NAICS", "Term", "NoEmp", "NewExist",
        "CreateJob", "RetainedJob", "UrbanRural", "RevLineCr",
        "LowDoc", "GrAppv", "Recession", "HasFranchise"
    ]
    missing_features = [feature for feature in required_features if feature not in df.columns]
    if missing_features:
        raise ValueError(f"Features manquantes dans les données d'entrée : {missing_features}")

    # Vérifier le format des colonnes
    if not isinstance(df["State"].iloc[0], str):
        raise ValueError("La colonne 'State' doit être de type string.")
    if not isinstance(df["Bank"].iloc[0], str):
        raise ValueError("La colonne 'Bank' doit être de type string.")
    if not isinstance(df["NAICS"].iloc[0], str):
        raise ValueError("La colonne 'NAICS' doit être de type string.")
    if not isinstance(df["Term"].iloc[0], (int, np.integer)):
        raise ValueError("La colonne 'Term' doit être de type entier.")
    if not isinstance(df["NoEmp"].iloc[0], (int, np.integer)):
        raise ValueError("La colonne 'NoEmp' doit être de type entier.")
    if not isinstance(df["NewExist"].iloc[0], (int, np.integer)):
        raise ValueError("La colonne 'NewExist' doit être de type entier.")
    if not isinstance(df["CreateJob"].iloc[0], (int, np.integer)):
        raise ValueError("La colonne 'CreateJob' doit être de type entier.")
    if not isinstance(df["RetainedJob"].iloc[0], (int, np.integer)):
        raise ValueError("La colonne 'RetainedJob' doit être de type entier.")
    if not isinstance(df["UrbanRural"].iloc[0], (int, np.integer)):
        raise ValueError("La colonne 'UrbanRural' doit être de type entier.")
    if not isinstance(df["RevLineCr"].iloc[0], (int, np.integer)):
        raise ValueError("La colonne 'RevLineCr' doit être de type entier.")
    if not isinstance(df["LowDoc"].iloc[0], (int, np.integer)):
        raise ValueError("La colonne 'LowDoc' doit être de type entier.")
    if not isinstance(df["GrAppv"].iloc[0], (float, np.floating)):
        raise ValueError("La colonne 'GrAppv' doit être de type float.")
    if not isinstance(df["Recession"].iloc[0], (int, np.integer)):
        raise ValueError("La colonne 'Recession' doit être de type entier.")
    if not isinstance(df["HasFranchise"].iloc[0], (int, np.integer)):
        raise ValueError("La colonne 'HasFranchise' doit être de type entier.")

    print("Les données d'entrée sont valides.")
    return df

# Exemple de données d'entrée
input_data = {
    "State": "OH",
    "Bank": "CAPITAL ONE NATL ASSOC",
    "NAICS": "54",
    "Term": 60,
    "NoEmp": 13,
    "NewExist": 1,
    "CreateJob": 0,
    "RetainedJob": 3,
    "UrbanRural": 2,
    "RevLineCr": 0,
    "LowDoc": 0,
    "GrAppv": 50000.0,
    "Recession": 0,
    "HasFranchise": 1,
}

# Valider et transformer les données d'entrée
transformed_data = validate_and_transform_input_data(input_data)
print(transformed_data)

# Faire des prédictions avec le modèle
predictions = model.predict(transformed_data)
print("Prédictions :", predictions)
