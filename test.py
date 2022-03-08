from flask import Flask,request,jsonify
import boto3
import sys
import logging
import botocore.exceptions
from config import config

app = Flask(__name__)

logging.basicConfig(filename='record.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(threadName)-10s %(message)s',)
 

config2=[]
@app.route('/ec2/list',methods=["GET","POST"])
def endPoint1():


    aws_access_key_id= request.args.get('aws_access_key_id')
    aws_secret_access_key= request.args.get('aws_secret_access_key')
    region_name= request.args.get('region_name')
    config2.append(aws_secret_access_key)

    try:
        ec2 = boto3.client('ec2',
                   region_name,
                   aws_access_key_id=str(aws_access_key_id),
                   aws_secret_access_key=config['aws_secret_access_key'])
    
        response = ec2.describe_instances()
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                print("instance id : " + instance["InstanceId"])
                print(config2[0])
    except botocore.exceptions.ParamValidationError as error:
        raise ValueError('The parameters you provided are incorrect: {}'.format(error))
    
    return "succesfull"

@app.route('/ec2/start',methods=["GET","POST"])
def endPoint2():
    
    aws_access_key_id= request.args.get('aws_access_key_id')
    aws_secret_access_key = request.args.get('aws_secret_access_key')
    region_name= request.args.get('region_name')
    InstanceId= request.args.get('InstanceId')
    try:
        ec2 = boto3.client('ec2',
                   region_name,
                   aws_access_key_id=str(aws_access_key_id),
                   aws_secret_access_key=config["aws_secret_access_key"])
    

        ec2.start_instances(InstanceIds=[InstanceId])
    except Exception as e:
        print("error")
    return"operation successful"

@app.route('/ec2/stop',methods=["GET","POST"])
def endPoint3():
    
    aws_access_key_id= request.args.get('aws_access_key_id')
    aws_secret_access_key = request.args.get('aws_secret_access_key')
    region_name= request.args.get('region_name')
    InstanceId = request.args.get('InstanceId')
    try:
        ec2 = boto3.client('ec2',
                   region_name,
                   aws_access_key_id=aws_access_key_id,
                   aws_secret_access_key=config["aws_secret_access_key"])

        ec2.stop_instances(InstanceIds=[InstanceId])
    except Exception as e:
        print(e)
        
    
    return "operation successful"

 
if __name__ == "__main__":
    app.run(host=config["host"], port=config["port"], debug=True)
