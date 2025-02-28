from models.models import LoanRequestInDb
from catboost import CatBoostClassifier
import pandas as pd
import numpy as np
import pickle 

class MaxModel : 
    
    def __init__(self, loan_data : LoanRequestInDb):
        self.loan_data = loan_data
        self.result_dico = {
            0 : "Not approved",
            1 : "Approved"
        }
    
    def predict_approval_status(self) :
        with open("startpoint/catboost_model.pkl", "rb") as f:
            max_model = pickle.load(f)

        max_model : CatBoostClassifier = max_model
    
        features = [
            [str(self.loan_data.state), # "State" : str
            str(self.loan_data.bank), # "Bank" : str
            str(self.loan_data.naics), # "NAICS" str
            int(self.loan_data.term), # "Term" : int
            int(self.loan_data.no_emp), # "NoEmp" : int 
            int(self.loan_data.new_exist), # "NewExist" : int 
            int(self.loan_data.create_job), # "CreateJob", :int
            int(self.loan_data.retained_job), # "RetainedJob" : int
            int(self.loan_data.urban_rural), # "UrbanRural" : int
            int(self.loan_data.rev_line_cr), # "RevLineCr" : int
            int(self.loan_data.low_doc), # "LowDoc" : int
            float(self.loan_data.gr_appv), # "GrAppv" : float 
            int(self.loan_data.recession), # "Recession" : int
            int(self.loan_data.has_franchise)] # "HasFranchise" : int
        ]

        features_names = [
            "state",        "bank",        "naics",       "term",    "no_emp",  "new_exist", "create_job", 
            "retained_job", "urban_rural", "rev_line_cr", "low_doc", "gr_appv", "recession", "has_franchise"
        ]

        result = max_model.predict(features)
        #useless_data = result[1]
        useful_data = result[0]

        #return self.result_dico[useful_data]

        json_result = {}
        json_result["approval_status"] = self.result_dico[useful_data]

        probas = max_model.predict_proba(features)
        singles_probas = probas[0]
        json_result["approval_proba_0"] = singles_probas[0]
        json_result["approval_proba_1"] = singles_probas[1]
        
        importances = max_model.get_feature_importance()
        for feature, importance in zip(features_names, importances):
            feature_name = f"feat_imp_{feature}"
            json_result[feature_name] = importance

        return json_result
        
        

