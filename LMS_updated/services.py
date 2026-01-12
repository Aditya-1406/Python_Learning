
# lms/services.py
from datetime import datetime, timedelta, timezone
from typing import Optional
from db import Database
from repo import MemberRepository, BookRepository, LoanRepository
from models import Loan, Member, Book
from loger import log_function


ISO = "%Y-%m-%d"
PER_DAY  = 10 

def calulate_fine(borrowdate, returndate):
    
    ret_on = datetime.strptime(returndate, "%Y-%m-%d")
    bor_on = datetime.strptime(borrowdate, "%Y-%m-%d")
    delta = (ret_on-bor_on)
    days = delta.days
    fine_cost = 0
    if days> 14 :
        days -=  14
        fine_cost = days * PER_DAY
    return fine_cost

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime(ISO)

def plus_days_iso(days: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(days=days)).strftime(ISO)

class MemberService:

    def __init__(self,member : MemberRepository):
        self.member = member

    @log_function("member_logs.txt")
    def create_member(self,mem: Member):
        try:
            mem_id = self.member.create(mem)
            mem.member_id = mem_id
            log = (f"✅ Member {mem.name} added with ID: {mem.member_id}")
            return mem_id,log
        except Exception as e:
            log =(f"❌ Error adding member: {e}")
            return None,log
        
    
    @log_function("member_logs.txt")
    def get_by_id(self,mem_id: int):
        try:
            mem = self.member.get_by_id(mem_id)
            log = (f"Id : {mem.member_id}, Name : {mem.name}, Email : {mem.email}, Role : {mem.role}  ")
            return mem,log
        except Exception as e:
            log=("❌ Sorry, Some Error while Fetching the data", e)
            return None,log
        
    @log_function("member_logs.txt")
    def get_by_email(self,email: str):
        try:
            mem = self.member.get_by_email(email)
            log = (f"Id : {mem.member_id}, Name : {mem.name}, Email : {mem.email}, Role : {mem.role}  ")
            return (mem, log)
        except Exception as e:
            log = ("❌ Sorry, Some Error while Fetching the data", e)
            return None,log
        
    @log_function("member_logs.txt")  
    def list_all_members(self):
        try:
            mem_list = self.member.list()
            log_arr = []
            for mem in mem_list:
                log_arr.append((f"Id : {mem.member_id}, Name : {mem.name}, Email : {mem.email}, Role : {mem.role}  "))
            return mem_list,log_arr
        except Exception as e:
            log= ("❌ Sorry, Some Error while Fetching the data", e)
            return None,log
    
    @log_function("member_logs.txt")
    def update_role(self,member_id:int, role:str):
        try:
            is_updated = self.member.update_role(member_id,role)
            if is_updated:
                log = (f"✔️ Role has been updated for mem_id {member_id}")
            else:
                log = ("❌ Member not found")
            return log
        except Exception as e:
            log = ("❌ Some error while updating the data", e)
            return  None,log
    
    @log_function("member_logs.txt")
    def delete_user(self,mem_id : int):
        try:
            is_deleted = self.member.delete(mem_id)
            if is_deleted:
                log = (f"✔️ User Deleted Successfully with mem_id {mem_id}")
            else:
                log = ("❌ User not found")
            return log
        except Exception as e:
            log = ("❌ Some Error while deleting the record", e)
            return None,log


        

class BookService:

    def __init__(self, book : BookRepository):
        self.book = book

    def create_book(self,books : Book):
        try:
            book_id = self.book.create(books)
            books.book_id = book_id
            print(f"Book {books.title} Added with Book id : {books.book_id}")
            return book_id
        except  Exception as e :
            print("❌ Some Error while Adding the book", e)
    
    def get_by_id(self,book_id: int):
        try:
            bo = self.book.get_by_id(book_id)
            print(f"Id : {bo.book_id}, ISBN : {bo.isbn}, Title : {bo.title}, Author : {bo.author}, Copies : {bo.copies_available}  ")
            return  bo
        except Exception as e:
            print("❌ Sorry, Some Error while Fetching the data", e)
            return None
        
    def get_by_isbn(self,isbn:str):
        try:
            bo = self.book.get_by_isbn(isbn)
            print(f"Id : {bo.book_id}, ISBN : {bo.isbn}, Title : {bo.title}, Author : {bo.author}, Copies : {bo.copies_available} ")
            return bo
        except Exception as e:
            print("❌ Sorry, Some Error while Fetching the data", e)
            return None
    
    def list_all_book(self):
        try:
            book_list = self.book.list()
            for bo in book_list:
                print(f"Id : {bo.book_id}, ISBN : {bo.isbn}, Title : {bo.title}, Author : {bo.author}, Copies : {bo.copies_available} ")
            return book_list
        except Exception as e:
            print("❌ Sorry, Some Error while Fetching the data", e)
            return None
        
    def delete_book(self,book_id : int):
        try:
            is_deleted = self.book.delete(book_id)
            if is_deleted:
                print("✔️ Book Deleted Successfully")
            else:
                print("❌ Book not found")
        except Exception as e:
            print("❌ Some Error while deleting the record", e)
            return None
  
    def increment_copy(self,book_id):
        try:
            self.book.increment_copy(book_id)
            return
        except Exception as e:
            print("Some Error while incrementing")
            return None
        
  
    def decrement_copy(self,book_id):
        try:
            self.book.decrement_copy(book_id)
            return
        except Exception as e:
            print("Some Error while decrementing")
            return None



