import unittest
from ...utils.json_utils import JsonUtils as JU


class VagasApiTests(unittest.TestCase):
    def setUp(self):
        self.api_url, self.options = JU.read_json(
            'src/secrets/vagas_api_secret.json').values()

    def tearDown(self):
        return super().tearDown()

    def test_vagas_api_credentials(self):
        self.assertGreater(len(self.api_url),  0, 'Api_url not supplied!')
        self.assertGreater(len(self.options), 0, 'Options not supplied!')
