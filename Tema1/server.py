from urllib.parse import urlparse, parse_qs
import async
import requests as req
import random
import json
from http.server import *
import socketserver
import logging
import re
import configparser

capital_cities = ["Kabul", "Tirane", "Algiers", "Vienna", "Bucharest", "Minsk",
                  "Brussels", "Sofia", "Beijing", "Bogota", "Zagreb", "Havana",
                  "Helsinki", "Berlin", "Budapest", "Dublin", "Pristina", "Luxembourg",
                  "Chisinau", "Podgorica", "Oslo", "Lisbon", "Moscow", "Madrid", "Bangkok"]

PORT = 8082
logging.basicConfig(filename='application.log', level=logging.INFO, format='%(asctime)s - %(message)s')


class MyRequestHandler(SimpleHTTPRequestHandler):

    def set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def capital_city_ws_response(self):
        self.set_headers()
        city_name = random.choice(capital_cities)
        response_to_client_city_ws = capital_city_web_service(city_name)
        print(response_to_client_city_ws)
        json_string = json.dumps(response_to_client_city_ws)
        self.wfile.write(json_string.encode())

        return response_to_client_city_ws

    def forecast_ws_response(self):
        self.set_headers()
        lat_long_parameters = self.capital_city_ws_response()
        lat = lat_long_parameters['lat']
        long = lat_long_parameters['long']
        response_to_client_forecast_ws = forecast_web_service(lat, long)
        print(response_to_client_forecast_ws)
        json_string = json.dumps(response_to_client_forecast_ws)
        self.wfile.write(json_string.encode())

        return response_to_client_forecast_ws

    def md5_ws_response(self):
        self.set_headers()
        city_ws_info = self.capital_city_ws_response()
        forecast_ws_info = self.forecast_ws_response()
        response_to_client_md5_ws = md5_web_service(city_ws_info, forecast_ws_info)
        print(response_to_client_md5_ws)
        json_string = json.dumps(response_to_client_md5_ws)
        self.wfile.write(json_string.encode())

        return response_to_client_md5_ws

    def metrics_api_response(self):
        self.set_headers()
        response_to_client_metrics_values = metrics_response()
        print(response_to_client_metrics_values)
        self.wfile.write(response_to_client_metrics_values.encode())

        return response_to_client_metrics_values

    def concurrent_nr_of_request(self):
        number_of_request = 20

        for i in range(number_of_request):
            random_web_service = random.randint(1, 3)
            if random_web_service == 1:
                self.capital_city_ws_response()
            elif random_web_service == 2:
                self.forecast_ws_response()
            else:
                self.md5_ws_response()

        self.metrics_api_response()

    def do_GET(self):
        url_path = urlparse(self.path).path
        try:
            if url_path == "/city":
                self.capital_city_ws_response()
                return

            if url_path == "/forecast":
                self.forecast_ws_response()
                return

            if url_path == "/md5":
                self.md5_ws_response()
                return

            if url_path == "/metrics":
                self.metrics_api_response()
                return

            if url_path == "/concurrent_requests":
                self.concurrent_nr_of_request()
                return

            f = self.send_head()
            if f:
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    f.close()
            return

        except IOError:
            self.send_error(404, 'Page Not Found')
        return


def capital_city_web_service(city_name):
    print(city_name)

    # Preparing for request
    url_api = 'https://restcountries.eu/rest/v2/capital/{}'.format(city_name)
    print(url_api)

    response_message = req.request('GET', url_api)
    logging.info('web-service: capital_city_web_service status:{} response:{} latency:{} \n'.format(
        response_message.status_code, response_message.text, response_message.elapsed.total_seconds()))

    # print(response_message.json()[0]['latlng'][0])
    info_response_message = dict()

    if len(response_message.json()[0]['latlng']) != 0:
        info_response_message['lat'] = response_message.json()[0]['latlng'][0]
        info_response_message['long'] = response_message.json()[0]['latlng'][1]
    else:
        info_response_message['lat'] = random.randint(-100, 100)
        info_response_message['long'] = random.randint(-100, 100)

    return info_response_message

def forecast_web_service(lat, long):
    print(lat, long)

    # Preparing for request
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['forecast_service']['api_key']
    url_api = 'https://api.darksky.net/forecast/{}/{},{}'.format(api_key, lat, long)
    print(url_api)

    response_message = req.request('GET', url_api)
    logging.info('web-service: forecast_web_service status:{} response:{} latency:{} \n'.format(
        response_message.status_code, response_message.text, response_message.elapsed.total_seconds()))

    info_response_message = dict()

    if len(response_message.json()) != 0:
        info_response_message["timezone"] = response_message.json()["timezone"]
        info_response_message["summary"] = response_message.json()["currently"]["summary"]
        info_response_message["precipitation-probability"] = response_message.json()["currently"]["precipProbability"]
        info_response_message["temeperature"] = response_message.json()["currently"]["temperature"]
        info_response_message["apparent-temperature"] = response_message.json()["currently"]["apparentTemperature"]
        info_response_message["temeperature"] = response_message.json()["currently"]["temperature"]
        info_response_message["dew-point"] = response_message.json()["currently"]["dewPoint"]
        info_response_message["humidity"] = response_message.json()["currently"]["humidity"]
        info_response_message["air-pressure"] = response_message.json()["currently"]["pressure"]
        info_response_message["wind-speed"] = response_message.json()["currently"]["windSpeed"]
        info_response_message["wind-gust"] = response_message.json()["currently"]["windGust"]
        info_response_message["cloud-cover"] = response_message.json()["currently"]["cloudCover"]
        info_response_message["uv-index"] = response_message.json()["currently"]["uvIndex"]
        info_response_message["ozone"] = response_message.json()["currently"]["ozone"]

    return info_response_message


