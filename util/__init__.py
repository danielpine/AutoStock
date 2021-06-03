# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Pine
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json
import yaml


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
