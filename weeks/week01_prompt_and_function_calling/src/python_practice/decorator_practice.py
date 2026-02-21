import format_number
import random
def log(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"[log] {func.__name__},args: {args}, kwargs: {kwargs}, result: {result}")
        return result
    return wrapper

def retry(max_retry=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(max_retry):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    print(f"[retry] {func.__name__} failed, retrying...")
                    continue
            raise Exception("max retry")
        return wrapper
    return decorator

@log
def fmt_number(number):
    return format_number.format_number(number)

@retry()
def fmt_number_retry(number):
    if random.random() < 0.5:
        raise Exception("test")
    return "success"

if __name__ == "__main__":
    print(fmt_number_retry(100000000))
