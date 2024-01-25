from random import seed

import numpy as np

from ..label_studio.server import prepare_label_config
from ..label_studio.server import parse_model_results
from ..label_studio.server import rand_hex_color


def test_rand_hex_color_1() -> None:
    seed(2601)
    assert rand_hex_color() == "d7b210"


def test_rand_hex_color_2() -> None:
    seed(603)
    assert rand_hex_color() == "2b8e92"


def test_rand_hex_color_3() -> None:
    seed(813)
    assert rand_hex_color() == "e62160"


def test_parse_model_results_1() -> None:
    class SingleStageDetector:
        CLASSES = ["car", "bike", "boat"]

    model = SingleStageDetector()
    model_results = [
        np.array([
            (0, 0, 100, 100, 0.4)
        ]),
        np.array([
        ]),
        np.array([
        ])
    ]
    size = 1000

    test_results = [
        {
            "result":
            [
                {
                    "value": {
                        "x": 0.0,
                        "y": 0.0,
                        "width": 10.0,
                        "height": 10.0,
                        "rectanglelabels": [
                            "car"
                        ]
                    },
                    "from_name": "label",
                    "to_name": "image",
                    "type": "rectanglelabels"
                }
            ]
        }
    ]

    received_results = parse_model_results(model, model_results, size, size)

    assert received_results == test_results


def test_parse_model_results_2() -> None:
    class SingleStageDetector:
        CLASSES = ["car", "bike", "boat"]

    model = SingleStageDetector()
    model_results = [
        np.array([
            (0, 0, 100, 100, 0.4)
        ]),
        np.array([
            (0, 0, 100, 100, 0.1)
        ]),
        np.array([
        ])
    ]
    size = 1000

    test_results = [
        {
            "result":
            [
                {
                    "value": {
                        "x": 0.0,
                        "y": 0.0,
                        "width": 10.0,
                        "height": 10.0,
                        "rectanglelabels": [
                            "car"
                        ]
                    },
                    "from_name": "label",
                    "to_name": "image",
                    "type": "rectanglelabels"
                }
            ]
        }
    ]

    received_results = parse_model_results(model, model_results, size, size)

    assert received_results == test_results


def test_parse_model_results_3() -> None:
    class SingleStageDetector:
        CLASSES = ["car", "bike", "boat"]

    model = SingleStageDetector()
    model_results = [
        np.array([
            (0, 0, 100, 100, 0.4)
        ]),
        np.array([
            (0, 0, 100, 100, 0.1)
        ]),
        np.array([
        ])
    ]
    size = 1000

    test_results = [
        {
            "result": []
        }
    ]

    received_results = parse_model_results(
        model, model_results, size, size, 0.5
        )

    assert received_results == test_results


def test_parse_model_results_4() -> None:
    class SingleStageDetector:
        CLASSES = ["car", "bike", "boat"]

    model = SingleStageDetector()
    model_results = [
        np.array([
            (0, 0, 100, 100, 0.4)
        ]),
        np.array([
        ]),
        np.array([
            (20, 20, 80, 80, 0.1)
        ])
    ]
    size = 1000

    test_results = [
        {
            "result":
            [
                {
                    "value": {
                        "x": 0.0,
                        "y": 0.0,
                        "width": 10.0,
                        "height": 10.0,
                        "rectanglelabels": [
                            "car"
                        ]
                    },
                    "from_name": "label",
                    "to_name": "image",
                    "type": "rectanglelabels"
                },
                {
                    "value": {
                        "x": 2.0,
                        "y": 2.0,
                        "width": 6.0,
                        "height": 6.0,
                        "rectanglelabels": [
                            "boat"
                        ]
                    },
                    "from_name": "label",
                    "to_name": "image",
                    "type": "rectanglelabels"
                }
            ]
        }
    ]

    received_results = parse_model_results(
        model, model_results, size, size, 0.0
        )

    assert received_results == test_results


def test_prepare_label_config_1() -> None:
    seed(813)
    classes = ["car", "boat", "plane"]
    result = """
        <View>
            <Image name="image" value="$image"/>
            <RectangleLabels name="label" toName="image">
                \n<Label value="car" background="#e62160"/>
                \n<Label value="boat" background="#e62160"/>
                \n<Label value="plane" background="#e62160"/>
            </RectangleLabels>
        </View>
        """
    return prepare_label_config(classes) == result


def test_prepare_label_config_2() -> None:
    seed(603)
    classes = ["Python<3"]
    result = """
        <View>
            <Image name="image" value="$image"/>
            <RectangleLabels name="label" toName="image">
                \n<Label value="Python<3" background="#2b8e92"/>
            </RectangleLabels>
        </View>
        """
    return prepare_label_config(classes) == result


def test_prepare_label_config_3() -> None:
    classes = []
    result = """
        <View>
            <Image name="image" value="$image"/>
            <RectangleLabels name="label" toName="image">
            </RectangleLabels>
        </View>
        """
    return prepare_label_config(classes) == result
