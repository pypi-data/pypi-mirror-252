import requests
from datetime import datetime, timedelta
import json


class OneNet:
    def __init__(self):
        self.get_url = None
        self.get_device = None
        self.datastream_id = None
        self.limit = None
        self.authorization = None
        self.time_delta_milliseconds = None

        self.push__url = None
        self.push_device = None
        self.masterkey = None

    def set_get_url(self, get_url):
        self.get_url = get_url

    def set_push_url(self, push_url):
        self.push_url = push_url

    def set_get_device(self, get_device):
        self.get_device = get_device

    def set_push_device(self, push_device):
        self.push_device = push_device

    def set_datastream_id(self, datastream_id):
        self.datastream_id = datastream_id

    def set_limit(self, limit):
        self.limit = limit

    def set_authorization(self, authorization):
        self.authorization = authorization

    def set_masterkey(self, masterkey):
        self.masterkey = masterkey

    def set_time_delta_milliseconds(self, time_delta_milliseconds):
        self.time_delta_milliseconds = time_delta_milliseconds

    def handle_get_response(self, json_response):
        if json_response.get('errno') == 0 and not json_response['data']['datastreams']:
            print("No data available.")
        elif json_response.get('errno') != 0:
            print(f"Error occurred: {json_response.get('error')}")
        else:
            datastreams = json_response['data']['datastreams']
            result_string = []
            for stream in datastreams:
                datapoints = stream['datapoints']
                for point in datapoints:
                    time = point['at']
                    value = point['value']
                    print(f"时间为 {time} and 数据为 {value}")
                    result_string.append(value)
                    result_string.append(time)
            return result_string

    def handle_push_response(self, response):
        response_code = response.status_code
        print("Response Code:", response_code)

        if response_code == requests.codes.ok:
            response_text = response.text
            print("Response:", response_text)
        else:
            print("Request failed")

    def doGet(self, formatted_time):
        try:
            headers = {
                'Content-type': 'application/json',
                'authorization': self.authorization
            }
            # onenet.set_get_url("http://api.heclouds.com/devices/1184037843/datapoints")
            url = f"{self.get_url}/{self.get_device}/datapoints?datastream_id={self.datastream_id}&start={formatted_time}&limit={self.limit}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            result = response.json()
            print(json.dumps(result, indent=4))
            return self.handle_get_response(result)

        except requests.RequestException as e:
            print(e)
            return None

    def Pushdata(self, json_input_string):
        try:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'api-key': self.masterkey
            }
            # onenet.set_push_url("https://api.heclouds.com/cmds?device_id=1184037843")
            push_url=f"{self.push_url}{self.push_device}"
            response = requests.post(push_url, headers=headers, data=json_input_string)
            return self.handle_push_response(response)

        except Exception as e:
            print(e)

    def Getdata(self):
        now = datetime.now()
        past_time = now - timedelta(milliseconds=self.time_delta_milliseconds)
        formatted_time = past_time.strftime("%Y-%m-%dT%H:%M:%S")
        return self.doGet(formatted_time)
