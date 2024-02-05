import json

from mmdet.apis import init_detector, inference_detector
import mmcv
import cv2

IMAGE_PATH = "label_studio/test_images/000000001532.jpg"
MIN_MODEL_SCORE = 0.3


def check_differences(models_json: str) -> None:
    with open(models_json, "r") as file:
        models = json.loads("".join(file.readlines()))

    for model_name in models:
        checkpoint = "models/" + models[model_name]["checkpoint_file"]
        config = "models/" + models[model_name]["config_file"]

        model = init_detector(config, checkpoint, device="cpu")

        model_results = inference_detector(
            model,
            IMAGE_PATH
            )

        img = mmcv.imread(IMAGE_PATH)

        for _, bbox in enumerate(model_results):
            for box in bbox:
                if box[-1] > MIN_MODEL_SCORE:
                    cv2.rectangle(
                        img,
                        (int(box[0]), int(box[1])),
                        (int(box[2]), int(box[3])),
                        color=(0, 255, 0),
                        thickness=2,
                    )

        output_path = f"models/{model_name}_{IMAGE_PATH.split('/')[-1]}"
        mmcv.imwrite(img, output_path)


if __name__ == "__main__":
    models_json = "models/experiment_models.json"
    check_differences(models_json)
