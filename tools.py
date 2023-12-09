from mmdet.models.detectors.single_stage import SingleStageDetector
from mmdet.apis import inference_detector
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from PIL import Image


def get_mmdet_rects(
        file_path: str,
        model: SingleStageDetector,
        printing: bool = True,
        min_score: float = 0.6,
        ) -> list[list[int, int, int, int]]:

    rectangles = []
    scores = []

    results = inference_detector(model, file_path)

    for class_idx in range(len(results)):
        class_results = results[class_idx]
        for detection in class_results:
            score = detection[-1]
            scores.append(score)
            if score > min_score:
                rect = [int(el) for el in detection[:-1]]

                bbox_left, bbox_top, bbox_right, bbox_bottom = rect
                bbox_width = bbox_right - bbox_left
                bbox_height = bbox_bottom - bbox_top

                new_rect = (bbox_left, bbox_top, bbox_width, bbox_height)
                rectangles.append(new_rect)

    if printing:
        print("--- mmdet score ---")
        print("min\tmax\tavg")
        print(
            round(min(scores), 3),
            round(max(scores), 3),
            round(sum(scores)/len(scores), 3),
            sep="\t"
            )
        print("--- < < --- > > ---")

    return rectangles


def get_coco_rects(
        file_segments: list[list[int, int, int, int]]
        ) -> list[list[int, int, int, int]]:
    """
    TODO: Do we need the function? For code readability?
    """

    rects: list = []

    for rect in file_segments:
        rects.append(rect)

    return rects


def add_coco_rects_to_plt(coco_rects: list) -> None:
    for rect in coco_rects:
        bbox_left, bbox_top, bbox_width, bbox_height = rect

        rect = patches.Rectangle(
            (bbox_left, bbox_top),
            bbox_width, bbox_height,
            linewidth=1, edgecolor="r", facecolor="none"
            )

        plt.gca().add_patch(rect)


def add_mmdet_rects_to_plt(mmdet_rects: list) -> None:
    for rect in mmdet_rects:
        bbox_left, bbox_top, bbox_width, bbox_height = rect

        rect = patches.Rectangle(
            (bbox_left, bbox_top),
            bbox_width, bbox_height,
            linewidth=1, edgecolor="b", facecolor="none"
            )

        plt.gca().add_patch(rect)


def draw_rectangles(
        file_path: str,
        coco_rects: list,
        mmdet_rects: list
        ) -> None:

    img = Image.open(file_path)
    plt.imshow(img)

    add_coco_rects_to_plt(coco_rects)
    add_mmdet_rects_to_plt(mmdet_rects)

    plt.show()


def jaccard_index(
        rect1: tuple[int, int, int, int],
        rect2: tuple[int, int, int, int]
        ) -> float:
    """
    Calc Jaccard Index.
    Jaccard similarity coefficient is a measure of similarity between two sets.
    It takes values from the range [0, 1],
    where 0 means no similarity and1 means sets are identical.

    Input:
        * rect1: tuple[int, int, int, int] - (x, y, widht, height)
        * rect2: tuple[int, int, int, int] - (x, y, widht, height)
    Output:
        * index: float - value between <0, 1>
    """
    # Calculating the coordinates of the resulting rectangle
    x_left = max(rect1[0], rect2[0])
    y_top = max(rect1[1], rect2[1])
    x_right = min(rect1[0] + rect1[2], rect2[0] + rect2[2])
    y_bottom = min(rect1[1] + rect1[3], rect2[1] + rect2[3])

    # Calculating the common area of the area A ∩ B
    intersection_area = max(0, x_right - x_left) * max(0, y_bottom - y_top)

    # Calculating the area of the sum of areas A and B
    union_area = rect1[2] * rect1[3] + rect2[2] * rect2[3] - intersection_area

    # Calculation of the Jaccard index
    jaccard_index = intersection_area / union_area

    return jaccard_index


def get_files_annotations(
        json_annotations: dict,
        annotation_classes: tuple[int]
        ) -> dict[str, list[tuple[int, int, int, int]]]:

    """
    Input:
        * json_annotations: dict - panoptic_val2017.json as dict
        * annotation_classes: tuple[int] - target annotation classes ids

    Output:
        * annotations: dict[str, list[tuple[int, int, int, int]]] - dict where
            key is a file name and values are rects with annotations
    """

    annotations: dict[str, list[list[int, int, int, int]]] = {}

    for file_json in json_annotations["annotations"]:
        segments_json = [
            segment
            for segment in file_json["segments_info"]
            if segment["category_id"] in annotation_classes
            ]

        if len(segments_json) > 2:
            file_name = file_json["file_name"].replace("png", "jpg")
            segments = [segment["bbox"] for segment in segments_json]

            annotations[file_name] = segments

    return annotations


def filter_rectangles(
        rects1: list[tuple[int, int, int, int]],
        rects2: list[tuple[int, int, int, int]],
        min_jaccard_index: float = 0.7
        ) -> tuple[list[tuple], list[tuple], float, float]:
    """
    Function filtering the doubled rects given from the the lists.
    Example:
        If there are two rectangles in rects1 (A, B) and one rectangle in
        rects2 (C) and jaccard_index(A, C) = 0.8 and jaccard_index(B, C) = 0.7,
        the result of filtering is:
         * rects1: A
         * rects2: C
        Because we consider A and B to be duplicates, but B has less surface
        coverage with C than A.

    Input:
     * rects1: list[tuple[int, int, int, int]] - the first list of the rects
     * rects2: list[tuple[int, int, int, int]] - the second list of the rects
     * min_jaccard_index: float (default=0.7) - the min value of jaccard index
        for filtering only acceptable rectangles.

    Output:
     * filtered_rects1: list[tuple[int, int, int, int]]
     * filtered_rects2: list[tuple[int, int, int, int]]
     * float - avg index for each rectangle
     * float - avg index for each rectangle where IOU > min_jaccard_index
    """
    ji_all = []
    ji_ok = []

    pairs: dict = {}
    for r1 in rects1:
        for r2 in rects2:
            ji = jaccard_index(r1, r2)
            ji_all.append(ji)
            if ji >= min_jaccard_index:
                if (
                    (tuple(r1), tuple(r2)) not in pairs
                    or (tuple(r2), tuple(r1)) not in pairs
                ):
                    ji_ok.append(ji)
                    pairs[(tuple(r1), tuple(r2))] = ji

    sorted_pairs = sorted(pairs, key=pairs.get)
    if len(sorted_pairs) == 0:
        return [], [], 0, 0

    list1 = []
    list2 = []
    for pair in sorted_pairs:
        list1.append(pair[0])
        list2.append(pair[1])

    return list1, list2, sum(ji_all)/len(ji_all), sum(ji_ok)/len(ji_ok)
