from ..tools.annotations import get_files_annotations


def test_get_files_annotations_1() -> None:
    test_data = {
        "annotations": [
            {
                "file_name": "test1.png",
                "segments_info": [
                    {
                        "bbox": [413, 158, 53, 138],
                        "category_id": 1
                    },
                    {
                        "bbox": [359, 218, 56, 103],
                        "category_id": 2
                    },
                    {
                        "bbox": [285, 568, 420, 397],
                        "category_id": 5
                    }
                ]
            }
        ]
    }
    test_categories = (1, 2, 3)

    result = get_files_annotations(test_data, test_categories, 0)
    print(result)
    assert result == {
        "test1.jpg": [
            [413, 158, 53, 138],
            [359, 218, 56, 103]
        ]
    }


def test_get_files_annotations_2() -> None:
    test_data = {
        "annotations": [
            {
                "file_name": "test1.png",
                "segments_info": [
                    {
                        "bbox": [413, 158, 53, 138],
                        "category_id": 1
                    },
                    {
                        "bbox": [359, 218, 56, 103],
                        "category_id": 2
                    },
                    {
                        "bbox": [285, 568, 420, 397],
                        "category_id": 5
                    }
                ]
            },
            {
                "file_name": "test2.png",
                "segments_info": [
                    {
                        "bbox": [855, 883, 499, 160],
                        "category_id": 3
                    },
                    {
                        "bbox": [153, 366, 662, 946],
                        "category_id": 2
                    }
                ]
            }
        ]
    }
    test_categories = (1, 2, 5)

    result = get_files_annotations(test_data, test_categories, 0)
    print(result)
    assert result == {
        "test1.jpg": [
            [413, 158, 53, 138],
            [359, 218, 56, 103],
            [285, 568, 420, 397]
        ],
        "test2.jpg": [
            [153, 366, 662, 946]
        ]
    }


def test_get_files_annotations_3() -> None:
    test_data = {
        "annotations": [
            {
                "file_name": "test2.png",
                "segments_info": [
                    {
                        "bbox": [855, 883, 499, 160],
                        "category_id": 3
                    },
                    {
                        "bbox": [153, 366, 662, 946],
                        "category_id": 2
                    }
                ]
            }
        ]
    }
    test_categories = (1, 2, 5)

    result = get_files_annotations(test_data, test_categories)
    print(result)
    assert result == {}
