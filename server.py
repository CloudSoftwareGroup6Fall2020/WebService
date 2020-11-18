from flask import Flask

app = Flask(__name__, static_folder='static')

@app.route("/")
def index():
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