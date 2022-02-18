import  requests
import json

def get_quote(url):

    response = requests.get(url)
    if response.status_code == 200:
        res_json = json.loads(response.text)
        if res_json.get('content', None):
            return res_json['content']
    return 'Invalid quote resource'

uri = input()
print(get_quote(uri))