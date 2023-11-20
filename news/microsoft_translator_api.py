import http.client
import json

def translate(to, text):
    conn = http.client.HTTPSConnection("microsoft-translator-text.p.rapidapi.com")

    payload = json.dumps([{"Text": text}])

    headers = {
        'content-type': 'application/json',
        'X-RapidAPI-Key': '729ad8cb4bmshc2f04df14ef2a65p1e623djsne81bc94a5d3d',
        'X-RapidAPI-Host': 'microsoft-translator-text.p.rapidapi.com'
    }

    conn.request("POST", f"/translate?to[0]={to}&api-version=3.0", payload, headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")

    try:
        translation = json.loads(data)[0]['translations'][0]['text']
        print(f"translation!!!!!!!!!!!!!!!! {translation}")
        return translation
    except (KeyError, IndexError):
        # Handle the case when the expected keys are not present in the response
        print(f"Error parsing the translation response: {data}")
        return None



# import json
# import requests
# import gzip
# from io import BytesIO
# import time
#
#
# def translate(to, text, max_retries=3, delay=2):
#     url = "https://microsoft-translator-text.p.rapidapi.com/translate"
#     querystring = {"to[0]": to, "api-version": "3.0", "profanityAction": "NoAction", "textType": "plain"}
#
#     payload = [{"Text": text}]
#     headers = {
#         "content-type": "application/json",
#         "X-RapidAPI-Key": "729ad8cb4bmshc2f04df14ef2a65p1e623djsne81bc94a5d3d",
#         "X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com",
#         "Accept-Encoding": "gzip"
#     }
#
#     for attempt in range(max_retries):
#         try:
#             response = requests.post(url, json=payload, headers=headers, params=querystring)
#             response.raise_for_status()
#             print(response.content)
#
#             if 'gzip' in response.headers.get('content-encoding', '').lower():
#                 content = gzip.decompress(response.content).decode('utf-8')
#             else:
#                 content = response.content.decode('utf-8')
#
#             response_data = json.loads(content)
#             return response_data[0]['translations'][0]['text']
#         except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
#             if attempt < max_retries - 1:
#                 # Sleep before retrying
#                 time.sleep(delay)
#             else:
#                 raise e



# import json
# import urllib.request
# import urllib.parse
# import time
#
# def translate(to, text, max_retries=3, delay=2):
#     url = "https://microsoft-translator-text.p.rapidapi.com/translate"
#     querystring = {"to[0]": to, "api-version": "3.0", "profanityAction": "NoAction", "textType": "plain"}
#
#     payload = [{"Text": text}]
#     headers = {
#         "content-type": "application/json",
#         "X-RapidAPI-Key": "729ad8cb4bmshc2f04df14ef2a65p1e623djsne81bc94a5d3d",
#         "X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com",
#         "Accept-Encoding": "gzip"
#     }
#
#     print(f"URL: {url}")
#     print(f"Payload: {payload}")
#     print(f"Headers: {headers}")
#     # Encode payload as JSON
#     data = json.dumps(payload).encode('utf-8')
#
#     # Create the request
#     request = urllib.request.Request(url, data=data, headers=headers, method='POST')
#
#     for attempt in range(max_retries):
#         try:
#             with urllib.request.urlopen(request) as response:
#                 response_data = json.loads(response.read().decode('utf-8'))
#             return response_data[0]['translations'][0]['text']
#         except OSError as e:
#             if attempt < max_retries - 1:
#                 # Sleep before retrying
#                 time.sleep(delay)
#             else:
#                 raise e
