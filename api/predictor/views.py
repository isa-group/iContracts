from flask import Flask, request, g, Blueprint
from .paragraph_decoder import paragraph_decoder

predictor = Blueprint('predictor', __name__)

@predictor.post('/prediction')
@paragraph_decoder
def predict():
    paragraph = request.json['paragraph']
    print(paragraph)
    prediction = g.text
    return f'{prediction}'
