from enum import Enum
import json

json_path: str = "./coco/panoptic_val2017.json"
with open(json_path) as file:
    json_annotations: dict = json.loads("".join(file.readlines()))

ALL: list = [
    category["id"]
    for category in json_annotations["categories"]
    ]

VEHICLES: list = [
    category["id"]
    for category in json_annotations["categories"]
    if category["supercategory"] == "vehicle"
    ]

CATEGORIES: dict = {
    category["id"]: category["name"]
    for category in json_annotations["categories"]
    }


class Categories(Enum):
    ALL = ALL
    VEHICLES = VEHICLES
