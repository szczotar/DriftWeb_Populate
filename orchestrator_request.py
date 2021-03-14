import requests
import json
import sys
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
            return access_token

    except Exception as err:
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
            return(print("Item successfuly added"))

    except Exception as err:
        print(sys.exc_info())

    except:
        print(sys.exc_info())

if __name__ == "__main__":
    access_token = Get_token("Artur","8DEv1AMNXczW3y4U15LL3jYf62jK93n5",
    "MipuhkUYB5eN_fdW3dAzE0mK2RzwzKUy_CiE_HhBv7JSX")
    Content = Content = {"T_number":"T1993","Name":"Artur"}
    Add_queue_item("burki","Artur","1269","DriftWeb",access_token,Content)




    