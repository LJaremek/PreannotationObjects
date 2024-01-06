import matplotlib.patches as patches
import matplotlib.pyplot as plt
from PIL import Image

from tools.constans import VEHICLES, json_annotations
from tools.annotations import get_files_annotations
from tools.rectangles import add_coco_rects_to_plt
from tools.rectangles import move_rect_by_percentage
from tools.iou_math import jaccard_index


def draw_coco_rectangles(
        file_path: str,
        coco_rects: list,
        file_name: str
        ) -> None:

    img = Image.open(file_path)

    # Displaying the image
    plt.gca().clear()
    plt.imshow(img)

    add_coco_rects_to_plt(coco_rects)

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

    # Displaying images on the corresponding axes
    axs[0].imshow(img_1)
    for rectangle in rectangles_1:
        bbox_left, bbox_top, bbox_width, bbox_height = rectangle
        rect = patches.Rectangle(
            (bbox_left, bbox_top), bbox_width, bbox_height,
            linewidth=1, edgecolor="r", facecolor="none"
        )
        axs[0].add_patch(rect)
    axs[0].set_title(titles[0])

    axs[1].imshow(img_2)
    for rectangle in rectangles_2:
        bbox_left, bbox_top, bbox_width, bbox_height = rectangle
        rect = patches.Rectangle(
            (bbox_left, bbox_top), bbox_width, bbox_height,
            linewidth=1, edgecolor="r", facecolor="none"
        )
        axs[1].add_patch(rect)
    axs[1].set_title(titles[1])

    plt.tight_layout()  # Customize the layout

    plt.savefig(f"{title}.png")


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
            # draw_coco_rectangles(
            #     f"./coco/images/{file_name}",
            #     files_annotations[file_name],
            #     f"1_{file_name}"
            # )

            new_annotations = []
            for annotation in files_annotations[file_name]:
                x_min, y_min, width, height = annotation

                x_min, y_min, width, height = move_rect_by_percentage(
                    x_min, y_min, width, height, percentage
                    )

                percentages[percentage].append(jaccard_index(
                        annotation,
                        (x_min, y_min, width, height)
                        )
                    )

                new_annotations.append(
                  [x_min, y_min, width, height]
                )

            if file_name in example_files and percentage in (5, 10, 15, 20):
                prepare_two_images(
                    f"./coco/images/{file_name}",
                    f"./coco/images/{file_name}",
                    files_annotations[file_name],
                    new_annotations,
                    ("0 percentages", f"{percentage} percentages"),
                    f"./iou/images/{file_name.split('.')[0]}_{percentage}"
                    )

            # draw_coco_rectangles(
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
    plt.savefig("./iou/images/iou_chart.png")
