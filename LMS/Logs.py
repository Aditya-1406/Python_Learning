import os

base_dir = os.path.dirname(__file__)
member_logs = os.path.join(base_dir,'Logs','member_log.txt')
book_logs =  os.path.join(base_dir,'Logs','book_log.txt')
loan_logs = os.path.join(base_dir,'Logs','loan_log.txt')

def member_log_create(name, email, password, role,member_id):
    with open(member_logs,'a') as f:
        f.write(f'USER CREATED : NAME - {name}, EMAIL- {email}, PASSWORD- {password}, ROLE- {role}, MEMBER_ID - {member_id}\n ')

def member_log_delete(member_id):
    with open(member_logs,'a') as f:
        f.write(f'USER DELETED : MEMBER_ID - {member_id}\n ')

def book_log_created(book_id,isbn, title, author, copies_available):
    with open(book_logs,'a') as f:
        f.write(f'BOOK ADDED : BOOK ID - {book_id}, ISBN - {isbn}, TITLE - {title}, AUTHOR - {author}, COPIES - {copies_available}\n')

def book_log_delete(book_id):
    with open(book_logs,'a') as f:
        f.write(f'BOOK DELETED : BOOK ID - {book_id} \n')

def book_log_update(book_id,copies):
    with open(book_logs,'a') as f:
        f.write(f'BOOK UPDATED : BOOK ID - {book_id}, COPIES - {copies}\n ')

def loan_log_created(loan_id,borrowed_on, due_on, member_id, book_id):
    with open(loan_logs,'a') as f:
        f.write(f'LOAN CREATED : LOAN ID - {loan_id}, BORROW DATE - {borrowed_on}, DUE DATE - {due_on}, MEMBER - {member_id}, BOOK - {book_id} \n')

def loan_log_updated(loan_id,returned_on, fine_cost, payment):
    with open(loan_logs,'a') as f:
        f.write(f'LOAN UPDATED : LOAN ID - {loan_id}, RETURN DATE - {returned_on}, FINE COST - {fine_cost}, PAYMENT - {payment}\n')

def loan_log_delete(loan_id):
    with open(loan_logs,'a') as f:
        f.write(f'LOAN DELETED : LOAN ID - {loan_id} \n')