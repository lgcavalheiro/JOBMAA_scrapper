import json

console_caller = '[TOPIC_FORMATTER.PY]'


def read_from_json(file):
    with open(file) as json_file:
        return json.load(json_file)


def write_to_json(data_dict):
    data_dict.sort()
    with open(f"{console_caller}_topics.json", "w") as outfile:
        json.dump(data_dict, outfile, indent=4, ensure_ascii=False)


def main_handler():
    topics = read_from_json('topics.json')
    topics.sort()
    topics = set(topics)
    write_to_json(list(topics))


main_handler()
