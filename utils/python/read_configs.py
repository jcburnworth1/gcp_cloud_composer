## Import Libraries
from google.cloud import storage
import os
import json
from typing import Dict

class Configuration:

    def __init__(self):
        """
        Initialize GCS client and get bucket details during instantiation
        """
        self.client = storage.Client()
        self.bucket_name = os.environ['GCS_BUCKET']
        self.bucket = self.client.get_bucket(os.environ['GCS_BUCKET'])
        self.environ = self.get_environ()

    def get_environ(self) -> str:
        """
        Upon object instantiation, determine proper environment
        :return: prod, test, or dev
        """
        if self.bucket_name == 'us-central1-composer-burnwo-db1f01e8-bucket':
            environ = 'prod'
        elif self.bucket_name == 'test-bucket':
            environ = 'test'
        else:
            environ = 'dev'

        return environ

    def get_default_args(self) -> Dict:
        """
        Load default default_args from GCS bucket
        :return: Dict of default default_args
        """
        if self.environ == 'prod':
            args = 'dags/default_args/default-args-prod.json'
        elif self.environ == 'test':
            args = 'dags/default_args/default-args-test.json'
        else:
            args = 'dags/default_args/default-args-dev.json'

        blob = self.bucket.blob(args)
        default_args = json.loads(blob.download_as_string())

        return default_args

    def get_params(self) -> Dict:
        """
        Load default params
        :return: Dict of default params
        """
        if self.environ == 'prod':
            params = 'dags/params/params-prod.json'
        elif self.environ == 'test':
            params = 'dags/params/params-test.json'
        else:
            params = 'dags/params/params-dev.json'

        blob = self.bucket.blob(params)
        params = json.loads(blob.download_as_string())

        return params

    def get_markdown(self, md_file: str = None) -> str:
        """
        Load DAG specific markdown
        :return: Sting variable with markdown
        """
        with open(f'dags/markdowns/{md_file}', 'r') as f:
            doc = f.read()

        return doc