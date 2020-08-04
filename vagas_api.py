import requests
from json_utils import Json_utils as JU


def main():
    api_url, options = JU.read_json('./api_secret.json').values()
    res = requests.get(api_url, json=options)
    try:
        if res.status_code != 200:
            raise Exception(f'Cannot GET. Code {res.status_code}')
    except Exception as e:
        print(e)
    else:
        pagination, data, facets = res.json().values()
        actual_page, page_count, items_total = pagination.values()
        JU.write_json('./data.json', data)


if __name__ == '__main__':
    main()
