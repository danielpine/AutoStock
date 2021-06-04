import json
import yaml
from flask.json import JSONEncoder


class AutoJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            return obj.__json__()
        except AttributeError:
            return JSONEncoder.default(self, obj)


def get_mem_size(process):
    mem_info = process.memory_info()
    return mem_info.rss / 1024


def convert_json_from_lists(keys, data):
    container = []
    if data:
        for e in data:
            j = {}
            for k, v in enumerate(e):
                j[keys[k]] = v
            container.append(j)
    return container


def load_json(url):
    with open(url) as f:
        return json.load(f)


def load_yaml(url):
    with open(url) as f:
        return yaml.safe_load(f)


def csv_content_to_json(content):
    rows = content.split("\n")
    titles = rows[0].split(",")
    res = []
    for row in rows[1:]:
        o = {}
        cols = row.split(",")
        for index, col in enumerate(cols):
            o[titles[index]] = col
        res.append(o)
    return res
