import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

api_base="https://1b29c55a.au-syd.apigw.appdomain.cloud/api"

def get_request(url, **kwargs):
    print(kwargs)
    
    try:
        if "api_key" in kwargs:
            params=dict()
            params["text"]=kwargs["text"]
            params["version"]=kwargs["version"]
            params["features"]=kwargs["features"]
            params["return_analyzed_text"]=kwargs["return_analyzed_text"]
            response = requests.get(url,params=params,headers={'Content-Type': 'application/json'},
                auth=HTTPBasicAuth('apikey',kwargs["api_key"]))

            print("Response_apikey_Provided: ",response)

        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        print("Network exception occurred")
    print("GET from {} ".format(response.url))
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    print(json_data)
    return json_data

def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} with:{}".format(url, json_payload))
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    print(json_data)
    return json_data


def get_dealers_from_cf(**kwargs):
    url = api_base+"/dealership"
    results = []
    json_result = get_request(url,**kwargs)
    if "body" in json_result.keys():
        dealers = json_result["body"]
        for dealer in dealers:
            dealer_obj = CarDealer(**dealer)
            results.append(dealer_obj)

    return results

def get_dealer_with_id_from_cf(dealer_id):
    return get_dealers_from_cf(dealerId=dealer_id)

def get_dealer_with_state_from_cf(state):
    return get_dealers_from_cf(state=state)

def get_dealer_reviews_from_cf(**kwargs):
    url = api_base+"/review"
    results = []
    json_result = get_request(url,**kwargs)
    if json_result and "body" in json_result.keys():
        reviews = json_result["body"]
        for review in reviews:
            review_obj = DealerReview(**review)
            review_obj.sentiment=analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results

def analyze_review_sentiments(text):
    api_url="https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/0b1c9b69-f4f7-407f-9440-e57e5294e92c/v1/analyze"

    parameters={
        "api_key":"b9gt_MGLjI21PZEz7_brkGL-cD3UbS-CWuk-nRNLtibR",
        "text":text,
        "version":"2021-08-01",
        "features":"sentiment",
        "return_analyzed_text":True
    }
    response=get_request(api_url,**parameters)
    if 'sentiment' in response.keys():
        return response['sentiment']['document']['label']
    else:
        return 'neutral'

def post_review(review):
    url = api_base+"/review"
    return post_request(url, json_payload=review)


