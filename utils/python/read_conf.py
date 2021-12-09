## Import Libraries
from google.cloud import storage
import os
import json

class read_conf():

    ## Initilize GCS client and get bucket details
    def __init__(self):
        client = storage.Client()
        self.client = client
        self.bucket_name = os.environ['GCS_BUCKET']
        self.bucket = client.get_bucket(os.environ['GCS_BUCKET'])
        self.item = 'dags/conf/conf-prod.json'

    def get_default_args(self):
        blob = self.bucket.blob(self.item)
        conf = json.loads(blob.download_as_string())

        return conf