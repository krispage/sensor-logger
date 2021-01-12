import json
import requests

data = {
    "identifier": "<<identifier here>>",
    "data": {
        "foo": "bar"
        }
}

secret_key= "<<secret key here>>"


url = 'http://<<my server here>>:5000/data'
res = requests.post(url, headers={'Authorization': 'Bearer ' + secret_key,
    "Content-Type": "application/json", "Accept": "application/json"},
    data=json.dumps(data))
print(res.text)
res.close()
