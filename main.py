from flask import Flask, request
from pprint import pprint
from processinfo import getsimilarwords
app = Flask(__name__)


def messageconstruct(infos):
    fulfillmentMessages = []
    for info in infos:
        fulfillmentMessages.append({
                "text": {
                    "text": [
                        info
                    ]
                }
            })

    message = {
        "fulfillmentMessages": fulfillmentMessages
    }
    return message



@app.route('/')
def homepage():
    return "Google Sheets Database"


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    parameters = req['queryResult']['parameters']
    query = [parameters['optionregulier'],parameters['optionsicouchante'],parameters['poste'],parameters['typebudget']]
    pprint(req)
    tag = req['queryResult']['intent']['displayName']

    if tag == '01-get-info-employeur':
        message = None
        getdetail = getsimilarwords(query)
        no_result = len(getdetail)
        if no_result == 0:
            message = "No result found"
        else:
            message = f"Parfait, nous avons {no_result} personnes correspondant parfaitement à vos critères:"
        message = messageconstruct([message])
        return message



if __name__ == '__main__':
    app.run()




