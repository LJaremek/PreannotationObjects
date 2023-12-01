import requests
import json

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from PIL import Image

url = "http://localhost:8000/get_annotations_from_file"

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


if __name__ == "__main__":
    response = requests.post(url, files=file, params=data)

    predictions = []
    if response.status_code == 200:
        response_dict = json.loads(response.text)
        detections = response_dict["detections"]
        classes = response_dict["classes"]

        for class_idx, class_result in enumerate(detections):
            for detection in class_result:
                score = detection.pop(-1)
                if score > 0.3:
                    print(score, detection)
                    print(classes[class_idx], class_idx)
                    predictions.append(detection)

    draw_rectangles("./coco/images/000000000139.jpg", predictions)

    print(predictions)
