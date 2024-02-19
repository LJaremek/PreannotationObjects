import requests


data = {
    "project_id": None,
    "image_id": None,
    "annotations": None
    }


def call_import_annotations_to_image(
        project_id: int,
        image_id: int,
        annotations: list
        ) -> None:
    url = "http://localhost:8000/import_annotations_to_image/"

    data = {
        "project_id": project_id,
        "image_id": image_id,
        "annotations": annotations
        }

    response = requests.post(url, params=data)

    if response.status_code != 200:
        raise Exception(f"Network Error with code: {response.status_code}")

    print("Status code:", response.status_code)


if __name__ == "__main__":
    call_import_annotations_to_image(
        data["project_id"],
        data["image_id"],
        data["annotations"]
    )
