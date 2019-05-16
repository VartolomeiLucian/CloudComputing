import configparser
import logging
import json
import requests
import re
import random
from flask import Flask, app, jsonify
from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from azure.cognitiveservices.search.websearch import WebSearchAPI
from azure.cognitiveservices.search.websearch.models import SafeSearch
from msrest.authentication import CognitiveServicesCredentials

app = Flask(__name__)
URL_FIND_PLACES = "https://atlas.microsoft.com/search/poi/json?" \
                  "api-version=1&query={type}%&subscription-key=" \
                  "{APIKEY}&lat={lat}&lon={lng}&radius={radius}"

LAT = "47.165475"
LNG = "27.580282"
RADIUS = 10000
TYPE = "restaurant"

def return_azure_maps_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['azure_maps_api']['api_key']

    return api_key

def return_bing_image_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['azure_search_api']['api_key_search']

    return api_key

def find_places_api():
    url_find_places = URL_FIND_PLACES.format(type=TYPE,
                                             APIKEY=return_azure_maps_api_key(), lat=LAT, lng=LNG, radius=RADIUS)
    places_info = dict()
    places_info["restaurants"] = []
    response = requests.get(url_find_places)
    res = json.loads(response.text)
    print(url_find_places)

    for result in res["results"]:
        restaurant_info = dict()
        restaurant_info["titlu"] = replace_characters(result["poi"]["name"])
        restaurant_info["address"] = replace_characters(result["address"]["streetName"]) \
                                     + " " + result["address"]["streetNumber"]

        place_details(restaurant_info["titlu"], restaurant_info)
        photo_from_place(restaurant_info["titlu"], restaurant_info)
        places_info["restaurants"].append(restaurant_info)

    return jsonify(places_info)

def photo_from_place(search_place, restaurant_info):
    api_key = return_bing_image_api_key()
    credentials = ImageSearchAPI(CognitiveServicesCredentials(api_key))
    search_place = search_place + " Iasi Romania"
    image_results = credentials.images.search(query=search_place)
    total_number_of_results = len(image_results.value)
    random_image = random.randint(0, total_number_of_results)

    if image_results.value:
        image_result = image_results.value[0]
        restaurant_info["url"] = image_result.content_url
    else:
        restaurant_info["url"] = "No image results returned!"

def place_details(search_place, restaurant_info):
    api_key = return_bing_image_api_key()
    credentials = WebSearchAPI(CognitiveServicesCredentials(api_key))
    information = credentials.web.search(query=search_place)

    if hasattr(information.web_pages, 'value'):
        web_page = information.web_pages.value[0]
        print(web_page.snippet)
        restaurant_info["snippet"] = replace_characters(web_page.snippet)
    else:
        restaurant_info["snippet"] = "Didn't find any web pages!"


def replace_characters(text):
    text = re.sub("\\n", " ", text)
    text.replace('\\', "'")
    text = re.sub("\u2019", "'", text)
    text = re.sub("\u2019", "'", text)
    text = re.sub("\u015f", "s", text)
    text = re.sub("\u0219", "s", text)
    text = re.sub("\u00ee", "i", text)
    text = re.sub("\u021b", "t", text)
    text = re.sub("\u0103", "a", text)
    text = re.sub("\u00e2", "a", text)
    text = re.sub("\u0218", "S", text)
    text = re.sub("\u0163", "t", text)
    text = re.sub("\u03361", "1", text)
    text = re.sub("\u03367", "7", text)
    text = re.sub("\u03365", "5", text)
    text = re.sub("\u0336", "", text)


    return text

@app.route('/')
def places_api():
    """Return a friendly HTTP greeting."""
    return find_places_api()

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=8080, debug=True)
# # [END gae_flex_quickstart]
