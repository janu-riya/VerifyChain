import requests
from fastapi import FastAPI,File , UploadFile,Form, Query, HTTPException, Depends, status, Cookie
from pydantic import BaseModel
from typing import Dict, Optional
from random import choice
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
from pymongo import MongoClient
from datetime import timedelta, datetime
from io import StringIO
from fastapi.exceptions import HTTPException
import pandas as pd
import os
import configparser
from graph import Graph
import boto3
import hashlib
import tempfile
import botocore
from typing import List,Dict , Optional
from fastapi.responses import JSONResponse
from bson import ObjectId
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uvicorn
import io
import string
import random
import json
import re
import yagmail
import smtplib
import jwt
from decouple import config
import key_config as keys
from datetime import datetime, timedelta
import traceback
import threading
from numbers import Real

client = MongoClient('mongodb://localhost:27017/')
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=int, default=30)
COOKIE_DOMAIN = config('COOKIE_DOMAIN', default=None)

##############################S3 bucket #############################
AWS_REGION = "ap-south-1"

s3 = boto3.client('s3',
                    aws_access_key_id = keys.ACCESS_KEY_ID,
                    aws_secret_access_key = keys.ACCESS_SECRET_KEY,
                    region_name=AWS_REGION,
                    config=botocore.client.Config(signature_version='s3v4')
                    )

BUCKET_NAME = 'verifiedge'

origins = [
    "http://localhost:3000",
]


##############################################################################################
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )

# Replace these variables with your actual Gmail credentials
GMAIL_USERNAME = "verifyedge13@gmail.com"
GMAIL_PASSWORD = "kkddrgykwqizejec"

class EmailData(BaseModel):
    email: str
    email_subject: str
    email_body: str

@app.post("/send_rejection_email")
async def send_rejection_email(send: EmailData):
    # Replace the following with your email server settings
    email_server = 'smtp.gmail.com'
    email_port = 587
    email_sender = 'verifyedge13@gmail.com'
    email_password = 'kkddrgykwqizejec'

    email = send.email
    email_subject = send.email_subject
    email_body = send.email_body
    try:
        # Set up the email
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email
        msg['Subject'] = email_subject

        # Attach the body to the email
        msg.attach(MIMEText(email_body, 'plain'))

        # Connect to the email server and send the email
        server = smtplib.SMTP(email_server, email_port)
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email, msg.as_string())
        server.quit()

        return {"message": "Rejection email sent successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send the email: {e}")



########################Converting into Hash##############################
@app.get("/Hash/S3files")
async def Hash_S3files(email: Optional[str] = None, regno: Optional[str] = None):
    s3_key = f"{email}/{regno}/"
    try:
        # Check if any objects exist in the specified folder in S3
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=s3_key)
        if 'Contents' in response:
            # Get the first file in the folder (assuming only one file exists)
            filename = response['Contents'][0]['Key'].split('/')[-1]
            # Create a temporary file to download the S3 file
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                # Download the S3 object to the temporary file
                s3.download_fileobj(BUCKET_NAME, s3_key + filename, tmp_file)
                hash_value = hashlib.sha256(tmp_file.read()).hexdigest()

            # Return the temporary file as a downloadable response with the correct content headers
            return hash_value
        # If no files are present in the folder, raise an HTTP 404 error
        raise HTTPException(status_code=404, detail="File not found")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            # If the object is not found (404 error), raise an HTTP 404 error
            raise HTTPException(status_code=404, detail="File not found")
        # For other exceptions, raise an HTTP 500 error
        raise HTTPException(status_code=500, detail=str(e))

######################## Upload Files to S3 Bucket #########################

def upload_file_to_s3(file, email, regno):
    file_key = f"{email}/{regno}/{file.filename}"
    # Upload the file to S3 bucket
    s3.upload_fileobj(file.file, BUCKET_NAME, file_key)

def is_pdf_file(file: UploadFile) -> bool:
    # Check if the file is a PDF based on its content type
    return file.content_type == "application/pdf"

@app.post("/uploadfile/S3")
async def upload(email : str = Form(), regno : str = Form(), file: UploadFile = File(...)):
    
    try:
        if not is_pdf_file(file):
            return {"pdf": False}
        # Create the user folder if it doesn't exist
        user_folder = f"{email}/{regno}"
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        upload_file_to_s3(file, email, regno)
        return True
    except Exception as e:
        print(str(e))
        return False


############################# Get Files from s3 #########################
@app.get("/download/S3files")
async def download_file(email: Optional[str] = None, regno: Optional[str] = None):
    s3_key = f"{email}/{regno}/"
    try:
        # Check if any objects exist in the specified folder in S3
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=s3_key)
        if 'Contents' in response:
            # Get the first file in the folder (assuming only one file exists)
            filename = response['Contents'][0]['Key'].split('/')[-1]
            # Create a temporary file to download the S3 file
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                # Download the S3 object to the temporary file
                s3.download_fileobj(BUCKET_NAME, s3_key + filename, tmp_file)
                hash_value = hashlib.sha256(tmp_file.read()).hexdigest()

            # Return the temporary file as a downloadable response with the correct content headers
            return FileResponse(tmp_file.name, filename=filename)
        # If no files are present in the folder, raise an HTTP 404 error
        raise HTTPException(status_code=404, detail="File not found")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            # If the object is not found (404 error), raise an HTTP 404 error
            raise HTTPException(status_code=404, detail="File not found")
        # For other exceptions, raise an HTTP 500 error
        raise HTTPException(status_code=500, detail=str(e))



