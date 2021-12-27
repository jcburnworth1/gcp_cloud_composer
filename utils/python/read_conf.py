## Import Libraries
from google.cloud import storage
import os
import json

class read_conf():

    ## Initilize GCS client and get bucket details
    def __init__(self):
        self.client = storage.Client()
        self.bucket_name = os.environ['GCS_BUCKET']
        self.bucket = self.client.get_bucket(os.environ['GCS_BUCKET'])
        self.item = self.get_environ()

    def get_default_args(self):
        blob = self.bucket.blob(self.item)
        conf = json.loads(blob.download_as_string())

        return conf

    def get_environ(self):
        if self.bucket_name == 'us-central1-composer-burnwo-db1f01e8-bucket':
            item = 'dags/conf/conf-prod.json'
        elif self.bucket_name == 'test-bucket':
            item = 'dags/conf/conf-test.json'
        else:
            item = 'dags/conf/conf-dev.json'

        return item