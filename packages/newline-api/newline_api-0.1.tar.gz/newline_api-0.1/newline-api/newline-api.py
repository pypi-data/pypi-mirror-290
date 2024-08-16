import requests, json
def action(params):
    return requests.post('http://localhost:8085/actions', 
        headers={'Content-Type': 'application/json'}, 
        data=json.dumps(params)
    ).json()['content']