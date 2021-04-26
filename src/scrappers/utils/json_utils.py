import json


class JsonUtils:
    @staticmethod
    def read_json(file):
        with open(file, 'r') as json_file:
            return json.load(json_file)

    @staticmethod
    def write_json(file, data, mode):
        with open(file, mode=mode) as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
            json_file.close()
