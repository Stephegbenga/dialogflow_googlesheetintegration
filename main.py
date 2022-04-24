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
    queryText = req['queryResult']['queryText'].replace(',', '').split()
    pprint(req)
    tag = req['queryResult']['intent']['displayName']
    message = None
    getdetail = getsimilarwords(queryText)
    no_result = len(getdetail)
    if no_result == 0:
        message = "No result found"
    else:
        message = f"There are {no_result} found on the database"
    message = messageconstruct([message])
    return message



if __name__ == '__main__':
    app.run()