class LoanService:
    """Service layer for operations that must be atomic across multiple tables."""

    def __init__(self, members: MemberRepository, books: BookRepository, loans: LoanRepository):
        self.members = members
        self.books = books
        self.loans = loans

    def create_loan(self, loan:Loan):
        try:
            loan_id = self.loans.create(loan)
            loan.loan_id = loan_id
            print(f"✔️ Loan Created with Loan id : {loan_id}")
            self.books.decrement_copy(loan.book_id)
            return loan_id
        except Exception as e:
            print("❌ Some Error While Creating the Loan")
            return None
    
    def get_by_id(self, loan_id):
        try:
            lo = self.loans.get_by_id(loan_id)
            
            formatted = (
                f"Loan ID: {lo.loan_id}, "
                f"Borrowed On: {lo.borrowed_on}, "
                f"Due On: {lo.due_on}, "
                f"Returned On: {lo.returned_on}, "
                f"Fine: {lo.fine}, "
                f"Is Paid: {bool(lo.is_paid)}, "
                f"Member ID: {lo.member_id}, "
                f"Book ID: {lo.book_id}"
            )
            print(formatted)
            return lo

        except Exception as e:
            print("Some Error while fetching the data")
            return None

    
    def list_active_by_member(self, member_id: int) :
            """Return all active (not yet returned) loans of a member, printed and returned."""
            try:
                loans = self.loans.list_active_by_member(member_id)
                if not loans:
                    print(f"ℹ️ No active loans for member_id={member_id}")
                    return []
                print(f"✅ Active loans for member_id={member_id}:")
                for lo in loans:
                    print("  • " + self._format_loan(lo))
                return loans
            except Exception as e:
                print(f"❌ Error while listing active loans for member_id={member_id}: {e}")
                return None

    def mark_returned(self, loan_id: int, returned_on: str) -> bool:
        """Mark a loan as returned."""
        try:
            lo = self.loans.mark_returned(loan_id, returned_on)
            print(f"✔️ Loan {loan_id} marked returned on {returned_on}")
            self.books.increment_copy(lo.book_id)
            return True
        except Exception as e:
            print(f"❌ Error while marking loan {loan_id} as returned: {e}")
            return False

    def set_fine(self, loan_id: int, fine: int) -> bool:
        """Set/Update fine for a loan."""
        try:
            self.loans.set_fine(loan_id, fine)
            if fine:
                print(f"✔️ Fine for loan {loan_id} id : ₹{fine}")
            return True
        except Exception as e:
            print(f"❌ Error while setting fine for loan {loan_id}: {e}")
            return False

    def set_paid(self, loan_id: int, is_paid: bool) -> bool:
        """Mark fine as paid/unpaid."""
        try:
            self.loans.set_paid(loan_id, is_paid)
            state = "paid" if is_paid else "unpaid"
            print(f"✔️ Loan {loan_id} marked as {state}")
            return True
        except Exception as e:
            print(f"❌ Error while updating paid status for loan {loan_id}: {e}")
            return False

    def delete(self, loan_id: int) -> bool:
        """Delete a loan record."""
        try:
            self.loans.delete(loan_id)
            print(f"🗑️ Loan {loan_id} deleted")
            return True
        except Exception as e:
            print(f"❌ Error while deleting loan {loan_id}: {e}")
            return False

    # --- helpers ---

    @staticmethod
    def _format_loan(lo: Loan) -> str:
        """Nicely formatted single-line representation of a Loan."""
        return (
            f"Loan ID: {lo.loan_id}, "
            f"Borrowed On: {lo.borrowed_on}, "
            f"Due On: {lo.due_on}, "
            f"Returned On: {lo.returned_on}, "
            f"Fine: {lo.fine}, "
            f"Is Paid: {bool(lo.is_paid)}, "
            f"Member ID: {lo.member_id}, "
            f"Book ID: {lo.book_id}"
        )


            
        
        

   