########################### Check Whether file exist on S3 Bucket ##############################
@app.get("/check-s3-folder")
async def check_s3_folder(email: Optional[str] = None, regno: Optional[str] = None):
    folder_key = f"{email}/{regno}/"
    try:
        # Check if any objects exist in the specified folder in S3
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=folder_key)
        # If any files are present in the folder, return "file_present": true
        if 'Contents' in response:
            file_names = [obj['Key'].split('/')[-1] for obj in response['Contents']]
            return {"file_present": True, "file_names": file_names}
        else:
            return {"file_present": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





######################## Test API #############################################################
@app.get('/')
async def get():
    return True
######### API related to users #################################################################

class SubmitModel(BaseModel):
    email: str
    status: str='pending'
    submit_button: bool = False 

@app.post('/user/submit')
async def verify(submit:SubmitModel):
    personal = client.bgv.personal.count_documents({'email' : submit.email})
    sslc = client.bgv.sslc.count_documents({'email':submit.email})
    hse = client.bgv.hse.count_documents({'email':submit.email})
    ug = client.bgv.ug.count_documents({'email' : submit.email})
   
    if personal == 0 or sslc == 0 or hse == 0 or ug == 0:
        return False
    else:
        try:
            filter = {
                'email': submit.email,
            }
            update ={
                '$set':{'status': submit.status, 'submit_button': submit.submit_button}
            }
            client.bgv.user.update_one(filter=filter,update=update)
            return True
        except Exception as e:
            print(str(e))



class UserModel(BaseModel):
    name : str
    email : str
    password : str
    submit_button: bool = True 

### create a new user and also create a folder with email as filename
@app.post('/user')
async def add_user(user: UserModel):
    filter = {
        'email': user.email,
    }
    if client.bgv.user.count_documents(filter) == 0:
        try:
            os.mkdir(user.email)
        except FileExistsError as e:
            print (str(e))
        try:
            client.bgv.user.insert_one(dict(user))
            return True
        except Exception as e:
            print('Error inserting user: %s' % e)
    else : 
        return False

#### getting user information from database

@app.get('/company/verified_user')
async def verified_user(email: str):
    filter = {
        'email': email,
        'status': 'verified'
    }
    project = {
        '_id': 0,
    }
    if client.bgv.user.count_documents(filter) == 1:
        return {'list': dict(client.bgv.user.find_one(filter,project)), 'result': True}
    else : 
        return False

@app.get('/user')
async def get_user(email : str):
    filter = {
        'email': email
    }
    project = {
        '_id': 0,
    }
    if client.bgv.user.count_documents(filter) == 1:
        return dict(client.bgv.user.find_one(filter,project))
    else : 
        return False

@app.get('/totalprofile')
async def total_user():
    try:
        counts = client.bgv.user.count_documents({'status': "verified"})
        count1 = client.bgv.user.count_documents({'status':"pending"})
        count2 = client.bgv.user.count_documents({'status':"InProgress"})
        return {'counts': counts + count1 + count2}
    except Exception as e:
        print(str(e))
        return False


@app.get('/usereducation')
async def get_usercertificates(email:str):
    filter = {
        'email': email
        }
    project={
        '_id': 0,
    }
    data ={
        'sslc' : dict(client.bgv.sslc.find_one(filter,project)),
        'hse' : dict(client.bgv.hse.find_one(filter,project)),
        'ug': dict(client.bgv.ug.find_one(filter,project)),
    }
    return data

@app.get('userexp')
async def user_exp(email: str):
    filter ={
        'email': email
    }
    project = {
        '_id': 0,
        }
    if client.bgv.exp.count_documents(filter) == 0:
        return False
    else :
        return list(client.bgv.exp.find(filter,project))

#### generating otp for email verification


####  comparing OTP with existing user account


@app.post('/emailverified')
async def checkotp(email : str ):

    filter = { 'email' : email}
    update = {
        '$set': {'emailverified' : True}
    }
    try:
        client.bgv.user.find_one_and_update(filter,update)
        return True
    except Exception as e:
        print ("Error in updating email verification status"+str(e))
        return False

## the personal data input api for the user     

class PersonalData(BaseModel):

    empid : str
    doj : str
    email : str
    company_name:str
    designation: str
    company_mail : str
    mob : str
    aadhaar: str
    pan : str
    passport : str
    personal : bool = True
    status : bool = False
    submitted_on : str =  datetime.now()
    edited_on : str =  datetime.now()
    


@app.get('/personal')
async def get_personal(email : str):
    filter = {
        'email': email
    }
    project = {
        '_id': 0,
    }
    if client.bgv.personal.count_documents(filter) == 1:
        return dict(client.bgv.personal.find_one(filter,project))
    else : 
        return False

@app.post('/personal')
async def add_personal( data : PersonalData ):
    filt = {
        'email' : data.email,
        'empid': data.empid,
        'doj': data.doj,
        'company_name':data.company_name,
        'designation' : data.designation,
        'company_mail': data.company_mail,
        'mob': data.mob,
        'aadhaar': data.aadhaar,
        'pan': data.pan,
        'passport': data.passport,
        'personal': data.personal,
        'status': data.status,
        'submitted_on': data.submitted_on
    }
    update={
        '$set':{
        'empid': data.empid,
        'doj': data.doj,
        'company_name':data.company_name,
        'designation' : data.designation,
        'company_mail': data.company_mail,
        'mob': data.mob,
        'aadhaar': data.aadhaar,
        'pan': data.pan,
        'passport': data.passport,
        'personal': data.personal,
        'status': data.status,
        'submitted_on': data.submitted_on

        }
    }

    try: 
        client.bgv.personal.insert_one(filt, update)
        return True
    except Exception as e:
        print (str(e))
        return False
class PersonalAddress(BaseModel):
    email:str
    houseNo:str
    street:str
    region:str
    state:str
    country:str
    zipcode:str
    address:bool=True

@app.post('/personal/address')
async def update_address(data : PersonalAddress):
    filt ={
        'email':data.email
    }
    update={
        '$set':{
        'houseNo':data.houseNo,
        'street':data.street,
        'region' : data.region,
        'state':data.state,
        'country':data.country,
        'zipcode':data.zipcode,
        'address':data.address,
        }
    }
    try:
        client.bgv.personal.find_one_and_update(filt,update)
        return True
    except Exception as e:
        print(str(e))
        return False

@app.post('/personal/update')
async def update( data : PersonalData ):
    filt = {
        'email' : data.email
    }
    update={
        '$set':{
        'empid': data.empid,
        'doj': data.doj,
        'company_name':data.company_name,
        'designation' : data.designation,
        'company_mail': data.company_mail,
        'mob': data.mob,
        'aadhaar': data.aadhaar,
        'pan': data.pan,
        'passport': data.passport,
        'personal': data.personal,
        'status': data.status,
        'edited_on': data.edited_on,
        }
    }

    try: 
        client.bgv.personal.find_one_and_update(filt, update)
        return True
    except Exception as e:
        print (str(e))
        return False



## sslc certificate input

class SSLC(BaseModel):
    sslc_regno : str
    email : str
    sslc_marks : int
    sslc_school : str
    sslc_passout : int
    name : str
    sslc_board : str
    status : bool = False
    submitted_on: str= datetime.now()
    edited_on: str=datetime.now()
@app.post('/sslcupdate')
async def update( sslc : SSLC ):
    filt = {
        'email' : sslc.email
    }
    update={
        '$set':{
        'sslc_regno': sslc.sslc_regno,
        'sslc_marks':sslc.sslc_marks,
        'sslc_school' : sslc.sslc_school,
        'sslc_passout': sslc.sslc_passout,
        'sslc_board': sslc.sslc_board,
        'status': sslc.status,
        'edited_on': sslc.edited_on
        }
    }

    try: 
        client.bgv.sslc.find_one_and_update(filt, update)
        return True
    except Exception as e:
        print (str(e))
        return False
    
@app.post('/sslc')
async def sslcinput(sslc : SSLC):
    filt = {
        'email' : sslc.email,
        'sslc_regno': sslc.sslc_regno,
        'sslc_marks':sslc.sslc_marks,
        'sslc_school' : sslc.sslc_school,
        'sslc_passout': sslc.sslc_passout,
        'sslc_board': sslc.sslc_board,
        'status': sslc.status,
        'submitted_on': sslc.submitted_on
    }
    update={
        '$set':{
        'sslc_regno': sslc.sslc_regno,
        'sslc_marks':sslc.sslc_marks,
        'sslc_school' : sslc.sslc_school,
        'sslc_passout': sslc.sslc_passout,
        'sslc_board': sslc.sslc_board,
        'status': sslc.status,
        'submitted_on': sslc.submitted_on

        }
    }

    try: 
        client.bgv.sslc.insert_one(filt, update)
        return True
    except Exception as e:
        print (str(e))
        return False

@app.get('/sslc')
async def get_sslc(email : str):
    filter = {
        'email': email
    }
    project = {
        '_id': 0,
    }
    if client.bgv.sslc.count_documents(filter) == 1:
        return dict(client.bgv.sslc.find_one(filter,project))
    else : 
        return False



@app.get('/checkpdf')
async def checkpdf(email: str, regno: Optional[str] = None):
    filter = {
        'email': email
    }
    if(os.path.isfile(f"./{email}/{regno}.pdf")):
        return 'True'
    else:
        return 'False'


### code to upload pdf file 
@app.post('/uploadsslcpdf')
def upload(email : str = Form(), sslc_regno : str = Form(),file: UploadFile = File(...)):
    if(not os.path.isdir(email)):
         os.mkdir(email)
    path = os.path.join(email,sslc_regno+".pdf")
    try:
        contents = file.file.read()
        with open(path, 'wb') as f:
            f.write(contents)
    except Exception:
        return False
    finally:
        file.file.close()
    return True




@app.get('/getpdf')
async def getpdf(email: str, regno: str):
    path = os.path.join(email,regno+".pdf")
    if os.path.exists(path):
        try:
            return FileResponse(path, media_type="application/pdf", filename=regno+".pdf")
        except Exception as e:
            print(str(e))
    else:
        return False



## hser certificate input

class HSE (BaseModel):
    hse_regno: str
    email : str
    hse_marks : int
    hse_passout : int
    hse_school : str
    hse_board : str
    status : bool = False
    submitted_on: str= datetime.now()
    edited_on: str=datetime.now()

@app.post('/hseupdate')
async def update( hse : HSE ):
    filt = {
        'email' : hse.email
    }
    update={
        '$set':{
        'hse_regno': hse.hse_regno,
        'hse_marks':hse.hse_marks,
        'hse_school' : hse.hse_school,
        'hse_passout': hse.hse_passout,
        'hse_board': hse.hse_board,
        'status': hse.status,
        'edited_on': hse.edited_on
        }
    }

    try: 
        client.bgv.hse.find_one_and_update(filt, update)
        return True
    except Exception as e:
        print (str(e))
        return False

@app.post('/hse')
async def hseinput(hse : HSE):
    filt = {
        'email' : hse.email,
        'hse_regno': hse.hse_regno,
        'hse_marks':hse.hse_marks,
        'hse_school' : hse.hse_school,
        'hse_passout': hse.hse_passout,
        'hse_board': hse.hse_board,
        'status': hse.status,
        'submitted_on': hse.submitted_on
    }
    update={
        '$set':{
        'hse_regno': hse.hse_regno,
        'hse_marks':hse.hse_marks,
        'hse_school' : hse.hse_school,
        'hse_passout': hse.hse_passout,
        'hse_board': hse.hse_board,
        'status': hse.status,
        'submitted_on': hse.submitted_on
        }
    }
    try: 
        client.bgv.hse.insert_one(filt, update)
        return True
    except Exception as e:
        print (str(e))
        return False
@app.get('/hse')
async def get_hse(email:str):
    filter = {
        'email': email,
    }
    project={
        '_id':0
    }
    try:
        return dict(client.bgv.hse.find_one(filter,project))
    except Exception as e:
        print (str(e))
        return False

@app.post('/uploadhsepdf')
def upload(email : str = Form(), hse_regno : str = Form(),file: UploadFile = File(...)):
    if(not os.path.isdir(email)):
         os.mkdir(email)
    path = os.path.join(email,hse_regno+".pdf")
    try:
        contents = file.file.read()
        with open(path, 'wb') as f:
            f.write(contents)
    except Exception:
        return False
    finally:
        file.file.close()
    return True

# --------------- API for uploading UG data --------------------------------

class UG(BaseModel):
    ug_regno : str
    email : str
    name : str
    ug_specialization : str
    ug_college : str
    ug_marks : int
    ug_passout : int
    ug_university : str
    status : bool = False
    submitted_on: str= datetime.now()
    edited_on: str=datetime.now()

@app.post('/ugupdate')
async def update( ug : UG ):
    filt = {
        'email' : ug.email
    }
    update={
        '$set':{
        'ug_regno': ug.ug_regno,
        'ug_marks':ug.ug_marks,
        'ug_specialization' : ug.ug_specialization,
        'ug_college': ug.ug_college,
        'ug_passout': ug.ug_passout,
        'university': ug.ug_university,
        'status': ug.status,
        'edited_on': ug.edited_on
        }
    }

    try: 
        client.bgv.ug.find_one_and_update(filt, update)
        return True
    except Exception as e:
        print (str(e))
        return False

@app.post('/ug')
async def addug(ug: UG):
    filt = {
        'email' : ug.email,
        'ug_regno': ug.ug_regno,
        'ug_marks':ug.ug_marks,
        'ug_specialization' : ug.ug_specialization,
        'ug_college': ug.ug_college,
        'ug_passout': ug.ug_passout,
        'ug_university': ug.ug_university,
        'status': ug.status,
        'submitted_on': ug.submitted_on
    }
    update={
        '$set':{
        'ug_regno': ug.ug_regno,
        'ug_marks':ug.ug_marks,
        'ug_specialization' : ug.ug_specialization,
        'ug_college': ug.ug_college,
        'ug_passout': ug.ug_passout,
        'ug_university': ug.ug_university,
        'status': ug.status,
        'submitted_on': ug.submitted_on
        }
    }
    try: 
        client.bgv.ug.insert_one(filt, update)
        return True
    except Exception as e:
        print (str(e))
        return False


@app.get('/ug')
async def get_ug(email:str):
    filter = {'email': email}
    project = {
        '_id':0
    }
    try:
        return dict(client.bgv.ug.find_one(filter,project))
    except Exception as e:
        print(str(e))
        return False

@app.post('/uploadugpdf')
def upload(email : str = Form(), ug_regno : str = Form(),file: UploadFile = File(...)):
    if(not os.path.isdir(email)):
         os.mkdir(email)
    path = os.path.join(email,ug_regno+".pdf")
    try:
        contents = file.file.read()
        with open(path, 'wb') as f:
            f.write(contents)
    except Exception:
        return False
    finally:
        file.file.close()
    return True
######### PG DETAILS ##################
class updation(BaseModel):
    email: str 
    status: bool = False
    submit_button: bool = True 


@app.post('/user/pgupdation')
async def add_pgupdation(pg: updation):
    filter={
        'email': pg.email,
    }
    update={
        '$set':{
            'status': pg.status, 'submit_button': pg.submit_button
        }
    }
    try:
        client.bgv.user.find_one_and_update(filter, update)
        return True
    except Exception as e:
        print(str(e))
        return False

@app.post('/user/expupdation')
async def add_expupdation(exp: updation):
    filter={
        'email': exp.email,
    }
    update={
        '$set':{
            'status': exp.status, 'submit_button': exp.submit_button
        }
    }
    try:
        client.bgv.user.find_one_and_update(filter, update)
        return True
    except Exception as e:
        print(str(e))
        return False

class PG(BaseModel):
    pg_regno : str
    email : str
    name : str
    pg_specialization : str
    pg_college : str
    pg_marks : int
    pg_passout : int
    pg_university : str
    status : bool = False
    submitted_on: str= datetime.now()
    edited_on: str=datetime.now()

@app.post('/pgupdate')
async def update( pg : PG ):
    filt = {
        'email' : pg.email
    }
    update={
        '$set':{
        'pg_regno': pg.pg_regno,
        'pg_marks':pg.pg_marks,
        'pg_specialization' : pg.pg_specialization,
        'pg_college': pg.pg_college,
        'pg_passout': pg.pg_passout,
        'pg_university': pg.pg_university,
        'status': pg.status,
        'edited_on': pg.edited_on
        }
    }

    try: 
        client.bgv.pg.find_one_and_update(filt, update)
        return True
    except Exception as e:
        print (str(e))
        return False

@app.post('/pg')
async def addpg(pg: PG):
    filt = {
        'email' : pg.email,
        'pg_regno': pg.pg_regno,
        'pg_marks':pg.pg_marks,
        'pg_specialization' : pg.pg_specialization,
        'pg_college': pg.pg_college,
        'pg_passout': pg.pg_passout,
        'pg_university': pg.pg_university,
        'status': pg.status,
        'submitted_on': pg.submitted_on
    }
    update={
        '$set':{
        'pg_regno': pg.pg_regno,
        'pg_marks':pg.pg_marks,
        'pg_specialization' : pg.pg_specialization,
        'pg_college': pg.pg_college,
        'pg_passout': pg.pg_passout,
        'pg_university': pg.pg_university,
        'status': pg.status,
        'submitted_on': pg.submitted_on
        }
    }
    try: 
        client.bgv.pg.insert_one(filt, update)
        return True
    except Exception as e:
        print (str(e))
        return False


@app.get('/pg')
async def get_pg(email:str):
    filter = {'email': email}
    project = {
        '_id':0
    }
    try:
        return dict(client.bgv.pg.find_one(filter,project))
    except Exception as e:
        print(str(e))
        return False

@app.post('/uploadpgpdf')
def upload(email : str = Form(), pg_regno : str = Form(),file: UploadFile = File(...)):
    if(not os.path.isdir(email)):
         os.mkdir(email)
    path = os.path.join(email,pg_regno+".pdf")
    try:
        contents = file.file.read()
        with open(path, 'wb') as f:
            f.write(contents)
    except Exception:
        return False
    finally:
        file.file.close()
    return True
######### Experience models and API ################################

class Experience(BaseModel):
    empid : str
    name : str
    email : str
    company_name : str
    hr_mail : str
    start_date : str
    end_date : str
    designation : str
    lpa : str
    reporting_manager : str
    status : bool = False
    submitted_on: str= datetime.now()
    edited_on: str=datetime.now()

#### API to add experience  #########################
@app.post('/expupdate')
async def update( exp : Experience ):
    filt = {
        'email' : exp.email
    }
    update={
        '$set':{
        'empid': exp.empid,
        'company_name':exp.company_name,
        'hr_mail': exp.hr_mail,
        'start_date': exp.start_date,
        'end_date': exp.end_date,
        'designation': exp.designation,
        'lpa': exp.lpa,
        'reporting_manager': exp.reporting_manager,
        'status': exp.status,
        'edited_on': exp.edited_on
        }
    }

    try: 
        client.bgv.exp.find_one_and_update(filt, update)
        return True
    except Exception as e:
        print (str(e))
        return False
    
@app.post('/exp')
async def add_exp(exp :Experience):
    filt = {
        'email' : exp.email,
        'empid': exp.empid,
        'company_name':exp.company_name,
        'hr_mail': exp.hr_mail,
        'start_date': exp.start_date,
        'end_date': exp.end_date,
        'designation': exp.designation,
        'lpa': exp.lpa,
        'reporting_manager': exp.reporting_manager,
        'status': exp.status,
        'submitted_on': exp.submitted_on
    }
    update={
        '$set':{
        'empid': exp.empid,
        'company_name':exp.company_name,
        'hr_mail': exp.hr_mail,
        'start_date': exp.start_date,
        'end_date': exp.end_date,
        'designation': exp.designation,
        'lpa': exp.lpa,
        'reporting_manager': exp.reporting_manager,
        'status': exp.status,
        'submitted_on': exp.submitted_on
        }
    }
    try: 
        client.bgv.exp.insert_one(filt, update)
        return True
    except Exception as e:
        print (str(e))
        return False

@app.get('/exp')
async def get_experience(email: str):
    filter ={
        'email' : email,
    }
    project ={
        '_id':0,
        }
    
    try:
        
        return list(client.bgv.exp.find(filter,project))
        
    except Exception as e:
        print(str(e))
        return False

"""@app.get('/exp')
async def get_exp(email:str):
    filter = {'email': email}
    project = {
        '_id':0
    }
    try:
        return dict(client.bgv.exp.find_one(filter,project))
    except Exception as e:
        print(str(e))
        return False"""



@app.post('/uploadexppdf')
def upload(email : str = Form(), empid : str = Form(),file: UploadFile = File(...)):
    if(not os.path.isdir(email)):
         os.mkdir(email)
    path = os.path.join(email,empid+".pdf")
    try:
        contents = file.file.read()
        with open(path, 'wb') as f:
            f.write(contents)
    except Exception:
        return False
    finally:
        file.file.close()
    return True

 
class Expupdate(BaseModel):
    empid : str
    reason : str
    rehire : str
    dues: str
    relieved: str
    remarks: str
@app.post('/expdataadd')
async def dataadd(data : Expupdate):
    filter = {
        'empid' : data.empid
    }
    update = {
        '$set': {
            'reason': data.reason,
            'dues': data.dues,
            'relieved': data.relieved,
            'remarks': data.remarks,
            'rehire': data.rehire
        }
    }
    try:
        client.bgv.exp.find_one_and_update(filter, update)
        return True
    except Exception as e:
        print(str(e))
        return False
    
        
################################################################################################

############### API related to HR ##############################################################

class HrModel(BaseModel):
    name : str
    company_reg:str
    company_mail : str
    password : str
    mob:str
    gst:str
    status:str='pending'
    
@app.post('/hr')
async def add_hr(hr:HrModel):
    filter = {
        'company_email': hr.company_mail
    }
    if client.bgv.hr.count_documents(filter) == 0:
        try:
            client.bgv.hr.insert_one(dict(hr))
            return True
        except Exception as e:
            print('Error inserting hr'+ str(e))
            return False
    else: 
        return False
@app.get('/hr')
async def get_hr(company_mail: str):
    try :
        filter = {
            'company_mail':company_mail
            }
        project ={
            '_id':0,
        }
        return dict(client.bgv.hr.find_one(filter,project))
    except Exception as e:
        print('Error getting hr'+ str(e))
        return False
class Hrprofile(BaseModel):
    company_mail : str
@app.post('/hrprofile')
async def gethr(hr:Hrprofile):
    try:
        filter = dict(hr)
        project={
            '_id':0,
            'name': 1,
            'company_mail': 1
        }
        return dict(client.bgv.hr.find_one(filter,project))
    except Exception as e:
        print('Error getting hr'+ str(e))
        return False
    
@app.post('/uploadgstn')
async def uploadgstn(company_mail : str = Form(), file: UploadFile = File(...)):
      if(not os.path.isdir(company_mail)):
         os.mkdir(company_mail)
      path = os.path.join(company_mail, file.filename)
      try:
         contents = file.file.read()
         with open(path, 'wb') as f:
          f.write(contents)
      except Exception:
       return False
      finally:
         file.file.close()

      return True
################################################################################################

############### API related to Notary ##########################################################

@app.get('/notary')
async def get_notary(email: str):
    try :
        filter = {
            'email':email
            }
        project ={
            '_id':0,
        }
        return dict(client.bgv.notary.find_one(filter,project))
    except Exception as e:
        print('Error getting notary'+ str(e))
        return False

class NotaryModel(BaseModel):
    name : str
    email : str
    aadhaar :str
    password : str
    mob:str
    pan:str
    status:str='pending'

@app.post('/notary')
async def add_notary(notary:NotaryModel):
    filter = {
        'email': notary.email,
    }
    if client.bgv.notary.count_documents(filter) == 0:
        try:
            client.bgv.notary.insert_one(dict(notary))
            return True
        except Exception as e:
            print ('Error inserting notary'+ str(e))
    else :
        return False

class NLogin(BaseModel):
    email : str
    password : Optional[str] = None
    login_date: str = datetime.now()
    last_login: str = datetime.now()
    notary_last_visited: str = datetime.now()

@app.post('/notary/user_lastvisited')
async def user_lastvisited(data: NLogin):
    filter={
        'email': data.email
    }
    update={
        '$set':{
            'notary_last_visited': data.notary_last_visited
        }
    }
    try:
        client.bgv.user.update_one(filter, update)
        return True
    except Exception as e:
        print(str(e))
        return False

@app.get("/notary/login")
async def login(email : str, password : str):
    filter = {
        'email': email,
        'password': password
    }
    notary = client.bgv.notary.find_one(filter)
    if notary:
        access_token = create_access_token(data = {"sub":email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        response = JSONResponse(content={"access_token": access_token, "token_type": "bearer", "success": True})
        if COOKIE_DOMAIN:
            response.set_cookie(key="Authorization", value=f"Bearer {access_token}", domain=COOKIE_DOMAIN,
                                httponly=True, secure=True)
        else:
            response.set_cookie(key="Authorization", value=f"Bearer {access_token}", httponly=True, secure=True)
        return response
    else:
        return False
    
@app.post('/notarylogin')
async def notary_login(login:NLogin):
    try:
        if(client.bgv.notary.count_documents(dict(login))) ==1:
            return True
        else:
            return False
    except Exception as e:
        print(str(e))
        return False

@app.post('/notary/logindate')
async def notary_logindate(login:NLogin):
    filter={
        'email': login.email
    }
    update={
        '$set':{
            'login_date':login.login_date,
        }
    }
    try:
        client.bgv.notary.update_one(filter, update)
        return True
    except Exception as e:
        print(str(e))
        return False

@app.post('/notary/last_login')
async def notary_lastlogin(login:NLogin):
    filter={
        'email': login.email
    }
    update={
        '$set':{
                  'last_login': login.last_login
        }
  
    }
    try:
        client.bgv.notary.update_one(filter, update)
        return True
    except Exception as e:
        print(str(e))
        return False



#################################################################################################
# JWT Token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get the current user from the JWT token in the request header
async def get_current_user(request: Request, token: str = Cookie(None)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")


# You can create other routes for your frontend interactions with Vuetify
##################################### Login API #################################################


@app.get("/login")
async def login(email : str, password : str):
    filter = {
        'email': email,
        'password': password
    }
    user = client.bgv.user.find_one(filter)

    if user:
        access_token = create_access_token(data = {"sub":email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        response = JSONResponse(content={"access_token": access_token, "token_type": "bearer", "success": True})
        if COOKIE_DOMAIN:
            response.set_cookie(key="Authorization", value=f"Bearer {access_token}", domain=COOKIE_DOMAIN,
                                httponly=True, secure=True)
        else:
            response.set_cookie(key="Authorization", value=f"Bearer {access_token}", httponly=True, secure=True)
        return response
    else:
        return False

class HRLogin(BaseModel):
    company_mail :str
    password : Optional[str] = None
    login_date: str = datetime.now()
    last_login: str = datetime.now()

@app.post('/hr/login_date')
async def hr_logindate(login:HRLogin):
    filter={
        'company_mail': login.company_mail
    }
    update={
        '$set':{
            'login_date':login.login_date,
        }
    }
    try:
        client.bgv.hr.update_one(filter, update)
        return True
    except Exception as e:
        print(str(e))
        return False

@app.post('/hr/last_login')
async def hr_lastlogin(login:HRLogin):
    filter={
        'company_mail': login.company_mail
        }
    update={
        '$set':{
            'last_login':login.last_login,
        }
    }
    try:
        client.bgv.hr.update_one(filter, update)
        return True
    except Exception as e:
        print(str(e))
        return False

@app.get("/hr/login")
async def hr_login(company_mail : str, password : str):
    filter = {
        'company_mail': company_mail,
        'password': password
    }
    hr = client.bgv.hr.find_one(filter)

    if hr:
        access_token = create_access_token(data = {"sub":company_mail}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        response = JSONResponse(content={"access_token": access_token, "token_type": "bearer", "success": True})
        if COOKIE_DOMAIN:
            response.set_cookie(key="Authorization", value=f"Bearer {access_token}", domain=COOKIE_DOMAIN,
                                httponly=True, secure=True)
        else:
            response.set_cookie(key="Authorization", value=f"Bearer {access_token}", httponly=True, secure=True)
        return response
    else:
        return False

@app.get('/pendinguser')
async def pendinguser():
    filter ={
        'status' : 'pending',
    }
    project ={
        '_id':0,
        }
    
    try:
        count = client.bgv.user.count_documents(filter)
        return {"count":count, "list": list(client.bgv.user.find(filter,project))}
        
    except Exception as e:
        print(str(e))
        return False

@app.get('/verifiedusers')
async def apprpvedusers():
    try:
        filter ={
            'status' : 'verified'
            }
        project ={
            '_id':0
            }
        count1 = client.bgv.user.count_documents(filter)
        return {"count1": count1, "list":list(client.bgv.user.find(filter,project))}
    except Exception as e:
        print(str(e))
        return False





class Verify(BaseModel):
    user_email : str
    empid: Optional[str] = None 
    sslc_regno: Optional[str] = None
    hse_regno: Optional[str] = None
    ug_regno: Optional[str] = None
    pg_regno: Optional[str] = None
    notary_email: str
    notary_name :str
    status : str = "verified"
    approved_on: str= datetime.now()

@app.post('/verify/user')
async def verify(verify:Verify):
    personal = client.bgv.personal.count_documents({'email' : verify.user_email, 'status' : False})

    sslc = client.bgv.sslc.count_documents({'email':verify.user_email,'status':False})
    hse = client.bgv.hse.count_documents({'email':verify.user_email,'status':False})
    ug = client.bgv.ug.count_documents({'email' : verify.user_email, 'status' : False})
    pg = client.bgv.pg.count_documents({'email' : verify.user_email, 'status' : False})
    exp = client.bgv.exp.count_documents({'email' : verify.user_email, 'status' : False})


    if sslc+hse+ug+pg+exp+personal == 0:
        try:
        
            filter = {
                'email': verify.user_email,
            }
            update ={
                '$set':{ 'approved_on':verify.approved_on,'status': verify.status, 'notary_email': verify.notary_email, 'notary_name':verify.notary_name}
            }
            client.bgv.user.update_one(filter=filter,update=update)
            return True
        except Exception as e:
            print(str(e))
    else:
        return False

@app.post('/verify/personaldetails')
async def verify(verify : Verify):
    try:
        filter = {
            'email': verify.user_email,
        }
        update = {
            '$set' : {
                'approved_on':verify.approved_on,
                'status' : verify.status,
                'notary_email' : verify.notary_email,
                'notary_name' : verify.notary_name
            }
        }
        client.bgv.personal.find_one_and_update(filter=filter,update=update)
        return True
    except Exception as e:
        print(str(e))
        return False


@app.post('/verify/sslc')
async def verifysslc(verify : Verify):
    try:
        filter = {
            'email': verify.user_email,
            'sslc_regno': verify.sslc_regno
        }
        update = {
            '$set' : {
                'approved_on':verify.approved_on,
                'status' : verify.status,
                'notary_email' : verify.notary_email,
                'notary_name' : verify.notary_name
            }
        }
        client.bgv.sslc.find_one_and_update(filter=filter,update=update)
        return True
    except Exception as e:
        print(str(e))
        return False

@app.post('/verify/hse')
async def verifyhse(verify: Verify):
    try:
        filter = {
            'email' : verify.user_email,
            'hse_regno': verify.hse_regno
        }
        update = {
            '$set' : {
                'approved_on':verify.approved_on,
                'status' : verify.status,
                'notary_email' : verify.notary_email,
                'notary_name' : verify.notary_name
            }
        }
        client.bgv.hse.find_one_and_update(filter=filter,update=update)
        return True
    except Exception as e:
        print(str(e))
        return False

@app.post('/verify/ug')
async def verifyug(verify: Verify):
    try:
        filter = {
            'email' : verify.user_email,
            'ug_regno': verify.ug_regno
        }
        update = {
            '$set' : {
                'approved_on':verify.approved_on,
                'status' : verify.status,
                'notary_email' : verify.notary_email,
                'notary_name' : verify.notary_name
            }
        }
        client.bgv.ug.find_one_and_update(filter=filter,update=update)
        return True
    except Exception as e:
        print(str(e))
        return False

@app.post('/verify/pg')
async def verifypg(verify: Verify):
    try :
        filter = {
            'email' : verify.user_email,
            'pg_regno': verify.pg_regno
        }
        update = {
            '$set' : {
                'approved_on':verify.approved_on,
                'status' : verify.status,
                'notary_email' : verify.notary_email,
                'notary_name' : verify.notary_name
            }
        }
        client.bgv.pg.find_one_and_update(filter=filter,update=update)
        return True
    except Exception as e:
        print(str(e))
        return False

@app.post('/verify/exp')
async def verifyexp(verify: Verify):
    try:
        filter = {
            'email' : verify.user_email,
            'empid' : verify.empid
        }
        update = {
            '$set' : {
                'approved_on':verify.approved_on,
                'status' : verify.status,
                'notary_email' : verify.notary_email,
                'notary_name' : verify.notary_name
            }
        }
        client.bgv.exp.find_one_and_update(filter=filter,update=update)
        return True
    except Exception as e:
        print(str(e))
        return False
## API to create view request

class Request(BaseModel):
    user_email : str
    hr_email :str
    hr_name:str
    status: str = 'pending'
@app.post('/requestdata')
async def request(request:Request):
    try:
        client.bgv.request.insert_one(dict(request))
        return True
    except Exception as e:
        print(str(e))
        return False
## API to update request status
@app.get('/user/pendingrequest')
async def get_request(email:str):
    try:
        filter = {
            'user_email': email,
            'status' :'pending'
            }
        project ={
            '_id':0
        }
        return list(client.bgv.request.find(filter,project))
    except Exception as e:
        print(str(e))
        return False

@app.get('/user/approved')
async def get_approved(email:str):
    try:
        filter = {
            'user_email': email,
            'status':'approved'
        }
        project ={
            '_id':0
            }
        return list(client.bgv.request.find(filter,project))
    except Exception as e:
        print(str(e))
        return False



@app.get('/hr/pendingrequest')
async def pendingrequest(hr_email: str):
    try:
        pipeline = [
            {
                '$match': {
                    'hr_email': hr_email, 
                    'status': 'pending'
                }
            }, {
                '$lookup': {
                    'from': 'user', 
                    'localField': 'user_email', 
                    'foreignField': 'email', 
                    'as': 'user_name'
                }
            }, {
                '$addFields': {
                    'user_name': {
                        '$arrayElemAt': [
                            '$user_name', 0
                        ]
                    }
                }
            }, {
                '$addFields': {
                    'user_name': '$user_name.name', 
                    'user_designation': '$user_name.designation'
                }
            }, {
                '$project': {
                    '_id': 0
                }
            }
]
        return list(client.bgv.request.aggregate(pipeline))
    except Exception as e:
        print(str(e))
        return False

@app.get('/hr/approved')
async def approvedhr(email: str):
    try:
        filter ={
            'hr_email':email,
            'status':'approved'
            }
        project={
            '_id':0
        }
        return list(client.bgv.request.find(filter,project))
    except Exception as e:
        print(str(e))
        return False


class UpdateRequest(BaseModel):
    user_email : str
    hr_email : str
    status : str
@app.post('/request/update')
async def update_user(update : UpdateRequest ):
    try:
        filter = {
            'user_email': update.user_email,
            'hr_email' : update.hr_email,
            'status': 'pending'
            }
        update= {
            '$set' : {
                'status' : update.status
            }
        }
        client.bgv.request.update_one(filter, update)
        return True
    except Exception as e:
        print(str(e))
        return False




@app.post('/user/filter')
async def user_filter(query : Dict):
    try:
        filter = query
        project = {
            "_id":0
        }
        return list(client.bgv.user.find(filter,project))
    except Exception as e:
        print(str(e))
        return False



#############Super Admin ###########

class Admin(BaseModel):
      name: str
      admin_email: str
      password: str

@app.post("/admin")
async def add_admin(admin: Admin):
      try:
        client.bgv.admin.insert_one(dict(admin))
        return True
      except Exception as e:
        print(str(e))
      return False

@app.get('/admin')
async def get_user(admin_email:str):
    filter={
        'admin_email':admin_email
    }
    project ={
        '_id':0,
    }
    if client.bgv.admin.count_documents(filter)==1:
        return dict(client.bgv.admin.find_one(filter,project))
    else:
        return False

class Adminlogin(BaseModel):
      admin_email : str
      password : str
@app.post('/adminlogin')
async def admin_login(login:Adminlogin):
      try:
        if(client.bgv.admin.count_documents(dict(login)) ==1):
          return True
        else:
          return False
      except Exception as e:
        print(str(e))
        return False
      
      
@app.post('/hr/uploadcsv')
async def uploadcsv(company_mail: str= Form(),file: UploadFile = File(...) ):
   if(not os.path.isdir(company_mail)):
       os.mkdir(company_mail)
   path = os.path.join(company_mail,file.filename)
   try:
        contents = file.file.read()
        with open(path, 'wb') as f:
            f.write(contents)
   except Exception:
        return False
   finally:
        file.file.close()
   return True
    
############### CompanyRegistration ################################
@app.get('/company/pending')
async def company_pending():
    filter={
        'status':"pending"
    }
    project={
        '_id':0
    }
    try:
        Ccount=client.bgv.hr.count_documents(filter)
        return {'Ccount':Ccount,'list':list(client.bgv.hr.find(filter,project))}
    except Exception as e:
        print(str(e))
        return False
    
@app.get('/company/verified')
async def company_verified():
    filter={
        'status':"verified"
    }
    project={
        '_id':0
    }
    try:
        Gcount=client.bgv.hr.count_documents(filter)
        return {'Gcount':Gcount,'list':list(client.bgv.hr.find(filter,project))}
    except Exception as e:
        print(str(e))
        return False
#####################NotayRegistration################

@app.get('/notary/pending')
async def notary_pending():
    filter={
        'status':"pending"
    }
    project={
        '_id':0
    }
    try:
        Ecount=client.bgv.notary.count_documents(filter)
        return{'Ecount':Ecount,'list':list(client.bgv.notary.find(filter,project))}
    except Exception as e:
        print(str(e))
        return False
    
@app.get('/notary/verified')
async def notary_verified():
    filter={
        'status':"verified"
    }
    project={
        '_id':0
    }
    try:
        Fcount=client.bgv.notary.count_documents(filter)
        return{'Fcount':Fcount,'list':list(client.bgv.notary.find(filter,project))}
    
    except Exception as e:
        print(str(e))
        return False
    
class SuperAdminVerify(BaseModel):
    company_mail:Optional[str] = None
    email:Optional[str] = None
    admin_email:str
    name:str
    status:str="verified"

@app.post('/company/verification')
async def verify_company(data:SuperAdminVerify):
    filter={
        'company_mail':data.company_mail
    }
    update={
        '$set':{
            'admin_email':data.admin_email,
            'name':data.name,
            'status':data.status
        }
    }
    try:
        client.bgv.hr.find_one_and_update(filter,update)
        return True
    except Exception as e:
        print(str(e))
        return False
    
@app.post('/notary/verification')
async def verify_notary(data:SuperAdminVerify):
    filter={
        'email':data.email
    }
    update={
        '$set':{
            'admin_email':data.admin_email,
            'name':data.name,
            'status':data.status
        }
    }
    try:
        client.bgv.notary.find_one_and_update(filter,update)
        return True
    except Exception as e:
        print(str(e))
        return False
    

#####################InProgress###################
class InProgress(BaseModel):
    email:str
    status:str="InProgress"

@app.post('/personal/inprogress')
async def inprogress_personal(data:InProgress):
    filter={
        'email':data.email
    }
    update={
        '$set':{
            'status':data.status
      }
    }
    try:
        client.bgv.user.find_one_and_update(filter,update)
        return True
    except Exception as e:
        print(str(e))
        return False
    
@app.post('/sslc/inprogress')
async def inprogress_sslc(data:InProgress):
    filter={
        'email':data.email
    }
    update={
        '$set':{
            'status':data.status
      }
    }
    try:
        client.bgv.user.find_one_and_update(filter,update)
        return True
    except Exception as e:
        print(str(e))
        return False
    
@app.post('/hse/inprogress')
async def inprogress_hse(data:InProgress):
    filter={
        'email':data.email
    }
    update={
        '$set':{
            'status':data.status
      }
    }
    try:
        client.bgv.user.find_one_and_update(filter,update)
        return True
    except Exception as e:
        print(str(e))
        return False
    

@app.post('/ug/inprogress')
async def inprogress_ug(data:InProgress):
    filter={
        'email':data.email
    }
    update={
        '$set':{
            'status':data.status
      }
    }
    try:
        client.bgv.user.find_one_and_update(filter,update)
        return True
    except Exception as e:
        print(str(e))
        return False
    

@app.post('/pg/inprogress')
async def inprogress_pg(data:InProgress):
    filter={
        'email':data.email
    }
    update={
        '$set':{
            'status':data.status
      }
    }
    try:
        client.bgv.user.find_one_and_update(filter,update)
        return True
    except Exception as e:
        print(str(e))
        return False
    

   
@app.post('/exp/inprogress')
async def inprogress_exp(data:InProgress):
    filter={
        'email':data.email
    }
    update={
        '$set':{
            'status':data.status
      }
    }
    try:
        client.bgv.user.find_one_and_update(filter,update)
        return True
    except Exception as e:
        print(str(e))
        return False
    

class UserVerified(BaseModel):
    email: str
    status: str="verified"

@app.post('/inprogress_verified')
async def inprogress_verified(user: UserVerified):
    filter={
        'email': user.email, 
        'status': "verified"
    }
    user_filter={
        'email': user.email,
        'status': "InProgress"
    }
    
    project={
        '_id':0
    }
    update={
        '$set':{
            'status':user.status
        }
    }
    
    personal = client.bgv.personal.count_documents(filter)
    sslc = client.bgv.sslc.count_documents(filter)
    hse = client.bgv.hse.count_documents(filter)
    ug = client.bgv.ug.count_documents(filter)

    count_filter={
        'email': user.email
    }
    if client.bgv.pg.count_documents(count_filter) >0 and client.bgv.exp.count_documents(count_filter) >0:
        pg = client.bgv.pg.count_documents(filter)
        exp = client.bgv.exp.count_documents(filter)
        exp_count = client.bgv.exp.count_documents(count_filter)
        if personal > 0 and sslc > 0 and hse > 0 and ug > 0 and pg > 0 and exp == exp_count:
            try:
                client.bgv.user.find_one_and_update(user_filter, update)
                return True
            except Exception as e:
                print(str(e))
                return False

    elif client.bgv.pg.count_documents(count_filter) == 0 and client.bgv.exp.count_documents(count_filter) >0: 
        exp = client.bgv.exp.count_documents(filter)
        exp_count = client.bgv.exp.count_documents(count_filter)

        if personal > 0 and sslc > 0 and hse > 0 and ug > 0 and exp == exp_count:
            try:
                client.bgv.user.find_one_and_update(user_filter, update)
                return True
            except Exception as e:
                print(str(e))
                return False
    elif client.bgv.pg.count_documents(count_filter) > 0 and client.bgv.exp.count_documents(count_filter) == 0:
        pg = client.bgv.pg.count_documents(filter)
        if personal > 0 and sslc > 0 and hse > 0 and ug > 0 and pg > 0:
            try:
                client.bgv.user.find_one_and_update(user_filter, update)
                return True
            except Exception as e:
                print(str(e))
                return False
    elif client.bgv.pg.count_documents(count_filter) == 0  and client.bgv.exp.count_documents(count_filter) == 0:
        if personal > 0 and sslc > 0 and hse > 0 and ug > 0:
            try:
                client.bgv.user.find_one_and_update(user_filter, update)
                return True
            except Exception as e:
                print(str(e))
                return False
    else:
        return False


@app.get('/inprogressuser')
async def inprogressuser():
    filter ={
        'status' : 'InProgress',
    }
    project ={
        '_id':0,
        }
    
    try:
        count = client.bgv.user.count_documents(filter)
        return {"count":count, "list": list(client.bgv.user.find(filter,project))}
        
    except Exception as e:
        print(str(e))
        return False
    
#################################################### Upload CSV File ####################################################################################
@app.post("/hr/uploadpersonal")
async def upload_csv(csv_file: UploadFile = None):
    if csv_file is None:
        return {"message": "No file uploaded"}
    contents = await csv_file.read()
    csv_string = contents.decode("utf-8")
    df = pd.read_csv(StringIO(csv_string))
    df['aadhaar'] = df['aadhaar'].astype(str)
    df['passport'] = df['passport'].astype(str)
    df['mob'] = df['mob'].astype(str)
    insert=df[~df.isnull().any(1)]

    insert['status'] = False
    insert['submitted_on'] = datetime.now()

    user = insert[['email','name']].copy()
    user['submit_button'] = False
    user['status'] = "pending"
    user["password"]="sajith@123"
    try:
        client.bgv.user.insert_many(user.to_dict('records'))
        client.bgv.personal.insert_many(insert.to_dict('records'))

    except Exception as e:
        print(str(e))
    
    delete=df[df.isnull().any(1)]
    delete.fillna(0,inplace=True)
    returndata  = {
        'total_count':len(df.index),
        'insert_count': len(insert.index),
        'delete_count': len(delete.index),
        'insert_list': insert.to_dict('records'),
        'delete_list': delete.to_dict('records'),
    }
    return returndata  
################################################################################################
@app.post("/hr/uploadsslc")
async def upload_csv(csv_file: UploadFile = None):
    if csv_file is None:
        return {"message": "No file uploaded"}
    contents = await csv_file.read()
    csv_string = contents.decode("utf-8")
    df = pd.read_csv(StringIO(csv_string))
    df['sslc_regno'] = df['sslc_regno'].astype(str)
    df['sslc_passout'] = df['sslc_passout'].astype(str)
    df['sslc_marks'] = df['sslc_marks'].astype(str)
    insert=df[~df.isnull().any(1)]
    insert['status'] = False
    insert['submitted_on'] = datetime.now()
    try:
        client.bgv.sslc.insert_many(insert.to_dict('records'))

    except Exception as e:
        print(str(e))
    
    delete=df[df.isnull().any(1)]
    delete.fillna(0,inplace=True)
    returndata  = {
        'total_count':len(df.index),
        'insert_count': len(insert.index),
        'delete_count': len(delete.index),
        'insert_list': insert.to_dict('records'),
        'delete_list': delete.to_dict('records'),
    }
    return returndata
#######################################################################################################
@app.post("/hr/uploadhse")
async def upload_csv(csv_file: UploadFile = None):
    if csv_file is None:
        return {"message": "No file uploaded"}
    contents = await csv_file.read()
    csv_string = contents.decode("utf-8")
    df = pd.read_csv(StringIO(csv_string))
    df['hse_passout'] = df['hse_passout'].astype(str)
    df['hse_marks'] = df['hse_marks'].astype(str)
    df['hse_regno'] = df['hse_regno'].astype(str)
    insert=df[~df.isnull().any(1)]
    insert['status'] = False
    insert['submitted_on'] = datetime.now()
    try:
        client.bgv.hse.insert_many(insert.to_dict('records'))

    except Exception as e:
        print(str(e))
    
    delete=df[df.isnull().any(1)]
    delete.fillna(0,inplace=True)   
    returndata  = {
        'total_count':len(df.index),
        'insert_count': len(insert.index),
        'delete_count': len(delete.index),
        'insert_list': insert.to_dict('records'),
        'delete_list': delete.to_dict('records'),
    }
    return returndata
######################################################################################################
@app.post("/hr/uploadug")
async def upload_csv(csv_file: UploadFile = None):
    if csv_file is None:
        return {"message": "No file uploaded"}
    contents = await csv_file.read()
    csv_string = contents.decode("utf-8")
    df = pd.read_csv(StringIO(csv_string))
    df['ug_regno'] = df['ug_regno'].astype(str)
    df['ug_passout'] = df['ug_passout'].astype(str)
    df['ug_marks'] = df['ug_marks'].astype(str)
    insert=df[~df.isnull().any(1)]
    insert['status'] = False
    insert['submitted_on'] = datetime.now()
    try:
        client.bgv.ug.insert_many(insert.to_dict('records'))

    except Exception as e:
        print(str(e))
    
    delete=df[df.isnull().any(1)]
    delete.fillna(0,inplace=True) 
    returndata  = {
        'total_count':len(df.index),
        'insert_count': len(insert.index),
        'delete_count': len(delete.index),
        'insert_list': insert.to_dict('records'),
        'delete_list': delete.to_dict('records'),
    }
    return returndata  

##########################################################################################################
@app.post("/hr/uploadpg")
async def upload_csv(csv_file: UploadFile = None):
    if csv_file is None:
        return {"message": "No file uploaded"}
    contents = await csv_file.read()
    csv_string = contents.decode("utf-8")
    df = pd.read_csv(StringIO(csv_string))
    df['pg_regno'] = df['pg_regno'].astype(str)
    df['pg_passout'] = df['pg_passout'].astype(str)
    df['pg_marks'] = df['pg_marks'].astype(str)
    insert=df[~df.isnull().any(1)]
    insert['status'] = False
    insert['submitted_on'] = datetime.now()
    try:
        client.bgv.pg.insert_many(insert.to_dict('records'))

    except Exception as e:
        print(str(e))
    
    delete=df[df.isnull().any(1)]
    delete.fillna(0,inplace=True)  
    returndata  = {
        'total_count':len(df.index),
        'insert_count': len(insert.index),
        'delete_count': len(delete.index),
        'insert_list': insert.to_dict('records'),
        'delete_list': delete.to_dict('records'),
    }
    return returndata  

#####################################################################################################
@app.post("/hr/uploadexp")
async def upload_csv(csv_file: UploadFile = None):
    if csv_file is None:
        return {"message": "No file uploaded"}
    contents = await csv_file.read()
    csv_string = contents.decode("utf-8")
    df = pd.read_csv(StringIO(csv_string))
    df['empid'] = df['empid'].astype(str)
    df['lpa'] = df['lpa'].astype(str)
    insert=df[~df.isnull().any(1)]
    insert['status'] = False
    insert['submitted_on'] = datetime.now()
    try:
        client.bgv.exp.insert_many(insert.to_dict('records'))

    except Exception as e:
        print(str(e))
    
    delete=df[df.isnull().any(1)]
    delete.fillna(0,inplace=True)    
    returndata  = {
        'total_count':len(df.index),
        'insert_count': len(insert.index),
        'delete_count': len(delete.index),
        'insert_list': insert.to_dict('records'),
        'delete_list': delete.to_dict('records'),
    }
    return returndata
#######################################################################################################
class SubscriptionType(BaseModel):
    name: str
    price: float

subscription_types = [
    SubscriptionType(name="Basic", price=9.99),
    SubscriptionType(name="Standard", price=19.99),
    SubscriptionType(name="Premium", price=29.99)
]

class UserSubscription(BaseModel):
    email: str
    subscription_type: str

subscriptions = []

@app.get("/subscription_types")
def get_subscription_types():
    return {"subscription_types": subscription_types}

@app.post("/subscribe")
def subscribe(user_subscription: UserSubscription):
    matching_subscription_type = next(
        (st for st in subscription_types if st.name == user_subscription.subscription_type),
        None
    )
    if matching_subscription_type:
        subscriptions.append(user_subscription)
        return {"message": "Subscription added successfully"}
    else:
        return {"message": "Invalid subscription type"}

@app.get("/subscriptions")
def get_subscriptions():
    return {"subscriptions": subscriptions}

@app.get("/subscriptions/{email}")
def get_subscription_by_email(email: str):
    matching_subscriptions = [subscription for subscription in subscriptions if subscription.email == email]
    if matching_subscriptions:
        return {"subscriptions": matching_subscriptions}
    else:
        return {"message": "No subscriptions found for the provided email"}
    

################################################################################################################
def convert_to_json_compliant(data):
    if isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, (int, float, str)):
        return str(data)
    elif isinstance(data, list):
        return [convert_to_json_compliant(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_to_json_compliant(value) for key, value in data.items()}
    return data


def generate_id():
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(characters) for _ in range(50))
    return random_string

def is_valid_email(email):
    # Define the email regex pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Check if the email matches the pattern
    if re.match(email_pattern, email):
        return True
    else:
        return False
    # return True

def is_valid_aadhaar(aadhaar_number):
    pattern = r'^\d{12}$'
    if re.match(pattern, f"{aadhaar_number}"):
        return True
    else:
        return False
    # return True


def is_valid_worldwide_mobile_number(number):
    # Pattern for a worldwide mobile number (simplified)
    pattern = r'^[0-9]{10}$'

    if re.match(pattern, f"{number}"):
        return True
    else:
        return False
    # return True

def is_valid_passport_number(passport_number):
    pattern = r'^[A-Z0-9]{6,15}$'

    if re.match(pattern, f"{passport_number}"):
        return True
    else:
        return False
    # return True


def is_valid_pan_number(pan_number):
    pattern = r'^([A-Z]){5}([0-9]){4}([A-Z]){1}?$'

    if re.match(pattern, pan_number):
        return True
    else:
        return False
    # return True
    
def is_valid_number(value):
    return isinstance(value, (float, int))    
    # return True

def is_valid_date(date_string):
    pattern = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$'

    if re.match(pattern, f"{date_string}"):
        return True
    else:
        return False
    # return True
    
current_timestamp = datetime.now()
formatted_timestamp = current_timestamp.strftime('%Y-%m-%d %H:%M:%S')

@app.post("/upload/")
async def upload_excel_file(file: UploadFile = File(...), bgv: str = "bgv"):
    try:
        with open(file.filename, "wb") as f:
            f.write(await file.read())

        db = client[bgv]

        xls = pd.ExcelFile(file.filename)
        sheet_names = xls.sheet_names

        collection_names = {
            "personal": "personal",
            "sslc": "sslc",
            "hse": "hse",
            "ug": "ug",
            "pg": "pg",
            "exp": "exp"
        }

        sheet_data = dict()
        to_mongo = dict()
        emails_in_excel = []

        rejected_data = list()
        total_count = 0

        for sheet_name in sheet_names:
            df = xls.parse(sheet_name)
            collection_name = collection_names.get(sheet_name, sheet_name.lower().replace(" ", "_"))

            # print(sheet_name)

            total_count_sheet, emails_in_excel_sheet, qualified_data_sheet, rejected_data_sheet = filter_excel(df, total_count, sheet_name)
            total_count = total_count_sheet
            emails_in_excel += emails_in_excel_sheet
            sheet_data[collection_name] = qualified_data_sheet
            rejected_data += rejected_data_sheet

            # print(len(rejected_data))

        os.remove(file.filename)
        new_user_list = list()
        new_user_emails = list()

        for db_collection in list(sheet_data):
            collection = db[db_collection]

            # print(sheet_data[db_collection])

            excel_data, new_user_list_in_sheet, rejected_data_sheet, new_user_emails_sheet = validate_users(
                sheet_data[db_collection], collection,db_collection, emails_in_excel, new_user_emails)

            # print(len(excel_data))

            to_mongo[db_collection] = excel_data
            new_user_list += new_user_list_in_sheet
            rejected_data += rejected_data_sheet
            new_user_emails = new_user_emails_sheet

            try:
                if len(to_mongo[db_collection]) > 0:
                    collection.insert_many(to_mongo[db_collection])
            except KeyError as e:
                print(f"No datas to insert in: {db_collection}")

        print(new_user_list)
        if len(new_user_list) > 0:
            db["user"].insert_many(new_user_list)

        if len(new_user_list) > 0:
            # send_user_mails(new_user_list)
            x = threading.Thread(target=send_user_mails, args=(new_user_list,))
            x.start()
        # if len(rejected_data) > 0:
        #     send_rejected_mails(rejected_data)

        return_data = {
            'total_count': total_count,
            'available_count': len(to_mongo["personal"]),
            'rejected_count': total_count - len(to_mongo["personal"]),
        }
        return return_data
    except HTTPException as http_exc:
        print(str(http_exc))
        raise http_exc

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=500)


def filter_excel(df_sheet, total_count, sheet_name):
    rejected_data = list()
    emails_in_excel = []

    if total_count < len(df_sheet.index):
        total_count = len(df_sheet.index)

    if df_sheet.isnull().values.any():
        # df_sheet = df_sheet.dropna()
        rejected_data.append(json.loads(df_sheet[df_sheet.isnull().any(axis=1)].to_json(orient='records')))
        df_sheet = df_sheet.dropna()

    if sheet_name == "personal":
        columns_to_convert = ["aadhaar", "passport", "mob"]
        df_sheet[columns_to_convert] = df_sheet[columns_to_convert].astype(int)

        # print("===>", df_sheet.to_json(orient='records'))

        for user_data in json.loads(df_sheet.to_json(orient='records')):
            # print("===>ss", user_data)
            if len(user_data) > 0:
                validity = apply_regex(user_data,sheet_name)

                # print(validity, sheet_name)

                if validity:
                    emails_in_excel.append(user_data["email"])

    if sheet_name == "sslc":
        columns_to_convert = ["sslc_passout", "sslc_regno"]
        df_sheet[columns_to_convert] = df_sheet[columns_to_convert].astype(int)
        
        for user_data in json.loads(df_sheet.to_json(orient='records')):
            # print("===>ss", user_data)
            if len(user_data) > 0:
                validity = apply_regex(user_data,sheet_name)

                # print(validity, sheet_name)

                if validity:
                    emails_in_excel.append(user_data["email"])

    if sheet_name == "hse":
        columns_to_convert = ["hse_regno", "hse_passout"]
        df_sheet[columns_to_convert] = df_sheet[columns_to_convert].astype(int)
        for user_data in json.loads(df_sheet.to_json(orient='records')):
            # print("===>ss", user_data)
            if len(user_data) > 0:
                validity = apply_regex(user_data,sheet_name)

                # print(validity, sheet_name)

                if validity:
                    emails_in_excel.append(user_data["email"])

    if sheet_name == "ug":
        columns_to_convert = ["ug_regno", "ug_passout"]
        df_sheet[columns_to_convert] = df_sheet[columns_to_convert].astype(int)
        
        for user_data in json.loads(df_sheet.to_json(orient='records')):
            # print("===>ss", user_data)
            if len(user_data) > 0:
                validity = apply_regex(user_data,sheet_name)

                # print(validity, sheet_name)

                if validity:
                    emails_in_excel.append(user_data["email"])

    if sheet_name == "pg":
        columns_to_convert = ["pg_regno", "pg_passout"]
        df_sheet[columns_to_convert] = df_sheet[columns_to_convert].astype(int)

    qualified_data = df_sheet.to_dict(orient="records")

    try:
        print(len(rejected_data[0]))
    except IndexError:
        rejected_data.append([])

    return total_count, emails_in_excel, qualified_data, rejected_data[0]


def validate_users(users_data, collection,db_collection, emails_exists, new_user_emails):
    excel_data = list()
    new_user_list = list()
    rejected_data = list()

    emails_in_db_list = list(collection.find({}, {"email": 1, "_id": 0}))
    email_in_db = list()

    for email_obj in emails_in_db_list:
        email_in_db.append(email_obj["email"])
    for user in users_data:
        # print(user)
        if user is not None:
            data_in_excel, new_user, rejected_data_sheet, new_user_emails_sheet = validate_user(user, emails_exists,
                                                                                                email_in_db, new_user_emails, 
                                                                                            db_collection)
    
            if len(data_in_excel) is not 0:
                # print("fijjiij", data_in_excel)
                excel_data.append(data_in_excel)
            if len(new_user) is not 0:
                new_user_list.append(new_user)
            rejected_data.append(rejected_data_sheet)
            new_user_emails = new_user_emails_sheet 

            # print("fijjiij", new_user_emails_sheet)

    # print(new_user_list)

    return excel_data, new_user_list, rejected_data, new_user_emails


def validate_user(user_data, emails_exists, email_in_db, new_user_emails,db_collection):
    user = dict()
    rejected_data = dict()
    excel_data = dict()

    email = user_data["email"]
    count = emails_exists.count(email)

    # print("jnjnj", count)

    if email_in_db.count(email) < 1:
        if count == 4 and is_valid_email(email):
            user_data["_id"] = generate_id()
            user_data["status"] = False
            user_data["submitted_on"] = formatted_timestamp

            excel_data = user_data

            if new_user_emails.count(email) < 1:
                new_user = {
                    "_id": generate_id(),
                    "name": user_data["name"],
                    "email": email,
                    "password": generate_id(),
                    "status": "pending",
                    "submitted_on": formatted_timestamp,
                }

                new_user_emails.append(email)
                user = new_user
        else:
            rejected_data = user_data
    else:
        rejected_data = user_data
    
    # print(f"validity {validity} {excel_data}")

    return excel_data, user, rejected_data, new_user_emails


def apply_regex(user: dict, collection: str) -> bool:
    is_valid = False

    print(user,collection)

    if collection == "personal":
        if is_valid_worldwide_mobile_number(user["mob"]) and is_valid_pan_number(user["pan"]) and is_valid_passport_number(user["passport"]) and is_valid_aadhaar(user["aadhaar"]) and is_valid_email(user["company_mail"]) and is_valid_date(user["doj"]):
            is_valid = True

    if collection == "sslc":
        if is_valid_number(user["sslc_marks"]) and is_valid_number(user["sslc_passout"]):
            is_valid = True

    if collection == "hse":
        if is_valid_number(user["hse_marks"]) and is_valid_number(user["hse_passout"]):
            is_valid = True

    if collection == "ug":
        if is_valid_number(user["ug_marks"]) and is_valid_number(user["ug_passout"]):
            is_valid = True

    if collection == "pg":
        if is_valid_number(user["pg_marks"]) and is_valid_number(user["pg_passout"]):
            is_valid = True

    if collection == "exp":
        if is_valid_number(user["lpa"]) and is_valid_date(user["start_date"]) and is_valid_date(user["end_date"]):
            is_valid = True

    return is_valid


config = configparser.ConfigParser()
config.read(['config.cfg', 'config.dev.cfg'])
azure_settings = config['azure']
graph: Graph = Graph(azure_settings)


def send_rejected_mails(rejected):
    for user in rejected:
        # print(user)

        subject = "Registration failed."
        reciptant = user["email"]

        message = f"Hi! This is to inform that your Profile creation was failed due to invalid or inconsistant data."

        # graph.send_mail(subject, message, reciptant)

        payload = {
            "reciptant": reciptant,
            "subject": subject,
            "body": message
        }

        requests.post("http://3.84.79.77:8000/mail/send", data=json.dumps(payload))


def send_user_mails(created):
    for user in created:
        print(user)
        subject = "Your New Account Details on Our Platform"
        reciptant = user["email"]
        password = user["password"]

        message = f"""
Hi There,

We're excited to inform you that your profile has been successfully created on our platform. You're now all set to access your account and begin utilizing our range of services. Below, you'll find your login details:

Password: {password}

Please take a moment to log in and securely update your password. Upon logging in, you'll be prompted to upload the necessary documents as part of the onboarding process.

If you encounter any issues or have questions, feel free to reach out to our dedicated support team at [Support Email Address] or [Support Phone Number].

Thank you for choosing [Your Company Name]. We look forward to serving you!

Best regards,
Team H.R.

    """

        # graph.send_mail(subject, message, reciptant)

        payload = {
            "reciptant": reciptant,
            "subject": subject,
            "body": message
        }

        requests.post("http://3.84.79.77:8000/mail/send", data=json.dumps(payload))
################################################################################################################    
@app.get("/download_excel/{template}/")
async def download_excel(template: str) -> FileResponse:
    excel_file_path = os.path.join("excel", template)

    if not os.path.exists(excel_file_path):
        return {"error": f"File '{template}' not found."}

    return FileResponse(
        path=excel_file_path,
        headers={"Content-Disposition": f'attachment; filename="{template}"'},
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

"""@app.post("/upload_excel/")
async def upload_excel_file(file: UploadFile = File(...)) -> dict:
    file_save_path = os.path.join("excel", file.filename)
    with open(file_save_path, "wb") as f:
        f.write(await file.read())
    return {"message": "File uploaded and saved successfully"}"""