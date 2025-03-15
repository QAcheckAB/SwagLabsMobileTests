# -*- coding: utf-8 -*-
import json
import os
from typing import Dict, Any


def load_config_from_json(file_name: str) -> Dict[str, Any]:
    """
    Loads data from json file
    :param file_name: json file name
    :return: json data in dictionary format
    """
    config = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "configuration",
        file_name,
    )
    with open(config, "r") as f:
        config_file = json.load(f)
    return config_file
