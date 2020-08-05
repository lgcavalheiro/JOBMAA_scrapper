import requests
from ...utils.json_utils import JsonUtils as JU


def request_data(api_url, options, results=[]):
    try:
        print(f'Requesting data, page: {options["pagina"]}')
        res = requests.get(api_url, json=options)
        if res.status_code != 200:
            raise Exception(f'Cannot GET. Code {res.status_code}')
    except Exception as e:
        print(e)
    else:
        pagination, data, facets = res.json().values()
        actual_page, page_count, items_total = pagination.values()
        results.extend(data)
        if actual_page <= 2:  # page_count for prod, 2 for dev
            options['pagina'] += 1
            request_data(api_url, options, results)
        else:
            JU.write_json('src/results/vagas_api_data.json', results, 'a')
            print(f'Requests finished, pulled a total of {items_total} items.')


def main():
    api_url, options = JU.read_json(
        'src/secrets/vagas_api_secret.json').values()
    request_data(api_url, options)


if __name__ == '__main__':
    main()
