import requests
import boto3
import os

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-1'
)

lambda_client = boto3.client(
    "lambda",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-1'
)

class Client():
    def __init__(self, name, token):
        self.name = name
        self.token = token
    
    def deploy(self, model_path, dependencies_path, proj_name, model_name):
        url = "http://localhost:3000/api/model/deploy"

        data = {
            "secretAccessToken": self.token, 
            "proj_name": proj_name,
            "model_name": model_name,
        }

        files = {
            "model": open(model_path, "rb"),
            "dependencies": open(dependencies_path, "rb")
        }

        response = requests.post(url=url, data=data, files=files)
        return response.text

