import json
import pandas as pd
import numpy as np

def json2dict(PATH):
    with open(PATH, "r") as f:
        result = json.load(f)
    return result



