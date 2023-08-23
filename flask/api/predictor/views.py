from flask import g, request, Blueprint, render_template, jsonify

from .models import Report
from .paragraph_decoder import paragraph_decoder
from setfit import SetFitModel
from ..services.openai import get_roles
import json

predictor = Blueprint('predictor', __name__)


@predictor.post('/predictions')
@paragraph_decoder
def predict():
    '''
    Applying the adjusted model to classify sentences
    '''
    body = g.body
    sentences_list = g.sent_list
    content = g.content 
    sentences_list = [s.replace('"', '') for s in sentences_list]
    model = SetFitModel.from_pretrained(
        "marmolpen3/paraphrase-mpnet-base-v2-sla-obligations-rights")
    predictions = model(sentences_list)
    labels = ["Obligation", "Right", "Neither"]
    i = 0
    obligations_results, rights_results = [], []
    results = {}

    for p in predictions:
        if labels[p] == "Obligation":
            obligations_results.append(sentences_list[i])
            results[sentences_list[i]] = "Obligation"
        if labels[p] == "Right":
            rights_results.append(sentences_list[i])
            results[sentences_list[i]] = "Right"
        i = i + 1

    if obligations_results != [] or rights_results != []:
        Report(
            name=body['name'],
            document=content,
            obligations=obligations_results,
            rights=rights_results
        ).save()

    return results


@predictor.post('/roles/<id>')
def sentences_actors(id):
    '''
    Get all sentences roles with GPT-3.5 model
    '''
    agreement = Report.objects().get(id=id)
    obligations_actors = get_roles(agreement.obligations)
    rights_actors = get_roles(agreement.rights)
    list_obligations_actors = obligations_actors['content'].replace(
        " ", "").replace(".", "").split(",")
    list_rights_actors = rights_actors['content'].replace(
        " ", "").replace(".", "").split(",")

    agreement.obligations_actors = list_obligations_actors
    agreement.rights_actors = list_rights_actors
    agreement.save()

    result = {
        "obligations": list_obligations_actors,
        "rights": list_rights_actors
    }
    return result


@predictor.get('/reports')
def get_reports():
    '''
    Get all reports
    '''
    reports = Report.objects().all()
    report_data = {}

    for report in reports:
        report_object = report.to_mongo().to_dict()
        report_id = str(report_object['_id'])
        report_data[report_id] = report_object

    return jsonify(report_data)


@predictor.get('/reports/<id>')
def get_report(id):
    '''
    Get a report by id
    '''
    report = Report.objects().get(id=id)
    return jsonify(report.to_mongo().to_dict())
