from random import randint

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from PIL import Image

from constans import VEHICLES, json_annotations


def get_files_annotations(
        json_annotations: dict,
        annotation_classes: tuple[int]
        ) -> dict[str, list[dict]]:
    """
    Input:
        * json_annotations: dict - panoptic_val2017.json as dict
        * annotation_classes: tuple[int] - target annotation classes ids

    Output:
        * annotations: list[dict] - list of dicts with annotations data
    """

    annotations: dict[str, list[list[int, int, int, int]]] = {}

    for file_json in json_annotations["annotations"]:

        segments_json = [
            segment
            for segment in file_json["segments_info"]
            if segment["category_id"] in annotation_classes
            ]

        if len(segments_json) != 0:
            file_name = file_json["file_name"].replace("png", "jpg")
            annotations[file_name] = segments_json

    return annotations


def draw_rectangles(
        file_path: str,
        coco_rects: list,
        file_name: str
        ) -> None:

    img = Image.open(file_path)

    # wyświetlenie obrazka
    plt.gca().clear()
    plt.imshow(img)

    # dodanie prostokątów coco na obrazku
    for rect in coco_rects:
        bbox_left, bbox_top, bbox_width, bbox_height = rect["bbox"]

        rect = patches.Rectangle(
            (bbox_left, bbox_top),
            bbox_width, bbox_height,
            linewidth=1, edgecolor="r", facecolor="none"
            )

        plt.gca().add_patch(rect)
    plt.show()
    plt.savefig(f"matplotlib_{file_name}.png")


def prepare_two_images(
        file_path_1: str,
        file_path_2: str,
        rectangles_1: list[dict],
        rectangles_2: list[dict],
        titles: list[str],
        title: str
        ) -> None:

    img_1 = Image.open(file_path_1)
    img_2 = Image.open(file_path_2)

    _, axs = plt.subplots(1, 2, figsize=(10, 5))

    # Wyświetlenie obrazków na odpowiadających osiach
    axs[0].imshow(img_1)
    for rectangle in rectangles_1:
        bbox_left, bbox_top, bbox_width, bbox_height = rectangle["bbox"]
        rect = patches.Rectangle(
            (bbox_left, bbox_top), bbox_width, bbox_height,
            linewidth=1, edgecolor="r", facecolor="none"
        )
        axs[0].add_patch(rect)
    axs[0].set_title(titles[0])

    axs[1].imshow(img_2)
    for rectangle in rectangles_2:
        bbox_left, bbox_top, bbox_width, bbox_height = rectangle["bbox"]
        rect = patches.Rectangle(
            (bbox_left, bbox_top), bbox_width, bbox_height,
            linewidth=1, edgecolor="r", facecolor="none"
        )
        axs[1].add_patch(rect)
    axs[1].set_title(titles[1])

    plt.tight_layout()  # Dostosowanie układu

    plt.savefig(f"{title}.png")


def calculate_iou(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    # Współrzędne górnego lewego narożnika
    # i dolnego prawego narożnika prostokąta 1
    x1_min, y1_min = x1, y1
    x1_max, y1_max = x1 + w1, y1 + h1

    # Współrzędne górnego lewego narożnika
    # i dolnego prawego narożnika prostokąta 2
    x2_min, y2_min = x2, y2
    x2_max, y2_max = x2 + w2, y2 + h2

    # Wyznaczenie wspólnego obszaru
    x_overlap = max(0, min(x1_max, x2_max) - max(x1_min, x2_min))
    y_overlap = max(0, min(y1_max, y2_max) - max(y1_min, y2_min))

    # Obliczenie obszaru przecięcia i obszaru sumy prostokątów
    intersection_area = x_overlap * y_overlap
    box1_area = w1 * h1
    box2_area = w2 * h2
    union_area = box1_area + box2_area - intersection_area

    # Obliczenie indeksu przekroju obiektów
    iou = intersection_area / union_area if union_area > 0 else 0
    return iou


def calc_error(
        x_min: int,
        y_min: int,
        width: int,
        height: int,
        percentage: int
        ) -> list[float]:

    x_error = (percentage/100)*width
    y_error = (percentage/100)*height

    random = randint(1, 4)
    if random == 1:
        width += x_error
    elif random == 2:
        width -= x_error
    elif random == 3:
        x_min += x_error
    else:
        x_min -= x_error

    random = randint(1, 4)
    if random == 1:
        height += y_error
    elif random == 2:
        height -= y_error
    elif random == 3:
        y_min += y_error
    else:
        y_min -= y_error

    return x_min, y_min, width, height


if __name__ == "__main__":
    files_annotations = get_files_annotations(json_annotations, VEHICLES)
    example_files = [
        "000000001532.jpg",
        "000000084170.jpg",
        "000000044652.jpg"
        ]

    percentages: dict[int, list] = {i: [] for i in range(0, 105, 5)}

    for percentage in percentages:
        for file_name in files_annotations:
            # draw_rectangles(
            #     f"./coco/images/{file_name}",
            #     files_annotations[file_name],
            #     f"1_{file_name}"
            # )

            new_annotations = []
            for annotation in files_annotations[file_name]:
                x_min, y_min, width, height = annotation["bbox"]

                x_min, y_min, width, height = calc_error(
                    x_min, y_min, width, height, percentage
                    )

                percentages[percentage].append(calculate_iou(
                        annotation["bbox"],
                        (x_min, y_min, width, height)
                        )
                    )

                new_annotations.append(
                  {"bbox": [x_min, y_min, width, height]}
                )

            if file_name in example_files and percentage in (5, 10, 15, 20):
                prepare_two_images(
                    f"./coco/images/{file_name}",
                    f"./coco/images/{file_name}",
                    files_annotations[file_name],
                    new_annotations,
                    ("0 percentages", f"{percentage} percentages"),
                    f"./images/iou/{file_name.split('.')[0]}_{percentage}"
                    )

            # draw_rectangles(
            #     f"./coco/images/{file_name}",
            #     files_annotations[file_name],
            #     f"2_{file_name}"
            #     )
        percentages[percentage] = (
            sum(percentages[percentage])/len(percentages[percentage])
        )

    plt.figure(figsize=(8, 6))
    plt.plot(percentages.keys(), percentages.values(), "-o")

    for i, (percentage, iou) in enumerate(percentages.items()):
        plt.text(
            percentage+2, iou+.01, f"{percentage}%",
            ha='center', va='bottom'
            )
        if i == 5:
            break

    plt.xlabel("Annotation offset percentage")
    plt.ylabel("IoU")
    plt.yticks([i/10 for i in range(0, 11)])
    plt.ylim(-0.05, 1.1)
    plt.title("Dependence of IoU on annotation offset percentage")
    plt.savefig("./images/iou/iou_chart.png")
