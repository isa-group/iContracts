from functools import wraps
from flask import request, g
import spacy

nlp_model = spacy.load('en_core_web_sm', disable=['ner'])


def paragraph_decoder(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        body = request.json
        g.body = body
        split_doc = list(nlp_model.pipe([body['paragraph']]))
        sentences = []

        for i in range(len(split_doc)):
            for sent in list(split_doc[i].sents):
                sentence = '"' + str(sent) + '"'
                sentences.append(sentence)

        g.sent_list = sentences
        return func(*args, **kwargs)

    return decorated_function
