import json
from .json_utils import JsonUtils as JU

console_caller = '[TOPIC_FORMATTER.PY]'


if(__name__ == "__main__"):
    topics = JU.read_json('topics.json')
    topics = sorted(list(set([str(x).lower() for x in topics])))
    JU.write_json(f"{console_caller}_topics.json", topics, "w")
