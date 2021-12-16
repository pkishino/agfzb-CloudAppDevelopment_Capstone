#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.query import Query
from cloudant.result import QueryResult
from cloudant.error import CloudantException
import requests


def main(dict):
    databaseName = "dealerships"
    
    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        dealerships = client[databaseName]
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce,"code":500}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err,"code":500}

    message="The database is empty"
    if "state" in dict.keys():
        selector={"st":{"$eq":dict['state']}}
        message="The state does not exist"
    elif "dealerId" in dict.keys():
        selector={"id":{"$eq":int(dict['dealerId'])}}
        message="This dealership does not exist"
    else:
        selector={"id":{"$gte":0}}
        
    query = Query(dealerships,fields=['id','city','state','st','address','zip','lat','long','short_name','full_name'],selector=selector)
    results=[]
    for result in QueryResult(query):
        results.append(result)
    if results:
        return {"body":results}
    else:
        return {
                "code":404,
                "error":{
                    "message": message
                }}
