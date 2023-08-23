from functools import wraps
from flask import request, g
import spacy
import pdfplumber
import base64
from io import BytesIO


nlp_model = spacy.load('en_core_web_sm', disable=['ner'])


def paragraph_decoder(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        body = request.json
        g.body = body

        if body['pdfFile']:
            try:
                pdf_bytes = base64.b64decode(body['pdfFile'])
                with BytesIO(pdf_bytes) as pdf_buffer:
                    with pdfplumber.open(pdf_buffer) as pdf:
                        content = ''
                        for i in range(len(pdf.pages)):
                            page = pdf.pages[i]
                            page_content = '\n'.join(page.extract_text().split('\n')[:-1])
                            content = content + page_content
            except Exception as e:
                print('Error opening PDF:', e)
        else:
            content = body['paragraph']

        split_doc = list(nlp_model.pipe([content]))
        sentences = []

        for i in range(len(split_doc)):
            for sent in list(split_doc[i].sents):
                sentence = '"' + str(sent) + '"'
                sentences.append(sentence)

        g.content = content
        g.sent_list = sentences
        return func(*args, **kwargs)

    return decorated_function
