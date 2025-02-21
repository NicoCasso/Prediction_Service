from models.models import LoanRequestInDb
#from catboost import CatBoostClassifier
import pickle 

class MaxModel : 
    def __init__(self, loan_data : LoanRequestInDb):
        self.loan_data = loan_data
    
    def predict(self) :
        with open("startpoint/cat_boost_model.pkl", "rb") as f:
            max_model = pickle.load(f)
    
        features = [
            [self.loan_data.state,
            self.loan_data.bank,
            self.loan_data.naics,
            self.loan_data.term,
            self.loan_data.no_emp,
            self.loan_data.new_exist,
            self.loan_data.create_job,
            self.loan_data.retained_job,
            self.loan_data.urban_rural,
            self.loan_data.rev_line_cr,
            self.loan_data.low_doc,
            self.loan_data.gr_appv,
            self.loan_data.recession,
            self.loan_data.has_franchise]
        ]

        resultat = max_model.predict(features)

        return resultat

