import requests
from ...utils.json_utils import JsonUtils as JU


class VagasApiConnector:
    def __init__(self):
        self.api_url, self.options = JU.read_json(
            'src/secrets/vagas_api_secret.json').values()

    def main(self):
        actual_page = 0
        page_count = 1
        results = []
        while actual_page < page_count:  # page_count for prod, 2 for dev
            res = self.request_data()
            pagination, data, facets = res.json().values()
            actual_page, page_count, items_total = pagination.values()
            results.extend(data)
            self.options['pagina'] += 1
        JU.write_json(
            'src/results/vagas_api_data.json', results, 'a')
        print(
            f'Requests finished, pulled a total of {items_total} items.')

    def request_data(self):
        print(f'Requesting data, page: {self.options["pagina"]}')
        res = requests.get(self.api_url, json=self.options)
        print('RES: ', res)
        if res.status_code != 200:
            raise Exception(f'Cannot GET. Code {res.status_code}')
        else:
            return res


if __name__ == '__main__':
    VAP = VagasApiConnector()
    VAP.main()
