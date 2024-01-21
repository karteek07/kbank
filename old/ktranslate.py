import requests, uuid, json
import sys

key = "dc91f0fe80224b99b4a602afe488255d"
endpoint = "https://api.cognitive.microsofttranslator.com"
location = "centralindia"

path = '/translate'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'from': 'en',
    'to': 'hi'
}

headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

body = [{
    'text': sys.argv[1]
}]

request = requests.post(constructed_url, params=params, headers=headers, json=body)
response = request.json()

# print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
print(response[0]['translations'][0]['text'])