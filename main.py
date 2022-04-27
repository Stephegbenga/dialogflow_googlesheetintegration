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
    # pprint(req)*-**
    parameters = req['queryResult']['parameters']
    pprint(parameters)
    query = {"reg_option":parameters['optionregulier'],"couch":parameters['optionsicouchante'],"post":parameters['poste'],"type_budget":parameters['typebudget'], "location":parameters['any']}
    if query['couch'] == 'non couchante' or query['couch'] == 'non' or query['couch'] == 'no':
        query['couch'] = 'conotconcho'

    if query['couch'] == 'oui' or query['couch'] == 'yes':
        query['couch'] = 'couchante'

    if query['reg_option'] == 'oui' or query['reg_option'] == 'yes':
        query['reg_option'] = 'regulier'

    if query['reg_option'] == 'no' or query['reg_option'] == 'non' or query['reg_option'] == 'non regulier' or query['reg_option'] == ['de temps en temps'] or query['reg_option'] == f"['de temps en temps']":
        query['reg_option'] = 'rekolarni'



    tag = req['queryResult']['intent']['displayName']
    pprint(query)
    if tag == '01-get-info-employeur':
        message = None
        getdetails = getsimilarwords(query)
        print(getdetails)


        main_message = []
        no_result = len(getdetails)
        if no_result == 0:
            message = "No result found"
            main_message.append(message)
        else:
            info_array = []
            for count, getdetail in enumerate(getdetails, start=1):
                info = f"{count} Name: {getdetail['name']}\nPhone Number: {getdetail['phonenumber']}\n\n"
                info_array.append(info)

            message1 = f"Parfait, nous avons {no_result} personnes correspondant parfaitement à vos critères:"
            message2 = "".join(info_array)
            main_message.append(message1)
            main_message.append(message2)

        message = messageconstruct(main_message)
        return message



if __name__ == '__main__':
    app.run()




