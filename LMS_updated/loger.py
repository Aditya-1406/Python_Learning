import functools
from datetime import datetime


def log_function(log_file="app_logs.txt"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            result = func(*args, **kwargs)   # call original function

            try:
                if isinstance(result, tuple) and len(result) == 2:
                    _, log_msg = result
                else:
                    log_msg = str(result)

                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(
                        f"[{timestamp}] ✅ {func.__name__} | {log_msg}\n"
                    )

            except Exception as log_err:
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(
                        f"[{timestamp}] ❌ LOGGER ERROR | {str(log_err)}\n"
                    )

            return result   # 🔒 contract preserved

        return wrapper
    return decorator
