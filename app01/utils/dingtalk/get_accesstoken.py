# coding = utf-8
import requests
import json

host = "https://api.dingtalk.com"
endpoint = "/v1.0/oauth2/accessToken"

url = ''.join([host, endpoint])
headers = {
    "Content-Type": "application/json"
}
body = {
        "appKey": "dingyxlaspxbccsj4ppu",
        "appSecret": "38dIeS7lD6bpMZFfpG3JvjvMb5hX7P8ziWzGw-W5ih4McDBrpez9u4nmv0W0R0L1"
    }
r = requests.post(url, headers=headers, data=json.dumps(body))
print(r.text)
