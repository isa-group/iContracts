from flask import g, Blueprint
from .paragraph_decoder import paragraph_decoder
from setfit import SetFitModel

predictor = Blueprint('predictor', __name__)

@predictor.post('/prediction')
@paragraph_decoder
def predict():
    sentences_list = g.sent_list
    model = SetFitModel.from_pretrained("marmolpen3/p-MiniLM-L3-v2-sla-obligations-rights")
    predictions = model(sentences_list)
    return f'{predictions}'
