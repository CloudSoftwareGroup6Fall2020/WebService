from flask import Flask
from flask import request, redirect
import random, requests, os
from flask import json
from flask.helpers import url_for

app = Flask(__name__, static_folder='static')

api_url = 'https://cloudsoftwareprojectgroup6api.azurewebsites.net'
uri_images = 'images'

previous = 0
@app.route("/")
def index():
    response = requests.get(f"{api_url}/{uri_images}/count")
    img_count = response.json()[0]['count']
    global previous
    i = previous
    while i == previous:
        i = random.randint(1, img_count-1)
    previous = i

    response = requests.get(f"{api_url}/{uri_images}/{i}")
    img_src = response.json()[0]['path']
    return """<!DOCTYPE html>
                <html>
                    <head>
                        <title>indexPage</title>
                            <!--All cats photos used are BSD Licensed (EAST BAY WOOPWOOP) https://github.com/maxogden/cats -->
                            <link href = "static/format.css" type="text/css" rel="stylesheet">
                    </head>
                    
                    <body>
                        <p>All cats photos used are BSD Licensed (EAST BAY WOOPWOOP) https://github.com/maxogden/cats</p>
                        <div class='container'>
                            <div class='button'>
                                <button style='background-color:blanchedalmond;' onclick="location.href='/';">Random</button>
                                <button onclick="location.href='/search';">Search</button>
                                <button onclick="location.href='/browse';">Browse</button>
                                <button onclick="location.href='/upload';">Upload</button>
                            </div>
                        </div>
                        <img src='""" + img_src + """'>
                    </body>
                </html>"""

@app.route("/search")
def search():
    return """<!DOCTYPE html>
                <html>
                    <head>
                        <title>searchPage</title>
                            <!--All cats photos used are BSD Licensed (EAST BAY WOOPWOOP) https://github.com/maxogden/cats -->
                            <link href = "static/format.css" type="text/css" rel="stylesheet">       
                            <style>
                                submit{
                                    width: 10%;
                                    border: 1px solid #aaa;
                                    border-radius: 4px;
                                    margin: 7px;
                                    padding: 7px;
                                    box-sizing: border-box;
                                    float: center;
                                    height: 2em;
                                    
                                }
                            </style>
                        </head>
                    
                    <body>
                        <p>All cats photos used are BSD Licensed (EAST BAY WOOPWOOP) https://github.com/maxogden/cats</p>
                        <div class='container'>
                            <div class='button'>
                                <button onclick="location.href='/';">Random</button>
                                <button style='background-color:blanchedalmond;' onclick="location.href='/search';">Search</button>
                                <button onclick="location.href='/browse';">Browse</button>
                                <button onclick="location.href='/upload';">Upload</button>
                                <br />
                                <br />
                                <br />
                                <form method='POST' action='"""+url_for('GetImageByID')+"""'>
                                    <input type='text' placeholder='Search by ID' name='id'></input>
                                    <button class='submit' type='submit'>Submit</button>
                                </form>
                                <br />
                                <br />
                                <br />
                                <form method='POST' action='"""+url_for('GetImageByName')+"""'>
                                    <input type='text' placeholder='Search by Name' name='name'></input>
                                    <button class='submit' name='name' type='submit'>Submit</button>
                                </form>
                            </div>
                        </div>
                    </body>
                </html>"""

