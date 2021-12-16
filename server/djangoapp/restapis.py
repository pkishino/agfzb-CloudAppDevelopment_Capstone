import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


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
    print(json_payload)
    print("POST to {} ".format(url))
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    print(json_data)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url,**kwargs)
    if "body" in json_result.keys():
        dealers = json_result["body"]
        for dealer in dealers:
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],state=dealer["state"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url,**kwargs)
    if "body" in json_result.keys():
        reviews = json_result["body"]
        for review in reviews:
            review_obj = DealerReview(dealership=review["dealership"],name=review["name"],purchase=review["purchase"],
                                        purchase_date=review["purchase_date"],review=review["review"],car_make=review["car_make"],car_model=review["car_model"],
                                        car_year=review["car_year"],id=review["id"])
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



