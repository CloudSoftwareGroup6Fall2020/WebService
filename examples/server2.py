from flask import Flask
import pyodbc

server = 'group6project.database.windows.net'
database = 'cloudprojectdb'
username = '*INSERT USERNAME HERE*'
password = '*INSERT PASSWORD HERE*'
driver= '{ODBC Driver 17 for SQL Server}'

response = []
with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Test")
        row = cursor.fetchone()
        while row:
            response.append(str(row[0]))
            row = cursor.fetchone()

app = Flask(__name__)

@app.route("/")
def index():
    # print(response[0])
    str1 = ''
    for val in response:
        str1 += val + ' '
    return "<h1>Hello There!</h1>" + str1

@app.route("/page1")
def page1():
    return "<img src=\"https://INSERT_IMG_URL_HERE" style=\"width:10%;height:10%;\">"

if __name__ == "__main__":
    app.run()