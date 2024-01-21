from ..tools.iou_math import jaccard_index


def test_jaccard_index_1() -> None:
    rect_1 = (20, 50, 100, 100)
    rect_2 = (20, 50, 100, 100)
    assert jaccard_index(rect_1, rect_2) == 1.0


def test_jaccard_index_2() -> None:
    rect_1 = (20, 50, 100, 100)
    rect_2 = (121, 151, 100, 100)
    assert jaccard_index(rect_1, rect_2) == 0.0


def test_jaccard_index_3() -> None:
    rect_1 = (0, 0, 50, 50)
    rect_2 = (0, 0, 25, 25)
    assert jaccard_index(rect_1, rect_2) == 0.25


def test_jaccard_index_4() -> None:
    rect_1 = (0, 0, 50, 50)
    rect_2 = (0, 0, 50, 25)
    assert jaccard_index(rect_1, rect_2) == 0.5
