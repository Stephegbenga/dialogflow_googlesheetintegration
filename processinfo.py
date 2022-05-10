import difflib
import gspread
from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials

# Get Data From Google Sheet
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

def opensheet(sheet):
    sheet = client.open("Recherche nounou").worksheet(sheet)
    return sheet

def getdatafromsheet():
    response = []
    sheet = opensheet("employees_2")
    results = sheet.get_all_records()
    for result in results:
        if result['optioncouchante'] == 'non couchante':
            result['optioncouchante'] = 'conotconcho'
        if result['optionregulier'] == 'non regulier':
            result['optionregulier'] = 'rekolarni'
        data = {"name":result['name'],"location":result['location'], "reg_option": result['optionregulier'],"couch":result['optioncouchante'], "optionmobilite":result['optionmobilite'], "phonenumber":result['phone number'], "post":result['poste']}
        response.append(data)
    print(response)
    return response


# Get The Nearly Similar Words
def getsimilarwords(incomingword):
    result = []
    final_result =[]
    sheet_datas = getdatafromsheet()
    for sheet_data in sheet_datas:
        location_t = difflib.get_close_matches(incomingword['location'], [sheet_data['location']])
        post_t = difflib.get_close_matches(incomingword['post'], [sheet_data['post']])
        reg_option_t = difflib.get_close_matches(incomingword['reg_option'], [sheet_data['reg_option']])
        couch_t = difflib.get_close_matches(incomingword['couch'], [sheet_data['couch']])

        print(f"results after diff Location -> {location_t},  post -> {post_t} reg_option -> {reg_option_t} Couch -> {couch_t}")

        if location_t != [] and post_t != [] and reg_option_t != [] and couch_t != []:
            print(sheet_data)
            result.append(sheet_data)
    for i in range(len(result)):
        if result[i] not in final_result:
            final_result.append(result[i])
    return final_result


def insertrow(row):
    sheet = opensheet("employees_2")
    sheet.append_row(row)
    return "Your information were stored on the database Successfully"


# rowtobeinserrted = ['I', 'love', 'mercy']
# result = insertrow(rowtobeinserrted)
# print(result)
# if result:
#     print("Your information were stored on the database Succssfully")
# else:
#     print("Unable to store these information on the database")