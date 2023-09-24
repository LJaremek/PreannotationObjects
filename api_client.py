import requests

url = "http://localhost:8000/get_annotations"

files = {
    "file": (
        "plik.jpg",
        open("./coco/images/000000000139.jpg", "rb"),
        "image/jpeg"
        ),
    "config_file": (
        None,
        "yolov3_mobilenetv2_320_300e_coco.py"
        ),
    "checkpoint_file": (
        None,
        "yolov3_mobilenetv2_320_300e_coco_20210719_215349-d18dff72.pth"
        )
    }

data = {
    "config_file":
        "yolov3_mobilenetv2_320_300e_coco.py",

    "checkpoint_file":
        "yolov3_mobilenetv2_320_300e_coco_20210719_215349-d18dff72.pth"
    }

response = requests.post(url, files=files, params=data)
print(response.status_code)
print(response.text)
