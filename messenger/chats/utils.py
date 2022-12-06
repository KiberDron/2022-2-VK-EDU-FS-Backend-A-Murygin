import json
import requests
from bs4 import BeautifulSoup


def publish_message(message, channel="chat"):
    command = {
        "method": "publish",
        "params": {
            "channel": channel,
            "data": message
        }
    }

    parsed_config = parse_json_config('config.json')
    api_key = parsed_config['api_key']

    data = json.dumps(command, default=str)

    headers = {'Content-type': 'application/json', 'Authorization': 'apikey ' + api_key}
    requests.post("http://localhost:8000/api", data=data, headers=headers)


def parse_json_config(json_file):
    with open(json_file) as json_data:
        data = json.load(json_data)
    return data


def clear_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    clean_text = soup.get_text()
    return clean_text
