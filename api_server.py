from fastapi.exceptions import HTTPException
from fastapi import FastAPI, UploadFile
import numpy as np
import uvicorn

# from mmdet.models.detectors.single_stage import SingleStageDetector
from mmdet.apis import init_detector, inference_detector
from mmcv import imread

ALLOWED_IMAGE_TYPES = ("image/jpeg", "image/png")

app = FastAPI()


@app.post("/get_annotations")
def get_annotations(
        file: UploadFile,
        config_file: str,
        checkpoint_file: str
        ) -> None:

    print(file.filename)
    print(file.content_type)
    print(file.file)

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        msg = "Unallowed file format. Allowed are: 'image/jpeg', 'image/png'"
        raise HTTPException(
            status_code=400,
            detail=msg)

    file_as_bytes = file.file.read()

    ndarray = np.frombuffer(file_as_bytes, dtype=np.uint8)
    image = imread(ndarray)

    model = init_detector(config_file, checkpoint_file, device="cpu")

    # results = inference_detector(model, image)

    # print(results)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
