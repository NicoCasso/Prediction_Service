from pydantic import BaseModel, Field, field_validator
from typing import Optional

#______________________________________________________________________________
#
# region Loan request Data
#______________________________________________________________________________
class LoanRequestData(BaseModel):
    """
    Data used for loan prediction.

    Attributes:
        state (str): State, encoded on 2 characters.
        bank (str): Bank name.
        naics (int): North American Industry Classification System code (first two digits).
        term (int): Loan term in months.
        no_emp (int): Number of business employees.
        new_exist (int): 1 = Existing business, 2 = New business (boolean).
        create_job (int): Number of jobs created.
        retained_job (int): Number of jobs retained.
        urban_rural (int): 1 = Urban, 2 = Rural, 0 = Undefined.
        rev_line_cr (int): 1 = Revolving line of credit, 0 = No revolving line of credit (boolean).
        low_doc (int): 1 = Low-documentation loan program, 0 = No low-documentation loan program (boolean).
        gr_appv (int): Gross amount of loan approved by the bank.
        recession (int): 1 = During recession period (December 2007 to June 2009), 0 = Otherwise (boolean).
        has_franchise (int): 1 = Has a franchise code, 0 = Does not have a franchise code (boolean).
    """
    state: str = Field(
        min_length=2,
        max_length=2,
        description="State, encoded on 2 characters"
    )
    bank: str = Field(
        min_length=1,
        description="Bank name"
    )
    naics: int = Field(
        ge=0,
        le=99,
        description="North American Industry Classification System code (first two digits)"
    )
    term: int = Field(
        ge=0,
        description="Loan term in months"
    )
    no_emp: int = Field(
        ge=0,
        description="Number of business employees"
    )
    new_exist: int = Field(
        ge=1,
        le=2,
        description="1 = Existing business, 2 = New business (boolean)"
    )
    create_job: int = Field(
        ge=0,
        description="Number of jobs created"
    )
    retained_job: int = Field(
        ge=0,
        description="Number of jobs retained"
    )
    urban_rural: int = Field(
        ge=0,
        le=2,
        description="1 = Urban, 2 = Rural, 0 = Undefined"
    )
    rev_line_cr: int = Field(
        ge=0,
        le=1,
        description="1 = Revolving line of credit, 0 = No revolving line of credit (boolean)"
    )
    low_doc: int = Field(
        ge=0,
        le=1,
        description="1 = Low-documentation loan program, 0 = No low-documentation loan program (boolean)"
    )
    gr_appv: int = Field(
        ge=0,
        description="Gross amount of loan approved by the bank"
    )
    recession: int = Field(
        ge=0,
        le=1,
        description="1 = During recession period (December 2007 to June 2009), 0 = Otherwise (boolean)"
    )
    has_franchise: int = Field(
        ge=0,
        le=1,
        description="1 = Has a franchise code, 0 = Does not have a franchise code (boolean)"
    )

    @field_validator('state')
    def state_must_be_two_chars(cls, v):
        if len(v) != 2:
            raise ValueError("State must be exactly 2 characters")
        return v.upper()

    @field_validator('bank')
    def bank_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("Bank name cannot be empty")
        return v.upper()

    @field_validator('urban_rural')
    def urban_rural_must_be_valid(cls, v):
        if v not in [0, 1, 2]:
            raise ValueError("Urban/Rural must be 0, 1, or 2")
        return v

    @field_validator('rev_line_cr', 'low_doc', 'recession', 'has_franchise')
    def binary_fields_must_be_valid(cls, v):
        if v not in [0, 1]:
            raise ValueError("Binary fields must be either 0 or 1")
        return v

#______________________________________________________________________________
#
# region Loan response Data
#______________________________________________________________________________
class LoanResponseData(BaseModel):
    """
    Response data for loan request.

    Attributes:
        approval_status (str): Approval status of the loan request.
    """
    approval_status: str

#______________________________________________________________________________
#
# region Loan info Data
#______________________________________________________________________________
class LoanInfoData(LoanRequestData):
    """
    Extended data for loan information, including approval status.

    Inherits from LoanRequestData and adds an approval status field.
    """
    approval_status: Optional[str]