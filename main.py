from flask import Flask, request
from pprint import pprint
from processinfo import getsimilarwords, insertrow
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

    action = req['queryResult']['action']


    if action == '01-get-info-employeur':
        try:
            parameters['optionregulier'] = parameters['optionregulier'][0]
        except:
            print("it's Normal")

        query = {"reg_option": parameters['optionregulier'], "couch": parameters['optionsicouchante'],
                 "post": parameters['poste'], "type_budget": parameters['typebudget'], "location": parameters['any']}

        if query['couch'] == 'non couchante' or query['couch'] == 'non' or query['couch'] == 'no':
            query['couch'] = 'conotconcho'

        if query['couch'] == 'oui' or query['couch'] == 'yes':
            query['couch'] = 'couchante'

        if query['reg_option'] == 'oui' or query['reg_option'] == 'yes':
            query['reg_option'] = 'regulier'

        if query['reg_option'] == 'no' or query['reg_option'] == 'non' or query['reg_option'] == 'non regulier' or \
                query['reg_option'] == ['de temps en temps'] or query['reg_option'] == f"['de temps en temps']":
            query['reg_option'] = 'rekolarni'

        pprint(query)

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

    elif action == 'saveEmployee':
        post = parameters['poste']
        optionregulier = parameters['optionregulier']
        jours = parameters['jours']
        optionsicouchante = parameters['optionsicouchante']
        optionmobilite = parameters['optionmobilite']
        location = parameters['location']
        typebudget = parameters['typebudget']  # Is not on Google Sheets
        budget = parameters['number']
        name = None
        phoneNumber = None
        nounoulocation = parameters['nounoulocation']

        database_info = []
        database_info.extend([post,optionregulier,jours,optionsicouchante,optionmobilite,location,budget,name,phoneNumber,nounoulocation])
        response = insertrow(database_info)
        print(response)
        message = messageconstruct([response])
        return message


if __name__ == '__main__':
    app.run()




