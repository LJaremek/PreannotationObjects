import requests
import json

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from PIL import Image

data1 = {
    "config_file":
    "./models/yolov3_mobilenetv2_320_300e_coco.py",

    "checkpoint_file":
    "./models/yolov3_mobilenetv2_320_300e_coco_20210719_215349-d18dff72.pth"
    }

data2 = {
    "config_file":
    "./models/yolov3_mobilenetv2_320_300e_coco.py",

    "checkpoint_file":
    "./models/yolov3_mobilenetv2_320_300e_coco_20210719_215349-d18dff72.pth",

    "folder_path": "/home/nolok/PreannotationObjects/coco/small_images/"
    }


def draw_rectangles(
        file_path: str,
        rects: list
        ) -> None:

    img = Image.open(file_path)
    plt.imshow(img)

    for rect in rects:
        bbox_left, bbox_top, bbox_right, bbox_bottom = rect
        bbox_width = bbox_right - bbox_left
        bbox_height = bbox_bottom - bbox_top

        rect = patches.Rectangle(
            (bbox_left, bbox_top),
            bbox_width, bbox_height,
            linewidth=1, edgecolor="b", facecolor="none"
            )

        plt.gca().add_patch(rect)

    plt.show()
    plt.savefig("plik.jpg")


def try_get_annotations_from_file() -> None:
    url = "http://localhost:8000/get_annotations_from_file"

    image_path = "./coco/images/000000000139.jpg"
    file = {
        "file": (
            "plik.jpg",
            open(image_path, "rb"),
            "image/jpeg"
            )
        }

    response = requests.post(url, files=file, params=data1)

    if response.status_code != 200:
        raise Exception(f"Network Error with code: {response.status_code}")

    response_dict = json.loads(response.text)

    predictions = []
    for class_name in response_dict:
        for detection in response_dict[class_name]:
            score = detection.pop(-1)
            if score > 0.3:
                print(f"Class '{class_name}' with score", end=" ")
                print(f"{round(score, 2)} and bbox = {detection}")
                print()

                predictions.append(detection)

    draw_rectangles(image_path, predictions)


def try_file_url() -> None:
    url = "http://localhost:8000/file_url"

    data = {
        "file_path": "./coco/images/000000000139.jpg"
    }

    response = requests.get(url, params=data)

    print(response.text)


def try_image_to_url() -> None:
    url = "http://localhost:8000/image_to_url/000000000139.jpg"
    response = requests.get(url)
    print(response.text)


def try_get_folder_annotations() -> None:
    url = "http://localhost:8000/get_folder_annotations/"

    response = requests.post(url, params=data2)

    if response.status_code != 200:
        raise Exception(f"Network Error with code: {response.status_code}")

    response_dict = json.loads(response.text)

    predictions = []
    for file_name in response_dict:
        print("File:", file_name)
        for class_name in response_dict[file_name]:
            for detection in response_dict[file_name][class_name]:
                score = detection.pop(-1)
                if score > 0.3:
                    print(f"\tClass '{class_name}' with score", end=" ")
                    print(f"{round(score, 2)} and bbox = {detection}")
                    print()

                    predictions.append(detection)


if __name__ == "__main__":
    # try_get_annotations_from_file()

    # try_file_url()

    # try_image_to_url()

    try_get_folder_annotations()
