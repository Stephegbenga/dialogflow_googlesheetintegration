from flask import Flask, request
from pprint import pprint
# app = Flask(__name__)


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


@app.route('/webhook')
def webhook():
    req = request.get_json()
    pprint(req)
    tag = req['queryResult']['intent']['displayName']
    message = messageconstruct(['hello','steve'])
    return message



if __name__ == '__main__':
    app.run()