@app.route("/browse")
def browse():
    response = requests.get(f"{api_url}/images/count")
    img_count = response.json()[0]['count']
    response = requests.get(f"{api_url}/images")
    col_count = 3
    i = 1
    data = ''
    numRows = 0
    if (img_count % col_count == 0):
        numRows = int(img_count / col_count) + 1
    else:
        numRows = int(img_count / col_count) + 2
    for row in range(1, numRows):
        data += '<tr>'
        for col in range(col_count):
            if (i == img_count):
                break
            img_src = response.json()[i]['path']
            data += '<td>'
            data += f"<img src=\'{img_src}\'>"
            data += '</td>'
            i += 1
        data += '</tr>'


    return """<!DOCTYPE html>
                <html>
                    <head>
                        <title>browsePage</title>
                        <!--All cats photos used are BSD Licensed (EAST BAY WOOPWOOP) https://github.com/maxogden/cats -->
                            <link href = "static/format.css" type="text/css" rel="stylesheet">   
                    </head>
                    
                    <body>
                        <p>All cats photos used are BSD Licensed (EAST BAY WOOPWOOP) https://github.com/maxogden/cats</p>
                        <div class='container'>
                            <div class='button'>
                                <button onclick="location.href='/';">Random</button>
                                <button onclick="location.href='/search';">Search</button>
                                <button style='background-color:blanchedalmond;' onclick="location.href='/browse';">Browse</button>
                                <button onclick="location.href='/upload';">Upload</button>
                            </div>
                        </div>
                        <div class='container'>
                            <table>"""+ data +"""
                            </table>
                        </div>
                    </body>
                </html>"""

@app.route("/upload")
def upload():
    return """<!DOCTYPE html>
                <html>
                    <head>
                        <title>indexPage</title>
                        <!--All cats photos used are BSD Licensed (EAST BAY WOOPWOOP) https://github.com/maxogden/cats -->
                            <link href = "static/format.css" type="text/css" rel="stylesheet">
                    </head>
                    
                    <body>
                        <p>All cats photos used are BSD Licensed (EAST BAY WOOPWOOP) https://github.com/maxogden/cats</p>
                        <div class='container'>
                            <div class='button'>
                                <button onclick="location.href='/';">Random</button>
                                <button onclick="location.href='/search';">Search</button>
                                <button onclick="location.href='/browse';">Browse</button>
                                <button style='background-color:blanchedalmond;' onclick="location.href='/upload';">Upload</button>
                                <br />
                                <br />
                                <br />
                                <form method='POST' action='"""+ url_for('UploadImage') +"""'>
                                    <input type='file' placeholder='Upload' name='file' accept="image/*"></input>
                                    <button class='submit' name='upload' type='submit'>Submit</button>
                                </form>
                            </div>
                        </div>
                    </body>
                </html>"""

@app.route("/uploadImage", methods=['POST'])
def UploadImage():
    file = request.files['file']
    escape(os.path.abspath(file) + file)
    response = requests.post(f"{api_url}/{uri_images}/upload/{newStr}")

def escape(str1):
    global newStr
    for character in str1:
        if (character == ':'):
            split = str1.split(':')
            newStr = split[0] + '&#58;' + split[1]
            escape(newStr)
            break
        if (character == '/'):
            split = str1.split('/')
            index = 0
            temp = ''
            for slash in split:
                if (index == len(split)):
                    continue
                if (index > 0):
                    temp += '&#47;' + split[index]
                    index += 1
                else:
                    temp += split[index] + '&#47;' + split[index + 1]
                    index += 2
            newStr = temp
            escape(newStr)
            break
        if (character == '.'):
            split = str1.split('.')
            newStr = split[0] + '&#46;' + split[1]
            return newStr
        


