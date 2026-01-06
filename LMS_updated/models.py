
from dataclasses import dataclass
from typing import Optional

@dataclass
class Member:
    member_id: Optional[int]
    name: str
    email: str
    password: str  
    role: str = "member"

@dataclass
class Book:
    book_id: Optional[int]
    isbn: str
    title: str
    author: str
    copies_available: int

@dataclass
class Loan:
    loan_id: Optional[int]
    borrowed_on: str      
    due_on: str
    returned_on: Optional[str]
    fine: int
    is_paid: bool
    member_id: int
    book_id: int
