from flask import g, Blueprint
from .paragraph_decoder import paragraph_decoder

predictor = Blueprint('predictor', __name__)

@predictor.post('/prediction')
@paragraph_decoder
def predict():
    prediction = g.sent_list
    return f'{prediction}'
