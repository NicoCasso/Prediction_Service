from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import List, Optional

#______________________________________________________________________________
#
# region UserInDb: The User object as stored in the database
#______________________________________________________________________________
class UserInDb(SQLModel, table=True):
    """
    Represents a user stored in the database.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): Username of the user (optional).
        email (str): Unique email of the user.
        password_hash (str): Hashed password of the user.
        role (str): Role of the user (e.g., "user" or "admin").
        is_active (bool): Boolean flag indicating if the account is active.
        loans (List[LoanRequestInDb]): Relationship with the LoanRequest table.
                                       Each user can have multiple loan requests.
    """

    __tablename__ = "userindb"
    id: int = Field(default=None, primary_key=True)
    username: Optional[str] = Field(default="You", max_length=100, nullable=True)
    email: Optional[str] = Field(unique=True, max_length=255, nullable=False)
    password_hash: str = Field(max_length=255, nullable=False)
    role: str = Field(default="user", max_length=50, nullable=False)
    is_active: bool = Field(default=False)
    loans: List["LoanRequestInDb"] = Relationship(back_populates="user")

#______________________________________________________________________________
#
# region LoanRequestInDb: The LoanRequest object as stored in the database
#______________________________________________________________________________
class LoanRequestInDb(SQLModel, table=True):
    """
    Represents a loan request stored in the database.

    Attributes:
        id (Optional[int]): Unique identifier for the loan request (auto-generated).
        user_id (int): Foreign key referencing the user who submitted the loan request.
        state (str): State of the business (e.g., "OH").
        bank (str): Name of the bank.
        naics (int): North American Industry Classification System code (first two digits).
        term (int): Loan term in months.
        no_emp (int): Number of employees in the business.
        new_exist (int): 1 = Existing business, 2 = New business (boolean).
        create_job (int): Number of jobs created.
        retained_job (int): Number of jobs retained.
        urban_rural (int): 1 = Urban, 2 = Rural, 0 = Undefined.
        rev_line_cr (int): 1 = Revolving line of credit, 0 = No revolving line of credit (boolean).
        low_doc (int): 1 = Low-documentation loan program, 0 = No low-documentation loan program (boolean).
        gr_appv (int): Gross amount of loan approved by the bank.
        recession (int): 1 = During recession period (December 2007 to June 2009), 0 = Otherwise (boolean).
        has_franchise (int): 1 = Has a franchise code, 0 = Does not have a franchise code (boolean).
        approval_status (Optional[str]): Approval status of the loan request.
    """
    __tablename__ = "loan_requests"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="userindb.id")
    state: str = Field(max_length=10, nullable=False)
    bank: str = Field(max_length=255, nullable=False)
    naics: int = Field(nullable=False)
    term: int = Field(nullable=False)
    no_emp: int = Field(nullable=False)
    new_exist: int = Field(default=0)
    create_job: int = Field(nullable=False)
    retained_job: int = Field(nullable=False)
    urban_rural: int = Field(default=0)
    rev_line_cr: int = Field(default=0)
    low_doc: int = Field(default=0)
    gr_appv: int = Field(nullable=False)
    recession: int = Field(default=0)
    has_franchise: int = Field(default=0)
    approval_status: Optional[str] = Field(default=None, max_length=50)

    # Relationship to link a loan request to a user
    user: Optional[UserInDb] = Relationship(back_populates="loans")

#______________________________________________________________________________
#
# region TokenInDB: White list of valid tokens
#______________________________________________________________________________
class TokenInDB(SQLModel, table=True):
    """
    Represents a valid token stored in the database.

    Attributes:
        id (int): Unique identifier for the token.
        expires (datetime): Expiration time of the token.
        token (str): The token string.
    """

    __tablename__ = "valid_tokens"
    
    id: int = Field(default=None, primary_key=True)
    expires: datetime = Field(nullable=False)
    token: str = Field(max_length=512, nullable=False)