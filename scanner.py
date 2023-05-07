import requests
import json


with open("APIKEYS.json", 'r') as f:
    data = json.load(f)
    license_code = data["license_code"]
    user_name = data["user_name"]


def scan(img):
    request_url = 'http://www.ocrwebservice.com/restservices/processDocument?language=russian&outputformat=txt&gettext=true'
    with open(img, 'rb') as image_file:
        image_data = image_file.read()
    r = requests.post(request_url, data=image_data, auth=(user_name, license_code))
    job_j = json.loads(r.content)
    try:
        output = str(job_j["OCRText"][0][0])
    except IndexError:
        print("количество запросов закончилось")
        output = ''
    print("Еще можно сканить: " + str(job_j["AvailablePages"]))
    print(output)
    return output
