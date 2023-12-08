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
        print(f"Error parsing the translation response: {data}")
        return None
