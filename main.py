import json
import openai
import shutil
import requests
from PyQt5.QtWidgets import QApplication, QFileDialog

app = QApplication([])
N = input("Кол-во фото")
photos_path = []
for i in range(N):
    photo = QFileDialog.getOpenFileName()[0]
    photos_path.append(photo)


def scan(photos_path):
    LicenseCode = 'C43B927C-C9E8-4342-BCC4-118FD066A10C'
    UserName = 'FEDAAAA'
    RequestUrl = 'http://www.ocrwebservice.com/restservices/processDocument?language=russian&outputformat=txt&gettext=true'
    output = ''
    for i in photos_path:
        FilePath = i
        with open(FilePath, 'rb') as image_file:
            image_data = image_file.read()
        r = requests.post(RequestUrl, data=image_data, auth=(UserName, LicenseCode))
        jobj = json.loads(r.content)
        try:
            output = str(jobj["OCRText"][0][0])
        except IndexError:
            print("количество запросов закончилось")
            output = ''
        print("Еще можно сканить:" + str(jobj["AvailablePages"]))
        for i, elem in enumerate(output):
            if elem == "V" or elem == 'v' or elem == 'i' or elem == "I":
                if i == 0:
                    output += output[i + 1:]
                output += output[:i] + output[i + 1:]

    return output


model_engine = "text-davinci-003"
openai.api_key = "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"
option = ''


def request(b, tokens):
    global option
    c = ''
    if option != '':
        option = 'В стиле ' + option
    for i in range(len(b)):
        completion = openai.Completion.create(
            engine=model_engine,
            prompt='Привет, можешь, пожалуйста, выделить самое главное в этом тексте: ' + b[i] + '.' + option,
            max_tokens=tokens,  # по сути, от 256 до 4096
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        c += completion.choices[0].text
    return c


data = scan(photos_path)
print(data)
data = data.split('. ')
sum = 0
big_data = ['']
for i in data:
    if sum + len(i) < 1536:
        sum += len(i)
        big_data[len(big_data) - 1] += i
    else:
        big_data.append(i)
        sum = 0
print(request(big_data, tokens=2048))
