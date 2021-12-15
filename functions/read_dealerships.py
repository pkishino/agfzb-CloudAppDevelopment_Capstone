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
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}
    if "state" in dict.keys():
        selector={"st":{"$eq":dict['state']}}
    elif 'dealerId' in dict.keys():
        selector={"id":{"$eq":dict['dealerId']}}
    else:
        selector={"id":{"$gte":0}}
        
    query = Query(dealerships,fields=['id','city','state','st','address','zip','lat','long','short_name','full_name'],selector=selector)
    results={"rows":[]}
    for result in QueryResult(query):
        results["rows"].append(result)
    return results