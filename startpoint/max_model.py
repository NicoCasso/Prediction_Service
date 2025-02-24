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
            [self.loan_data.state,
            self.loan_data.bank,
            str(self.loan_data.naics),
            self.loan_data.term,
            self.loan_data.no_emp,
            self.loan_data.new_exist,
            self.loan_data.create_job,
            self.loan_data.retained_job,
            self.loan_data.urban_rural,
            self.loan_data.rev_line_cr,
            self.loan_data.low_doc,
            float(self.loan_data.gr_appv),
            self.loan_data.recession,
            self.loan_data.has_franchise]
        ]

        result = max_model.predict(features)
        
        #useless_data = result[1]
        useful_data = result[0]
        match useful_data :
            case 0 : return self.result_dico[0]
            case 1 : return self.result_dico[1]
            case _ : return "Strange result"

