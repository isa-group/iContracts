import os
import openai

api_key = os.environ.get('OPENAI_API_KEY', "YOUR_API_KEY")

openai.api_key = api_key
openai.Model.list()


def get_roles(sentences):

    prompt = 'I have a list of SLA statements involving Customer and Provider and I want to know which of the two should perform what the statement says. Your answer should be only a LIST with the actors, Customer or Provider, as "Provider", "Customer", "Customer". Who is the person who should perform the action of the following statements ' + str(sentences) + ' ?'
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0]['message']
    except Exception as error:
        print(error)
