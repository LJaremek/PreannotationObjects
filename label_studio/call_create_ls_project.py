import requests


data = {
    "config_file":
    "models/yolov3_mobilenetv2_320_300e_coco.py",

    "checkpoint_file":
    "models/yolov3_mobilenetv2_320_300e_coco_20210719_215349-d18dff72.pth",

    "project_description": "This is test call project"
    }


def call_create_ls_project() -> None:
    url = "http://localhost:8000/create_ls_project/"

    response = requests.post(url, params=data)

    if response.status_code != 200:
        raise Exception(f"Network Error with code: {response.status_code}")

    print("Status code:", response.status_code)


if __name__ == "__main__":
    call_create_ls_project()
