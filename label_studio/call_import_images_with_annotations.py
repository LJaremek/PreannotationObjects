import requests
import json


def call_import_images_with_annotations(
        project_id: int,
        ) -> None:

    image_url = "http://localhost:8000/import_image_to_ls/"
    annotations_url = "http://localhost:8000/import_annotations_to_image/"

    with open("label_studio/files_with_annotations.json") as file:
        data = json.load(file)

    for record in data:
        image_data = {
            "project_id": project_id,
            "image_path": record["data"]["image"]
        }

        image_response = requests.post(image_url, params=image_data)
        response_dict = json.loads(image_response.text)
        image_id = json.loads(response_dict["text"])["id"]

        annotations = {"annotations": record["annotations"][0]["result"]}

        annotations_data = {
            "project_id": project_id,
            "image_id": image_id,
            "annotations": json.dumps(annotations)
        }

        annotations_response = requests.post(
            annotations_url,
            params=annotations_data
            )

        print("Image status code:", annotations_response.status_code)


if __name__ == "__main__":
    call_import_images_with_annotations(
        16
    )
