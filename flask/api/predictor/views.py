from flask import g, Blueprint
from .paragraph_decoder import paragraph_decoder
from setfit import SetFitModel

predictor = Blueprint('predictor', __name__)

model = SetFitModel.from_pretrained("marmolpen3/p-MiniLM-L3-v2-sla-obligations-rights")

@predictor.post('/predictions')
@paragraph_decoder
def predict():
    print("Hola")
    sentences_list = g.sent_list
    sentences_list = [s.replace('"', '') for s in sentences_list]
    predictions = model(sentences_list)
    labels = ["Obligations", "Rights", "Neither"]
    label_results = [labels[p] for p in predictions]
    result = dict(zip(sentences_list, label_results))
    return result
