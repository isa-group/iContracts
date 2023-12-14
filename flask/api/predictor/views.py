from flask import g, request, Blueprint, render_template, jsonify

from .models import Report
from .paragraph_decoder import paragraph_decoder
from setfit import SetFitModel
from ..services.openai import get_roles
import json
import time

predictor = Blueprint('predictor', __name__)


@predictor.post('/reports')
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
        report = Report(
            name=body['name'],
            document=content,
            obligations=obligations_results,
            rights=rights_results
        )
        report.save()
        report_object = report.to_mongo().to_dict()

    return jsonify(report_object)

def process_batches(items, batch_size, item_type):
    all_roles = []
    i = 0
    while i < len(items):
        if i + batch_size > len(items):
            batch = items[i:len(items)]
            i = len(items)
        else:
            batch = items[i:i + batch_size]
            i = i + batch_size
        gpt_results = get_roles(batch, len(batch), item_type)
        actors_per_item = json.loads(gpt_results['content'].replace("'", "\"")) 
        list_item_actors = [entry["actor"] for entry in actors_per_item]
        all_roles.extend(list_item_actors)
        time.sleep(30)
    return all_roles


@predictor.post('/reports/<id>/roles')
def sentences_actors(id):
    '''
    Get all sentences roles with GPT-3.5 model
    '''
    agreement = Report.objects().get(id=id)

    all_obligations_roles = process_batches(agreement.obligations, 3, "obligations")
    all_rights_roles = process_batches(agreement.rights, 3, "rights")

    agreement.obligations_actors = all_obligations_roles
    agreement.rights_actors = all_rights_roles
    agreement.save()

    result = {
        "obligations": all_obligations_roles,
        "rights": all_rights_roles
    }
    return result


@predictor.get('/reports')
def get_reports():
    '''
    Get all reports
    '''
    reports = Report.objects().all()
    report_data = []

    for report in reports:
        report_object = report.to_mongo().to_dict()
        report_data.append(report_object)

    return jsonify(report_data)


@predictor.get('/reports/<id>')
def get_report(id):
    '''
    Get a report by id
    '''
    report = Report.objects().get(id=id)
    return jsonify(report.to_mongo().to_dict())


@predictor.delete('/reports/<id>')
def delete_report(id):
    '''
    Delete a report by id
    '''
    report = Report.objects().get(id=id)
    report.delete()
    return {"message": "Report deleted successfully"}