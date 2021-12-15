from cloudant.client import Cloudant
from cloudant.query import Query
from cloudant.result import QueryResult
from cloudant.error import CloudantException
import requests


def main(dict):
    databaseName = "reviews"
    
    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        reviews = client[databaseName]
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}
    if "review" in dict.keys():
        my_document = reviews.create_document(dict['review'])
        # Check that the document exists in the database
        if my_document.exists():
            return my_document
    elif 'dealerId' in dict.keys():
        selector={"id":{"$eq":dict['dealerId']}}
        query = Query(reviews,fields=['id','name','dealership','review','purchase','purchase_date','car_make','car_model','car_year'],selector=selector)
        results={"rows":[]}
        for result in QueryResult(query):
            results["rows"].append(result)
        return results
    else:
        return {"err": 'No parameters provided.' }