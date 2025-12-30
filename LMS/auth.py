from repo import conn, cursor,close_connection

# auth for admin

def is_admin(user_id):
    """Check if the given user_id belongs to an admin."""
    cursor.execute('SELECT role FROM member WHERE member_id = ?', (user_id,))
    row = cursor.fetchone()
    if row and row['role'] == 'admin':
        return True
    return False

# auth for member   
def is_member(user_id):
    """Check if the given user_id belongs to a member."""
    cursor.execute('SELECT role FROM member WHERE member_id = ?', (user_id,))
    row = cursor.fetchone()
    if row and row['role'] == 'member':
        return True
    return False

def authenticate(user_id, password):
    """Authenticate a user by user_id and password. Returns True if valid."""
    cursor.execute(
        'SELECT password FROM member WHERE member_id = ?',
        (user_id,)
    )
    row = cursor.fetchone()
    if row and row['password'] == password:
        return True
    return False




def check_admin(user_id, password):
    """Check if user is admin and authenticate."""
    if not is_admin(user_id):
        return False
    return authenticate(user_id, password)

def check_member(user_id, password):
    """Check if user is member and authenticate."""
    if not is_member(user_id):
        return False
    return authenticate(user_id, password)
