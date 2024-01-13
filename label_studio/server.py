from random import randint
import requests
import json
import os

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile
from PIL import Image
import numpy as np
import uvicorn

from mmdet.models.detectors.single_stage import SingleStageDetector
from mmdet.apis import init_detector, inference_detector
from mmcv import imfrombytes

LOCAL_SERVER_PATH = os.getenv("LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT")
TOKEN = os.getenv("LABEL_STUDIO_TOKEN")

ALLOWED_IMAGE_TYPES = ("image/jpeg", "image/png")
ALLOWED_IMAGES_EXTS = ("png", "jpg", "jpeg")

app = FastAPI()


def rand_hex_color() -> str:
    return "".join([f"{hex(randint(1, 255)):04}"[2:] for _ in range(3)])


def parse_model_results(
        model: SingleStageDetector,
        model_results: list[np.array],
        image_width: int,
        image_height: int,
        min_model_score: float = 0.3
        ) -> dict[str, list[tuple[float, float, float, float]]]:
    """
    Function parse the model results for the Label Studio.

    Input:
     * model: SingleStageDetector
     * model_results: list[np.array] - list with model detections
     * image_width: int - image width
     * image_height: int - image height
     * min_model_score: float [default 0.3] - min model score for annotations

    Output:
     * annotations: dict - prepared model annotations for Label Studio
    """

    annotations = [
        {
            "result": []
        }
    ]

    model_results = [arr.tolist() for arr in model_results]

    for index, class_name in enumerate(model.CLASSES):
        detections = model_results[index]

        for detection in detections:
            x1, y1, x2, y2, score = detection

            if score < min_model_score:
                continue

            result_record = {
                "value": {
                    "x": x1*100/image_width,
                    "y": y1*100/image_height,
                    "width": (x2-x1)*100/image_width,
                    "height": (y2-y1)*100/image_height,
                    "rectanglelabels": [
                        class_name
                    ]
                },
                "from_name": "label",
                "to_name": "image",
                "type": "rectanglelabels"
            }
            annotations[0]["result"].append(result_record)

    return annotations


def prepare_label_config(model_classes: list[str]) -> str:
    class_records = ""
    for the_class in model_classes:
        new_line = f"""\n<Label value="{the_class}" """
        new_line += f"""background="#{rand_hex_color()}"/>"""

        class_records += new_line

    return f"""
        <View>
            <Image name="image" value="$image"/>
            <RectangleLabels name="label" toName="image">
                {class_records}
            </RectangleLabels>
        </View>
        """


@app.post("/get_annotations_from_file")
def get_annotations_from_file(
        file: UploadFile,
        config_file: str,
        checkpoint_file: str
        ) -> JSONResponse:
    """
    Endpoint generates annotations for the given file.

    Input:
     * file: dict[str, tuple[str, io._io.TextIOWrapper, str]] - dict like that:
        {
        "file": (
            <file_path>,
            <file handler>,
            <file type> 'image/jpeg' or 'image/png'
            )
        }
     * config_file: str - model config file .py
     * checkpoint_file: str - model checkpoint file .pth

    Output:
     * response: dict - key is a class, value is bbox list
    """

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        msg = "Unallowed file format. Allowed are: 'image/jpeg', 'image/png'"
        raise HTTPException(
            status_code=400,
            detail=msg
            )

    file_as_bytes = file.file.read()

    image = imfrombytes(file_as_bytes)

    model = init_detector(config_file, checkpoint_file, device="cpu")

    results: list[np.array] = inference_detector(model, image)

    model.show_result(image, results, out_file='resultLJ.jpg')

    results_as_list = [arr.tolist() for arr in results]

    return JSONResponse(content=parse_model_results(model, results_as_list))


@app.get("/file_url")
async def file_url(file_path: str) -> FileResponse:
    """
    Endpoint for generating URL for the file with the given path.
    """
    print(file_path)
    return FileResponse(file_path)


