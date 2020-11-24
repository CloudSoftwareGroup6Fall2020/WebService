from flask import Flask
import os, datetime, sys
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from flask_sqlalchemy import SQLAlchemy

server = 'group6project.database.windows.net'
database = 'cloudprojectdb'
username = os.environ.get('sql_username')
password = os.environ.get('sql_password')
driver= 'ODBC+Driver+17+for+SQL+Server'
connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}"
engine = SQLAlchemy.create_engine(SQLAlchemy, connection_string, {})

try:
    connection = engine.connect()
except Exception as ex:
    print('Database connection FAILED!:')
    print(ex)
    sys.exit()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = server
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    #No idea what this does, but it's set to false to suppress deprecation warning.
db = SQLAlchemy(app)

connection_string_blob = 'DefaultEndpointsProtocol=https;AccountName=cs71003bffda805345c;AccountKey=KdCm90f50B+/59bmb7F8A97ATIxbfMhHlz41BN4jpTR9bQKT5Bjp9yfPeZKYXDG613JQPoQHoe1lesbFjoADCA==;EndpointSuffix=core.windows.net'
# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connection_string_blob)

# Create a unique name for the container
container_name = "blobcontainer8b009926-54c3-4286-858b-daabadfe43f3"

# Create a file in local data directory to upload and download
image_path = './images'
file_names = os.listdir(image_path)

print("\nBeginning File Upload...")
for file in file_names:
    upload_file_path = os.path.join(image_path, file)
    temp = upload_file_path.split('\\')
    img_name = temp[len(temp) - 1]
    img_type = img_name.split('.')[1]
    img_name = img_name.split('.')[0]
    img_path = 'https://cs71003bffda805345c.blob.core.windows.net/' + container_name + '/' + img_name + '.' + img_type

    # Create a blob client using the local file name as the name for the blob
    blob_service_client = BlobServiceClient.from_connection_string(connection_string_blob)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=img_name + '.' + img_type)

    try:
        # Upload the created file
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)
        print(f"{img_name}.{img_type} uploaded to storage account as blob!")
    except Exception as ex:
        print('Blob upload failed!')
        print(ex)
        sys.exit()

    # Add entry to database
    response = engine.execute('SELECT MAX(id) FROM Images')

    val = 0
    for rowproxy in response:
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
            val = value
    img_id = val + 1

    engine.execute(f"INSERT INTO Images (id, name, img_type, upload_date, path) VALUES ('{img_id}', '{img_name}', '{img_type}', '{str(datetime.datetime.now())[0: 22]}', '{img_path}')")
    print(f"**SUCCESS {img_name}.{img_type} added to database successfully!")

