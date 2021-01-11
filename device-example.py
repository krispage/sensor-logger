import json
import requests

data = {
    "identifier": "test_python",
    "data": {
        "foo": "bar"
        }
}

secret_key= "a341c0b4aed42473e5d829a25195ee56"


url = 'http://127.0.0.1:5000/data'
res = requests.post(url, headers={'Authorization': 'Bearer ' + secret_key,
    "Content-Type": "application/json", "Accept": "application/json"},
    data=json.dumps(data))
print(res.text)
res.close()
