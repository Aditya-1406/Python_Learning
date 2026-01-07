# lms/auth.py
from functools import wraps

SESSION = {
    "user": None
}

def login_user(user):
    SESSION["user"] = user

def logout_user():
    SESSION["user"] = None

def get_current_user():
    return SESSION["user"]


def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            print("❌ Please login first")
            return
        if user.role != "admin":
            print("⛔ Admin access only")
            return
        return func(*args, **kwargs)
    return wrapper


def member_only(func):
    """
    Member functions → accessible by MEMBER + ADMIN
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            print("❌ Please login first")
            return
        if user.role not in ("member", "admin"):
            print("⛔ Access denied")
            return
        return func(*args, **kwargs)
    return wrapper
