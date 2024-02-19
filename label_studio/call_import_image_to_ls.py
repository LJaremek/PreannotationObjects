import requests


data = {
    "project_id": None,
    "image_path": None
    }


def call_import_image_to_ls(
        project_id: int,
        image_path: str
        ) -> None:
    url = "http://localhost:8000/import_annotations_to_image/"

    data = {
        "project_id": project_id,
        "image_path": image_path
        }

    response = requests.post(url, params=data)

    if response.status_code != 200:
        raise Exception(f"Network Error with code: {response.status_code}")

    print("Status code:", response.status_code)


if __name__ == "__main__":
    call_import_image_to_ls(
        data["project_id"],
        data["image_path"]
    )
