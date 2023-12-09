import json

from mmdet.apis import init_detector

from constans import Categories, json_annotations
from tools import get_coco_rects, get_mmdet_rects
from tools import get_files_annotations
from tools import filter_rectangles


MODELS_JSON = "./models/experiment_models.json"
MIN_JI_INDEX = 0.7  # Based on ./iou/README.md


if __name__ == "__main__":
    with open(MODELS_JSON, "r", -1, "utf-8") as file:
        models: dict[str, dict[str, str]] = json.load(file)

    files = get_files_annotations(json_annotations, Categories.VEHICLES.value)
    for model_name, model_files in models.items():
        checkpoint_file = f"./models/{model_files['checkpoint_file']}"
        config_file = f"./models/{model_files['config_file']}"

        model = init_detector(config_file, checkpoint_file, device="cpu")

        model_ji: list[float] = []
        for file_name in files:

            file_path = f"./coco/images/{file_name}"

            coco_rects = get_coco_rects(files[file_name])
            mmdet_rects = get_mmdet_rects(file_path, model, False)

            _, _, _, ji_avg = filter_rectangles(
                coco_rects, mmdet_rects, MIN_JI_INDEX
            )

            model_ji.append(ji_avg)

        print("!!!!!")
        print(model_name, sum(model_ji)/len(model_ji))
        print("!!!!!")
