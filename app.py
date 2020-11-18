from flask import Flask
from flask.wrappers import Response
import pyodbc, random

try:
    server = 'group6project.database.windows.net'
    database = 'cloudprojectdb'
    username = '*INSERT USERNAME HERE*'
    password = '*INSERT PASSWORD HERE*'
    driver= '{ODBC Driver 17 for SQL Server}'

except Exception as ex:
    print('Exception:')
    print(ex)

connection_string_blob = 'DefaultEndpointsProtocol=https;AccountName=cs71003bffda805345c;AccountKey=KdCm90f50B+/59bmb7F8A97ATIxbfMhHlz41BN4jpTR9bQKT5Bjp9yfPeZKYXDG613JQPoQHoe1lesbFjoADCA==;EndpointSuffix=core.windows.net'

response = ""
with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        query = f"SELECT * from Images"
        cursor.execute(query)
        row = cursor.fetchall()
        i = 0
        for var in row:
            if (i == 0):
                i += 1
                continue
            j = 0
            for var in row[i]:
                if (j == 3):
                    temp = str(row[i][j]).split()
                    row[i][j] = temp[0] + ' ' + temp[1]
                else:
                    temp = str(row[i][j]).split()
                    row[i][j] = temp[0]
                j += 1
            i += 1
        response = row

app = Flask(__name__, static_folder='static')

previous = 0
@app.route("/")
def index():
    global previous
    i = previous
    while i == previous:
        i = random.randint(1, len(response) - 1)
    previous = i

    image_url_index = 4
    return """<!DOCTYPE html>
            <html>
                <head>
                    <title>indexPage</title>
                        <link href = "static/format.css" type="text/css" rel="stylesheet">       
                </head>
                
                <body>
                    <div class='container'>
                        <div class='button'>
                            <button style='background-color:blanchedalmond;' onclick="location.href='/';">Random</button>
                            <button onclick="location.href='/search';">Search</button>
                            <button onclick="location.href='/browse';">Browse</button>
                            <button onclick="location.href='/upload';">Upload</button>
                        </div>
                    </div>
                    <img src='"""+ response[i][image_url_index] +"""'>
                </body>
            </html>"""

@app.route("/search")
def search():
    return """<!DOCTYPE html>
                <html>
                    <head>
                        <title>searchPage</title>
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
                        <div class='container'>
                            <div class='button'>
                                <button onclick="location.href='/';">Random</button>
                                <button style='background-color:blanchedalmond;' onclick="location.href='/search';">Search</button>
                                <button onclick="location.href='/browse';">Browse</button>
                                <button onclick="location.href='/upload';">Upload</button>
                                <br />
                                <br />
                                <br />
                                <form method='POST' action=''>
                                    <input type='text' placeholder='Search by ID'></input>
                                    <button class='submit' name='id' type='submit'>Submit</button>
                                    <br />
                                    <br />
                                    <br />
                                    <input type='text' placeholder='Search by Name'></input>
                                    <button class='submit' name='name' type='submit'>Submit</button>
                                </form>
                            </div>
                        </div>
                    </body>
                </html>"""

@app.route("/browse")
def browse():
    return """<!DOCTYPE html>
                <html>
                    <head>
                        <title>browsePage</title>
                            <link href = "static/format.css" type="text/css" rel="stylesheet">       
                    </head>
                    
                    <body>
                        <div class='container'>
                            <div class='button'>
                                <button onclick="location.href='/';">Random</button>
                                <button onclick="location.href='/search';">Search</button>
                                <button style='background-color:blanchedalmond;' onclick="location.href='/browse';">Browse</button>
                                <button onclick="location.href='/upload';">Upload</button>
                            </div>
                        </div>
                        <div class='container'>
                            <table>
                                <tr>
                                    <td>1</td>
                                    <td>2</td>
                                </tr>
                                <tr>
                                    <td>3</td>
                                    <td>4</td>
                                </tr>
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
                            <link href = "static/format.css" type="text/css" rel="stylesheet">       
                    </head>
                    
                    <body>
                        <div class='container'>
                            <div class='button'>
                                <button onclick="location.href='/';">Random</button>
                                <button onclick="location.href='/search';">Search</button>
                                <button onclick="location.href='/browse';">Browse</button>
                                <button style='background-color:blanchedalmond;' onclick="location.href='/upload';">Upload</button>
                                <br />
                                <br />
                                <br />
                                <form method='POST' action=''>
                                    <input type='text' placeholder='Upload'></input>
                                    <button class='submit' name='upload' type='submit'>Submit</button>
                                </form>
                            </div>
                        </div>
                    </body>
                </html>"""
if __name__ == "__main__":
    app.run()