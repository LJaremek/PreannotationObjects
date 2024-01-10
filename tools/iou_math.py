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
