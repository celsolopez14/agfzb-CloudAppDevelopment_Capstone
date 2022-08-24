import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
#import os
#from dotenv import load_dotenv


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def  get_request(url, **kwargs):

    print(kwargs)
    print("GET from {}".format(url))
    if "api_key" in kwargs:
        try:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=params,
            auth = HTTPBasicAuth('apikey', kwargs["api_key"]))
    
        except:
            print("Network exception occurred")

    else:
        try:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        
        except:
            print("Network exception occurred")

    status_code = response.status_code
    print("With status {}".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):

    try:
        response = requests.post(url, params=kwargs, json=json_payload)

    except:
        print("Network exception occurred")
    
    status_code = response.status_code
    print("With status {}".format(status_code))
    json_data = json.loads(response.text)

    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["dealerships"]
        for dealer in dealers:
            dealer_obj = CarDealer(address = dealer["address"], city = dealer["city"], 
            full_name = dealer["full_name"], id = dealer["id"], lat = dealer["lat"], 
            long = dealer["long"], short_name = dealer["short_name"], st = dealer["st"], zip = dealer["zip"])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealers_by_state_from_cf(url, **kwargs):
    results = []
    if "state" in kwargs:
        json_result = get_request(url, **kwargs)
    json_result = get_request(url,**kwargs)
    if json_result:
        dealers = json_result["dealerships"]
        for dealer in dealers:
            dealer_obj = CarDealer(address = dealer["address"], city = dealer["city"], 
            full_name = dealer["full_name"], id = dealer["id"], lat = dealer["lat"], 
            long = dealer["long"], short_name = dealer["short_name"], st = dealer["st"], zip = dealer["zip"])
            results.append(dealer_obj)
    return results

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    if "dealerId" in kwargs:
        json_result = get_request(url, **kwargs)
    if json_result:
        reviews = json_result["reviews"]
        for review in reviews:
            review_obj = DealerReview(dealership = review["dealership"], name = review["name"],
            purchase = review["purchase"], id = review["id"], review = review["review"],
            purchase_date = review["purchase_date"], car_make = review["car_make"], 
            car_model = review["car_model"], car_year = review["car_year"], sentiment = '')
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results
        


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealer_review): 

    #load_dotenv()
    #api_key = os.getenv('WATSON_API_KEY')
    #url = os.getenv("URL_WATSON")
    url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/c3e54c58-3256-44b7-b8bb-c676589df47c"
    api_key = "876IJZI8sC9b5-Ypig0jDsTLK88AuiLN31ntLdsc7d2U"

    authenticator = IAMAuthenticator(api_key) 
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07',
    authenticator=authenticator)

    natural_language_understanding.set_service_url(url) 
    response = natural_language_understanding.analyze( text=dealer_review ,
    features=Features(sentiment=SentimentOptions(targets=[dealer_review]))).get_result() 

    rev_sentiment=json.dumps(response, indent=2) 

    rev_sentiment = response['sentiment']['document']['label'] 

    return rev_sentiment
    




