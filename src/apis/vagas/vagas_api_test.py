from unittest import TestCase
from unittest.mock import MagicMock, patch, create_autospec
from ...utils.json_utils import JsonUtils as JU

import src.apis.vagas.vagas_api as VA


class VagasApiTests(TestCase):
    def setUp(self):
        self.api_url, self.options = JU.read_json(
            'src/secrets/vagas_api_secret.json').values()

    def tearDown(self):
        return super().tearDown()

    def test_credentials(self):
        self.assertGreater(len(self.api_url),  0, 'Api_url not supplied!')
        self.assertGreater(len(self.options), 0, 'Options not supplied!')

    def test_get_request(self):
        VA.request_data = MagicMock(return_value=3)
        self.assertEqual(3, VA.request_data(self.api_url, self.options))
