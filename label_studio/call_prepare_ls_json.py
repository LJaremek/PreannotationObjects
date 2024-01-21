import requests
import json


data = {
    "config_file":
    "models/yolov3_mobilenetv2_320_300e_coco.py",

    "checkpoint_file":
    "models/yolov3_mobilenetv2_320_300e_coco_20210719_215349-d18dff72.pth",

    "data_folder": "test_images"
    }


def call_prepare_ls_json() -> None:
    url = "http://localhost:8000/prepare_ls_json/"

    response = requests.post(url, params=data)

    if response.status_code != 200:
        raise Exception(f"Network Error with code: {response.status_code}")

    response_dict = json.loads(response.text)

    result_json_path = "label_studio/files_with_annotations.json"

    with open(
            result_json_path,
            "w",
            -1,
            "utf-8"
            ) as file:
        print(response_dict, file=file)
        print("File location:", result_json_path)


if __name__ == "__main__":
    call_prepare_ls_json()
