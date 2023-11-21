import requests
import json

def get_reserve_info():

    url = "http://127.0.0.1:17767/json_rpc"

    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "jsonrpc": "2.0",
        "id": "0",
        "method": "get_reserve_info",
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


if __name__ == "__main__":
    print(get_reserve_info())