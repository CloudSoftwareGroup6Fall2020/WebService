import os, uuid, datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import pyodbc

try:
    server = 'group6project.database.windows.net'
    database = 'cloudprojectdb'
    username = os.environ.get('sql_username')
    password = os.environ.get('sql_password')
    driver= '{ODBC Driver 17 for SQL Server}'

    connection_string_blob = 'DefaultEndpointsProtocol=https;AccountName=cs71003bffda805345c;AccountKey=KdCm90f50B+/59bmb7F8A97ATIxbfMhHlz41BN4jpTR9bQKT5Bjp9yfPeZKYXDG613JQPoQHoe1lesbFjoADCA==;EndpointSuffix=core.windows.net'
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string_blob)

    # Create a unique name for the container
    container_name = "imageblob" + str(uuid.uuid4())

    # Create the container
    container_client = blob_service_client.create_container(container_name, public_access='blob')
    # Create a file in local data directory to upload and download
    image_path = './data/images'
    file_names = os.listdir(image_path)

    for file in file_names:
        local_file_name = file
        upload_file_path = os.path.join(image_path, local_file_name)

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

        print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

        # Upload the created file
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)

        temp = file.split('.')
        name = temp[0]
        img_type = temp[1]
        path = 'https://cs71003bffda805345c.blob.core.windows.net/' + container_name + '/' + file
        with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                query = f"SELECT MAX(id) FROM Images"
                cursor.execute(query)
                row = cursor.fetchone()
                id = int(row[0]) + 1
                query = f"INSERT INTO Images (id, name, img_type, upload_date, path) VALUES ('{id}', '{name}', '{img_type}', '{str(datetime.datetime.now())[0: 22]}', '{path}')"
                cursor.execute(query)

        print("\nListing blobs...")

        # List the blobs in the container
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            print("\t" + blob.name)
except Exception as ex:
    print('Exception:')
    print(ex)