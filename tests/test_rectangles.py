from random import seed

from ..tools.rectangles import move_rect_by_percentage
from ..tools.rectangles import filter_rectangles
from ..tools.rectangles import get_coco_rects


def test_get_coco_rects_1() -> None:
    data = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 1, 2, 3]
    ]
    assert get_coco_rects(data) == data


def test_get_coco_rects_2() -> None:
    data = []
    assert get_coco_rects(data) == data


def test_filter_rectangles_1() -> None:
    rects1 = [
        (0, 0, 50, 50)
    ]
    rects2 = [
        (0, 0, 25, 25)
    ]
    results = (
        [(0, 0, 50, 50)],
        [(0, 0, 25, 25)],
        0.25, 0.25
    )

    assert filter_rectangles(rects1, rects2, 0.2) == results


def test_filter_rectangles_2() -> None:
    rects1 = [
        (0, 0, 50, 50),
        (0, 0, 50, 25)
    ]
    rects2 = [
        (0, 0, 25, 25)
    ]
    results = (
        [(0, 0, 50, 25)],
        [(0, 0, 25, 25)],
        0.375,
        0.5
    )

    assert filter_rectangles(rects1, rects2, 0.3) == results


def test_filter_rectangles_3() -> None:
    rects1 = [
        (0, 0, 50, 50),
        (0, 0, 50, 25)
    ]
    rects2 = [
        (0, 0, 25, 25),
        (40, 40, 10, 10)
    ]
    results = (
        [(0, 0, 50, 25)],
        [(0, 0, 25, 25)],
        0.1975,
        0.5
        )

    assert filter_rectangles(rects1, rects2, 0.3) == results


def test_filter_rectangles_4() -> None:
    rects1 = [
        (0, 0, 50, 50),
        (0, 0, 50, 25)
    ]
    rects2 = [
        (100, 100, 25, 25),
        (200, 200, 10, 10)
    ]

    assert filter_rectangles(rects1, rects2, 0.3) == ([], [], 0, 0)


def test_move_rect_by_percentage_1() -> None:
    seed(1104)
    result = (60.0, 60.0, 100, 100)
    assert move_rect_by_percentage(50, 50, 100, 100, 10) == result


def test_move_rect_by_percentage_2() -> None:
    seed(1104)
    result = (70.0, 70.0, 100, 100)
    assert move_rect_by_percentage(50, 50, 100, 100, 20) == result


def test_move_rect_by_percentage_3() -> None:
    seed(1104)
    result = (100.0, 100.0, 100, 100)
    assert move_rect_by_percentage(50, 50, 100, 100, 50) == result


def test_move_rect_by_percentage_4() -> None:
    seed(4011)
    result = (50, 0.0, 150.0, 100)
    assert move_rect_by_percentage(50, 50, 100, 100, 50) == result