@app.post("/get_folder_annotations")
def get_folder_annotations(
        folder_path: str,
        config_file: str,
        checkpoint_file: str
        ) -> JSONResponse:
    """
    Endpoint generates annotations for the given folder with files.

    Input:
     * folder_path: str - folder path with images
     * config_file: str - model config file .py
     * checkpoint_file: str - model checkpoint file .pth

    Output:
     * response: dict - key is a file name, value is a dit:
        key is class, value is bbox list
    """
    results = {}

    files = os.listdir(folder_path)
    if len(files) == 0:
        return JSONResponse(
            content={
                "files": results
                }
            )

    symbol = "/"
    if "\\" in folder_path:
        symbol = "\\"

    model = init_detector(config_file, checkpoint_file, device="cpu")

    content: dict[str, dict] = {}
    for file in files:
        file_path = folder_path + symbol + file
        model_results: list[np.array] = inference_detector(model, file_path)
        results_as_list = [arr.tolist() for arr in model_results]
        content[file] = parse_model_results(model, results_as_list)

    return JSONResponse(content=content)


@app.post("/prepare_ls_json")
def prepare_ls_json(
        data_folder: str,
        config_file: str,
        checkpoint_file: str
        ) -> JSONResponse:
    """
    Endpoint prepare json file content for the Label Studi with the images from
    the given server.

    Input:
     * data_folder: str - data folder name.
        It has to be in local server storage!
     * config_file: str - model config file .py
     * checkpoint_file: str - model checkpoint file .pth

    Output:
     * json_content: str - json content for Label Studio.
    """

    files = os.listdir(LOCAL_SERVER_PATH + "/" + data_folder)

    model = init_detector(config_file, checkpoint_file, device="cpu")

    label_studio_json = []
    for file in files:
        if file.split(".")[-1] not in ALLOWED_IMAGES_EXTS:
            continue

        file_path = LOCAL_SERVER_PATH + "/" + data_folder + "/" + file

        width, height = Image.open(file_path).size

        model_results: list[np.array] = inference_detector(model, file_path)
        annotations = parse_model_results(
            model, model_results, width, height
            )

        label_studio_json.append(
            {
                "data": {
                    "image": f"/data/local-files?d={data_folder}/{file}"
                },
                "annotations": annotations,
                "predictions": []
            }
        )

    return JSONResponse(
        content=json.dumps(label_studio_json).replace("'", '"')
        )


@app.post("/create_ls_project")
def create_ls_project(
        config_file: str,
        checkpoint_file: str,
        project_title: str = "My New Project",
        project_description: str = None
        ) -> JSONResponse:
    """
    Endpoint create a new project in Label Studio with the given title and desc
    This endpoint set label config (label names and colors) based on the model.

    Input:
     * config_file: str - model config file .py
     * checkpoint_file: str - model checkpoint file .pth
     * project_title: str - project title
     * project_description: str - project description

    Output:
     * json_content: str - json content with status code and response text
    """

    model = init_detector(config_file, checkpoint_file, device="cpu")

    label_config = prepare_label_config(model.CLASSES)

    task_data = {}
    task_data["label_config"] = label_config
    task_data["title"] = project_title

    if project_description is not None:
        task_data["description"] = project_description

    response = requests.post(
        "http://localhost:8080/api/projects/",
        headers={"Authorization": f"Token {TOKEN}"},
        json=task_data,
        verify=False
    )

    return JSONResponse(
        content=json.dumps(
            {
                "text": response.text,
                "status_code": response.status_code
            }
            )
        )


@app.post("/update_ls_project")
def update_ls_project(
        config_file: str,
        checkpoint_file: str,
        project_id: int
        ) -> JSONResponse:
    """
    Endpoint update the project in Label Studio with the given project id.
    This endpoint set label config (label names and colors) based on the model.

    Input:
     * config_file: str - model config file .py
     * checkpoint_file: str - model checkpoint file .pth
     * project_id: int - project id

    Output:
     * json_content: str - json content with status code and response text
    """

    model = init_detector(config_file, checkpoint_file, device="cpu")

    label_config = prepare_label_config(model.CLASSES)

    task_data = {}
    task_data["label_config"] = label_config

    response = requests.patch(
        f"http://localhost:8080/api/projects/{project_id}",
        headers={"Authorization": f"Token {TOKEN}"},
        json=task_data,
        verify=False
    )

    return JSONResponse(
        content=json.dumps(
            {
                "text": response.text,
                "status_code": response.status_code
            }
            )
        )


if __name__ == "__main__":
    uvicorn.run(
        app, host="0.0.0.0",
        port=8000,
        ssl_keyfile=None,
        ssl_certfile=None
        )
