import requests


data = {
    "config_file":
    "models/yolov3_mobilenetv2_320_300e_coco.py",

    "checkpoint_file":
    "models/yolov3_mobilenetv2_320_300e_coco_20210719_215349-d18dff72.pth",

    "project_id": 8
    }


def call_update_ls_project() -> None:
    url = "http://localhost:8000/update_ls_project/"

    response = requests.post(url, params=data)

    if response.status_code != 200:
        raise Exception(f"Network Error with code: {response.status_code}")

    print("Status code:", response.status_code)


if __name__ == "__main__":
    call_update_ls_project()
