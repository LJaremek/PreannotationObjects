from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile
from pathlib import Path
import numpy as np
import uvicorn

from mmdet.apis import init_detector, inference_detector
from mmcv import imfrombytes

ALLOWED_IMAGE_TYPES = ("image/jpeg", "image/png")
UPLOAD_FOLDER = Path("/home/nolok/PreannotationObjects/coco/images")

app = FastAPI()


@app.post("/get_annotations_from_file")
def get_annotations_from_file(
        file: UploadFile,
        config_file: str,
        checkpoint_file: str
        ) -> JSONResponse:

    print(file.filename)
    print(file.content_type)
    print(file.file)

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        msg = "Unallowed file format. Allowed are: 'image/jpeg', 'image/png'"
        raise HTTPException(
            status_code=400,
            detail=msg)

    file_as_bytes = file.file.read()

    image = imfrombytes(file_as_bytes)

    model = init_detector(config_file, checkpoint_file, device="cpu")

    results: list[np.array] = inference_detector(model, image)

    results_as_list = [arr.tolist() for arr in results]

    return JSONResponse(content={
        "detections": results_as_list,
        "classes": model.CLASSES})


@app.post("/get_annotations")
def get_annotations_from_dir(
        file: UploadFile,
        config_file: str,
        checkpoint_file: str
        ) -> JSONResponse:

    print(file.filename)
    print(file.content_type)
    print(file.file)

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        msg = "Unallowed file format. Allowed are: 'image/jpeg', 'image/png'"
        raise HTTPException(
            status_code=400,
            detail=msg)

    file_as_bytes = file.file.read()

    image = imfrombytes(file_as_bytes)

    model = init_detector(config_file, checkpoint_file, device="cpu")

    results: list[np.array] = inference_detector(model, image)

    results_as_list = [arr.tolist() for arr in results]

    return JSONResponse(content={
        "detections": results_as_list,
        "classes": model.CLASSES})


@app.get("/file_url/{file_path}")
async def read_file(file_path: str) -> FileResponse:
    return FileResponse(file_path, media_type="image/png")


@app.get("/image_to_url/{filename}")
async def get_image(filename: str):
    path = f"{UPLOAD_FOLDER}/{filename}"

    return FileResponse(path)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
