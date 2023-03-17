from flask import g, request, Blueprint, render_template
from .paragraph_decoder import paragraph_decoder
from setfit import SetFitModel
import spacy

nlp_model = spacy.load('en_core_web_sm')

predictor = Blueprint('predictor', __name__)


@predictor.get('/predictions')
def get_predict():
    return render_template("prediction.html", value='Hola', form={ 'paragraph': ''})


@predictor.post('/predictions')
@paragraph_decoder
def predict():
    '''
    Applying the adjusted model to classify sentences
    '''
    sentences_list = g.sent_list
    sentences_list = [s.replace('"', '') for s in sentences_list]
    model = SetFitModel.from_pretrained(
        "marmolpen3/p-MiniLM-L3-v2-sla-obligations-rights")
    predictions = model(sentences_list)
    labels = ["Obligations", "Rights", "Neither"]
    i = 0
    label_results, sentences_results, actor_results = [], [], []

    for p in predictions:
        if labels[p] == "Obligations" or labels[p] == "Rights":
            label_results.append(labels[p].upper())
            sentences_results.append(sentences_list[i])
            actor = extract_actor(sentences_list[i])
            actor_results.append(actor)
        i = i + 1

    value = list(zip(label_results, actor_results))
    result = dict(zip(sentences_results, value))
    check = check_solution(value)
    if request.headers['Content-Type'] == 'application/json':
        return result
    return render_template("prediction.html", value = 'Solve', check = check, results = result, form = { 'paragraph': g.text[0]})


def extract_actor(sentence):
    '''
    Get the subject of the sentence
    '''
    sent = nlp_model(sentence)
    actor = ""
    all_actors = []

    for word in sent:
        if word.pos_ == "VERB":
            subject = [tok for tok in word.children if tok.dep_ == "nsubj"]
            if subject and subject[0].ent_type_ and subject[0].ent_type_ == "ORG":
                print(subject[0].ent_type_)
                all_actors.append("provider")
            elif subject:
                all_actors.append(subject[0].text.lower())

    if "you" in all_actors:
        actor = "CLIENT"
    elif all_actors:
        actor = all_actors[0].upper()
    else:
        actor = "INDETERMINATE"
    return actor


def check_solution(value):
    err = []
    if ('OBLIGATIONS', 'PROVIDER') not in value:
        err.append("There is not obligations for the provider.")
    elif ('RIGHTS', 'PROVIDER') not in value:
        err.append("There is not rights for the provider.")
    elif ('OBLIGATIONS', 'CLIENT') not in value:
        err.append("There is not obligations for the client.")
    elif ('RIGHTS', 'CLIENT') not in value:
        err.append("There is not rights for the client.")
    return err
