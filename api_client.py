import requests
import json

url = "http://localhost:8000/get_annotations"

file = {
    "file": (
        "plik.jpg",
        open("./coco/images/000000000139.jpg", "rb"),
        "image/jpeg"
        )
    }

data = {
    "config_file":
        "yolov3_mobilenetv2_320_300e_coco.py",

    "checkpoint_file":
        "yolov3_mobilenetv2_320_300e_coco_20210719_215349-d18dff72.pth"
    }

response = requests.post(url, files=file, params=data)

if response.status_code == 200:
    detections = json.loads(response.text)["detections"]

    for class_idx, class_result in enumerate(detections):
        for detection in class_result:
            score = detection.pop(-1)
            print(class_idx, score, detection)
