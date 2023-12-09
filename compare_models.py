from time import time
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

        start_time = time()
        model = init_detector(config_file, checkpoint_file, device="cpu")
        model_init_time = time() - start_time

        model_ji: list[float] = []
        start_time = time()
        incorrect_images = 0
        for file_name in files:

            file_path = f"./coco/images/{file_name}"

            coco_rects = get_coco_rects(files[file_name])
            mmdet_rects = get_mmdet_rects(file_path, model, False)

            _, _, _, ji_avg = filter_rectangles(
                coco_rects, mmdet_rects, MIN_JI_INDEX
            )
            if ji_avg == 0:
                incorrect_images += 1

            model_ji.append(ji_avg)
        labeling_data_time = time() - start_time

        print(">>>>> MODEL STATS")
        print("model name:", model_name)
        print("model ji:", sum(model_ji)/len(model_ji))
        print("model load time:", model_init_time)
        print("model label time:", labeling_data_time)
        print("bad:", incorrect_images)
        print("<<<<<")
