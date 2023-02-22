from functools import wraps
from flask import Response, request, g


def paragraph_decoder(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        text = request.json['paragraph']
        g.text = text
        return func(*args, **kwargs)
       
    return decorated_function