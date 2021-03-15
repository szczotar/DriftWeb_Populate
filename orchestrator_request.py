import requests
import json
import sys
import logging
import logging.handlers
import os
import datetime


handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", r"C:\Users\admin\Desktop\Env\new_env\DriftWeb_populate\logs.txt"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)
 


def Get_token(Tenant_logical_name,Client_ID,User_key):
    url = "https://account.uipath.com/oauth/token"
    try:

        head = {
        'Content-Type':'application/json',
        'X-UIPATH-TenantName': Tenant_logical_name
        }

        body = {
        'grant_type': 'refresh_token',
        'client_id': Client_ID,
        'refresh_token': User_key}

        request = requests.post(url,headers=head,json=body)
        status_code = request.status_code
        if status_code != 200:
            raise Exception("Request failed") 
        else:
            access_token = "Bearer " + request.json()['access_token']
            logging.info(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S" + 
            " access token generated"))
            return access_token

    except Exception as err:
        logging.exception(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        print(repr(err))

    
def Add_queue_item(Account_logical_name,Tenant_logical_name,OrganizationUnitId,QueueName,access_token,Content):
    base_url = f"https://cloud.uipath.com/{Account_logical_name}/{Tenant_logical_name}"
    task_url = "/odata/Queues/UiPathODataSvc.AddQueueItem"
    
    try:
        head = {
            "Authorization" : access_token,
            "X-UIPATH-TenantName": Tenant_logical_name,
            "X-UIPATH-OrganizationUnitId" : OrganizationUnitId
            }

        queueItem = {
            "itemData": {
                "Name": QueueName,
                "Priority": "Normal",
                "SpecificContent": Content
                }
            }
        request = requests.post(url = base_url+task_url,headers = head,json=queueItem)
        if request.status_code != 201:
            raise Exception("Request failed") 
        else:     
            logging.info("Item successfuly added. Transaction ID: " +request.json()['Key'])
            return(print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") +
            " Item successfuly added. Transaction ID: " +request.json()['Key']))
            
    except Exception as err:
        logging.exception(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") +" Bad request")
        print(sys.exc_info())

    except:
        logging.exception(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") +" Bad request")
        print(sys.exc_info())

         