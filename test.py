import requests
import json
from requests.auth import HTTPBasicAuth

header = {"content-type": "application/json"}

data = {"grant_type": "authorization_code", "code": "MtVCaJSBxq5Gj669"}
a = requests.post("https://api.lyft.com/oauth/token",
                  headers=header,
                  data=json.dumps(data),
                  auth=HTTPBasicAuth("FDiIAIdqtrzy", "fymu7KD2MvS6Wxfk1Wzz7kE_qE9gH5wm"))

print(a.text)
print(a.headers)