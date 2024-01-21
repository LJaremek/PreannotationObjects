def get_files_annotations(
        json_annotations: dict,
        annotation_classes: tuple[int],
        min_segments: int = 2
        ) -> dict[str, list[tuple[int, int, int, int]]]:
    """
    Input:
        * json_annotations: dict - panoptic_val2017.json as dict
        * annotation_classes: tuple[int] - target annotation classes ids
        * min_segments: int (default=0) - minimum segments in file to accept

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

        if len(segments_json) > min_segments:
            file_name = file_json["file_name"].replace("png", "jpg")
            segments = [segment["bbox"] for segment in segments_json]

            annotations[file_name] = segments

    return annotations