@app.route('/GetImageByID', methods=['POST'])
def GetImageByID():
    id = int(request.form['id'])
    response = requests.get(f"{api_url}/{uri_images}/count")
    img_count = int(response.json()[0]['count'])
    if (id < 1 or id > img_count):
        return redirect(url_for('search'), code=302)
    response = requests.get(f"{api_url}/{uri_images}/{id}")
    img_src = response.json()[0]['path']
    return """<!DOCTYPE html>
                <html>
                    <head>
                        <title>searchPage</title>
                            <!--All cats photos used are BSD Licensed (EAST BAY WOOPWOOP) https://github.com/maxogden/cats -->
                            <link href = "static/format.css" type="text/css" rel="stylesheet">       
                            <style>
                                submit{
                                    width: 10%;
                                    border: 1px solid #aaa;
                                    border-radius: 4px;
                                    margin: 7px;
                                    padding: 7px;
                                    box-sizing: border-box;
                                    float: center;
                                    height: 2em;
                                    
                                }
                            </style>
                        </head>
                    
                    <body>
                        <p>All cats photos used are BSD Licensed (EAST BAY WOOPWOOP) https://github.com/maxogden/cats</p>
                        <div class='container'>
                            <div class='button'>
                                <button onclick="location.href='/';">Random</button>
                                <button style='background-color:blanchedalmond;' onclick="location.href='/search';">Search</button>
                                <button onclick="location.href='/browse';">Browse</button>
                                <button onclick="location.href='/upload';">Upload</button>
                                <br />
                                <br />
                                <br />
                                <form method='POST' action='"""+url_for('GetImageByID')+"""'>
                                    <input type='text' placeholder='Search by ID' name='id'></input>
                                    <button class='submit' type='submit'>Submit</button>
                                </form>
                                <br />
                                <br />
                                <br />
                                <form method='POST' action='"""+url_for('GetImageByName')+"""'>
                                    <input type='text' placeholder='Search by Name' name='name'></input>
                                    <button class='submit' name='name' type='submit'>Submit</button>
                                </form>
                            </div>
                        </div>
                        <div class='container'>
                            <img src='"""+ img_src +"""'>
                        </div>
                    </body>
                </html>"""

@app.route('/GetImageByName', methods=['POST'])
def GetImageByName():
    name = request.form['name']
    response = requests.get(f"{api_url}/{uri_images}/{name}")
    if (response.status_code == 404):
        return redirect(url_for('search'), code=302)
    imageList = []
    for image in response.json():
        imageList.append(image['path'])
    img_count = len(imageList)
    col_count = 3
    img_src = ''
    data = ''
    
    if (img_count == 1):
        img_src = imageList.pop()
        data = f"<img src=\'{img_src}\'>"
    else:
        data = '<table>'
        numRows = 0

        if (img_count % col_count == 0):
            numRows = int(img_count / col_count) + 1
        else:
            numRows = int(img_count / col_count) + 2

        i = 1
        for row in range(1, numRows):
            data += '<tr>'
            for col in range(col_count):
                if (i == img_count + 1):
                    break
                img_src = imageList.pop()
                data += '<td>'
                data += f"<img src=\'{img_src}\'>"
                data += '</td>'
                i += 1
            data += '</tr></table>'

    return """<!DOCTYPE html>
                <html>
                    <head>
                        <title>searchPage</title>
                            <!--All cats photos used are BSD Licensed (EAST BAY WOOPWOOP) https://github.com/maxogden/cats -->
                            <link href = "static/format.css" type="text/css" rel="stylesheet">       
                            <style>
                                submit{
                                    width: 10%;
                                    border: 1px solid #aaa;
                                    border-radius: 4px;
                                    margin: 7px;
                                    padding: 7px;
                                    box-sizing: border-box;
                                    float: center;
                                    height: 2em;
                                    
                                }
                            </style>
                        </head>
                    
                    <body>
                        <p>All cats photos used are BSD Licensed (EAST BAY WOOPWOOP) https://github.com/maxogden/cats</p>
                        <div class='container'>
                            <div class='button'>
                                <button onclick="location.href='/';">Random</button>
                                <button style='background-color:blanchedalmond;' onclick="location.href='/search';">Search</button>
                                <button onclick="location.href='/browse';">Browse</button>
                                <button onclick="location.href='/upload';">Upload</button>
                                <br />
                                <br />
                                <br />
                                <form method='POST' action='"""+url_for('GetImageByID')+"""'>
                                    <input type='text' placeholder='Search by ID' name='id'></input>
                                    <button class='submit' type='submit'>Submit</button>
                                </form>
                                <br />
                                <br />
                                <br />
                                <form method='POST' action='"""+url_for('GetImageByName')+"""'>
                                    <input type='text' placeholder='Search by Name' name='name'></input>
                                    <button class='submit' name='name' type='submit'>Submit</button>
                                </form>
                            </div>
                        </div>
                        <div class='container'>
                            <table>"""+ data +"""
                            </table>
                        </div>
                    </body>
                </html>"""
if __name__ == "__main__":
    app.run()