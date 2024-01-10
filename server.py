import os

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile
from pathlib import Path
import numpy as np
import uvicorn

from mmdet.models.detectors.single_stage import SingleStageDetector
from mmdet.apis import init_detector, inference_detector
from mmcv import imfrombytes

ALLOWED_IMAGE_TYPES = ("image/jpeg", "image/png")
UPLOAD_FOLDER = Path("/home/nolok/PreannotationObjects/coco/images")

app = FastAPI()


def parse_model_results(
        model: SingleStageDetector,
        model_results: list[list[tuple[float, float, float, float]]]
        ) -> dict[str, list[tuple[float, float, float, float]]]:
    """
    Function parse the model results.

    Input:
     * model: SingleStageDetector
     * model_results: list[list[tuple[float, float, float, float]]] - list with
        lists of detections for the class.

    Output:
     * response: dict - key is a class, value is bbox list
    """

    content: dict[str, list[tuple[float, float, float, float]]] = {}

    for index, class_name in enumerate(model.CLASSES):
        detections = model_results[index]
        content[class_name] = detections

    return content


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
    print(file_path)
    return FileResponse(file_path)


@app.get("/image_to_url/{filename}")
async def image_to_url(filename: str) -> FileResponse:
    """
    Hosting image on URL.
    Input:
     * filename: str - name of the file in path 'UPLOAD_FOLDER'
    """
    path = f"{UPLOAD_FOLDER}/{filename}"

    return FileResponse(path)


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


if __name__ == "__main__":
    uvicorn.run(
        app, host="0.0.0.0",
        port=8000,
        ssl_keyfile=None,
        ssl_certfile=None
        )
