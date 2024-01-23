
def abstract_method(f, *args, **kwargs):
    def wrapper(*args, **kwargs):
        msg = f"Must implement  {f}"
        raise NotImplementedError(msg)

    return wrapper

