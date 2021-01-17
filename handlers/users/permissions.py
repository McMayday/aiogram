

def permission_decorator(func):
    def outer(message):
        res = func(message)
        return res
    return outer
