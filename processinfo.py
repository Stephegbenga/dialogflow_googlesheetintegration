import difflib
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def getdatafromsheet():
    response = []
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Copie de Recherche nounou").sheet1
    results = sheet.get_all_records()
    for result in results:
        data_array = f"{result['type_de_poste']}, {result['ville']}, {result['optionsicouchante']}, {result['optionsireguliere']}".replace(',', '').split()
        data = {"name":result['nom'],"data":data_array}
        response.append(data)
    return response

def getsimilarwords(incomingwords):
    result = []
    words = getdatafromsheet()
    for word in words:
        for incomingword in incomingwords:
            testt = difflib.get_close_matches(incomingword, word['data'])
            if testt != []:
                print(f"{word['name']} --> {testt}")
                result.append(incomingword)
    return result

information = getsimilarwords(['iiididid'])
print(len(information))
