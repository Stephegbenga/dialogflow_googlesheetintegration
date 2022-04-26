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
    pprint(req)
    parameters = req['queryResult']['parameters']
    query = {"reg_option":parameters['optionregulier'],"couch":parameters['optionsicouchante'],"post":parameters['poste'],"type_budget":parameters['typebudget']}
    if query['optioncouchante'] == 'non couchante' or query['optioncouchante'] == 'non' or query['optioncouchante'] == 'no':
        query['optioncouchante'] = 'conotconcho'

    if query['optioncouchante'] == 'oui' or query['optioncouchante'] == 'yes':
        query['optioncouchante'] = 'couchante'

    if query['optionregulier'] == 'oui' or query['optionregulier'] == 'yes':
        query['optioncouchante'] = 'regulier'

    if query['optionregulier'] == 'no' or query['optionregulier'] == 'non' or query['optionregulier'] == 'non regulier':
        query['optioncouchante'] = 'rekolarni'



    tag = req['queryResult']['intent']['displayName']

    if tag == '01-get-info-employeur':
        message = None
        getdetails = getsimilarwords(query)

        info_array = []
        for count, getdetail in enumerate(getdetails, start=1):
            info = f"{count} Name: {getdetail['name']}\nPhone Number: {getdetails['phonenumber']}\n\n"
            info_array.append(info)

        main_message = []
        no_result = len(getdetails)
        if no_result == 0:
            message = "No result found"
        else:
            message1 = f"Parfait, nous avons {no_result} personnes correspondant parfaitement à vos critères:"
            message2 = "".join(info_array)
            main_message.append(message1)
            main_message.append(message2)

        message = messageconstruct(main_message)
        return message



if __name__ == '__main__':
    app.run()




