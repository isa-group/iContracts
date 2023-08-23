import os
import openai

api_key = os.environ.get('OPENAI_API_KEY', "YOUR_API_KEY")

openai.api_key = api_key
openai.Model.list()


def get_roles(statements, lenght, category):

    list_actors = [
        {
            "actor": "Customer",
            "actor": "Provider",
            "actor": "None"
        }
    ]

    prompt = f""" 
            Please detects the actor that must perform the action in each of the {category} statements in the list delimited by double backticks. 
            The available actors are the customer and the provider. If you are not able to detect an actor, put None.

            Perform the following steps:
                1.- Evaluate each statement.
                2.- Extract the actor.
                3.- Return the complete JSON with all actors.

            Example sentences: 
                - "AWS will make commercially reasonable efforts to make Amazon EC2 available to each AWS region with a Monthly Uptime Percentage of at least 99.99%", obligation, provider.
                - "In the event Amazon EC2 fails to meet the region level SLA, you will be eligible to receive a Service Credit as described below", right, customer.
                - "Service Credits may not be transferred or applied to any other account.", obligation, customer.
                - "Service Credits will not entitle you to any refund or other payment from AWS.", obligation, customer

            Provide a VALIDLY formatted JSON with the following key: actor. Note that there must be {lenght} phrases with your actor, please complete the JSON. 
            Example of the format: {list_actors}

            ""{statements}""
            """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],

        )
        return response.choices[0]['message']
    except Exception as error:
        print(error)
