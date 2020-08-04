import requests
import json


def read_json(file):
    with open(file) as json_file:
        return json.load(json_file)


def main():
    secrets = read_json('./api_secret.json')
    api_url = secrets['api_url']
    options = secrets['options']
    res = requests.get(api_url, json=options)
    if res.status_code != 200:
        print('Something went wrong!!')
    else:
        print(res.json()['pagination'])


if __name__ == '__main__':
    main()
