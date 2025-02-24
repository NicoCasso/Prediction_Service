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
        with open("startpoint/cat_boost_model.pkl", "rb") as f:
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

        result = max_model.predict(features)
        
        #useless_data = result[1]
        useful_data = result[0]
        match useful_data :
            case 0 : return self.result_dico[0]
            case 1 : return self.result_dico[1]
            case _ : return "Strange result"