def md5_web_service(city_info, forecast_info):
    print(city_info, forecast_info)

    # Preparing for request
    string_for_encryption = ""
    string_for_encryption = str(city_info) + str(forecast_info)
    url_api = 'https://md5.pinasthika.com/api/encrypt?value={}'.format(string_for_encryption)
    print(url_api)

    response_message = req.request('GET', url_api)
    logging.info('web-service: md5_web_service status:{} response:{} latency:{} \n'.format(
        response_message.status_code, response_message.text, response_message.elapsed.total_seconds()))

    info_response_message = dict()

    if len(response_message.json()) != 0:
        info_response_message["status"] = response_message.json()["status"]
        info_response_message["md5-encryption-result"] = response_message.json()["result"]

    return info_response_message


def metrics_response():
    with open('application.log', 'r') as fd:
        file_content = fd.read()

    status_values = [[], [], []]
    latencies_values = [[], [], []]
    status_codes_values = [{}, {}, {}]

    # Add information about web servicies from application.log
    ws_info = []
    ws_info.append(re.findall("capital_city_web_service(.+)", file_content))
    ws_info.append(re.findall("forecast_web_service(.+)", file_content))
    ws_info.append(re.findall("md5_web_service(.+)", file_content))

    for i in range(0, 3):
        for info in ws_info[i]:
            latencies_values[i].append(float(re.search("latency:(\d+\.\d+)", info).group(1)))

    for i in range(0, 3):
        for info in status_values[i]:
            status_codes_values[i][info] = status_values[i].count(info)

    # Metrics for city_web_service

    if len(latencies_values[0]) != 0:
        nr_of_requests_md5_ws = len(latencies_values[0])
        latency_forecast_ws = sum(latencies_values[0])
        min_latency_value_forecast_ws = min(latencies_values[0])
        max_latency_value_forecast_ws = max(latencies_values[0])
        avg_latency_value_forecast_ws = latency_forecast_ws / nr_of_requests_md5_ws
    else:
        min_latency_value_forecast_ws = 0
        max_latency_value_forecast_ws = 0
        avg_latency_value_forecast_ws = 0

    metrics_values = "Web-Service: Capital_City\n" \
                     "Number of requests:{} \n".format(len(ws_info[0]))

    metrics_values = metrics_values + "Min latency:{}\n".format(min_latency_value_forecast_ws)
    metrics_values = metrics_values + "Max latency:{}\n".format(max_latency_value_forecast_ws)
    metrics_values = metrics_values + "Avg latency:{}\n\n".format(avg_latency_value_forecast_ws)

    # Metrics for forecast_web_service

    if len(latencies_values[1]) != 0:
        nr_of_requests_forecast_ws = len(latencies_values[1])
        latency_forecast_ws = sum(latencies_values[1])
        min_latency_value_forecast_ws = min(latencies_values[1])
        max_latency_value_forecast_ws = max(latencies_values[1])
        avg_latency_value_forecast_ws = latency_forecast_ws / nr_of_requests_forecast_ws
    else:
        min_latency_value_forecast_ws = 0
        max_latency_value_forecast_ws = 0
        avg_latency_value_forecast_ws = 0

    metrics_values = metrics_values + "Web-Service: Forecast\n" \
                                      "Number of requests:{} \n".format(len(ws_info[1]))

    metrics_values = metrics_values + "Min latency:{}\n".format(min_latency_value_forecast_ws)
    metrics_values = metrics_values + "Max latency:{}\n".format(max_latency_value_forecast_ws)
    metrics_values = metrics_values + "Avg latency:{}\n\n".format(avg_latency_value_forecast_ws)

    # Metrics for md5_web_service

    if len(latencies_values[2]) != 0:
        nr_of_requests_md5_ws = len(latencies_values[2])
        latency_md5_ws = sum(latencies_values[2])
        min_latency_value_md5_ws = min(latencies_values[2])
        max_latency_value_md5_ws = max(latencies_values[2])
        avg_latency_value_md5_ws = latency_md5_ws / nr_of_requests_md5_ws
    else:
        min_latency_value_md5_ws = 0
        max_latency_value_md5_ws = 0
        avg_latency_value_md5_ws = 0

    metrics_values = metrics_values + "Web-Service: MD5\n" \
                                      "Number of requests:{} \n".format(len(ws_info[2]))

    metrics_values = metrics_values + "Min latency:{}\n".format(min_latency_value_md5_ws)
    metrics_values = metrics_values + "Max latency:{}\n".format(max_latency_value_md5_ws)
    metrics_values = metrics_values + "Avg latency:{}\n".format(avg_latency_value_md5_ws)

    return metrics_values


urls = ['http://localhost:8082/city',
        'http://localhost:8082/forecast',
        'http://localhost:8082/md5']


def run_server(server, handler):
    print('HTTP Server is starting...')
    server_addr = ('127.0.0.1', PORT)
    httpd = server.ThreadingTCPServer(server_addr, handler)
    print('HTTP Server listening on PORT:', PORT)
    print('HTTP Server is running!')
    httpd.serve_forever()


if __name__ == "__main__":
    run_server(socketserver, MyRequestHandler)
