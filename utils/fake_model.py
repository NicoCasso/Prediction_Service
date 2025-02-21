from models.models import LoanRequestInDb
import random

class FakeModel :
    def __init__(self, loanRequest : LoanRequestInDb) :
        pass

    def predict_approval_status(self) -> str :
        return random.choice(["Approved","Not approved"])