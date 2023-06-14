#!/bin/bash
sudo yum update -y
sudo yum install python3-pip -y
pip3 install urllib3==1.26.15
pip3 install mlflow boto3 psycopg2-binary