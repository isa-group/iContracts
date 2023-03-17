from functools import wraps
from flask import request, g
import spacy

nlp_model = spacy.load('en_core_web_sm', disable=['ner'])


def paragraph_decoder(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            text = [request.json['paragraph']]
        else:
            text = [request.form['paragraph']]
        g.text = text
        doc_to_split = list(nlp_model.pipe(text))
        sentences = []

        for i in range(len(doc_to_split)):
            for sent in list(doc_to_split[i].sents):
                sentence = '"' + str(sent) + '"'
                sentences.append(sentence)

        g.sent_list = sentences
        return func(*args, **kwargs)

    return decorated_function
