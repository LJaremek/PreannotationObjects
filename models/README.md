## Table of contents
- [Available models](#available-models)
- [How to download a model](#how-to-download-a-model)
- [Models used in the experiment](#models-used-in-the-experiment)
- [Experiment](#experiment)
    - [Experiment results](#experiment-results)
- [Recreating the experiment](#recreating-the-experiment)


## Available models
List of available models is located on the main github repository of mmdetecion project:
https://github.com/open-mmlab/mmdetection?tab=readme-ov-file#overview-of-benchmark-and-model-zoo


## How to download a model
If we want to download the model, we can use the command
```shell
mim download mmdet --config <MODEL NAME> --dest ./models/
```


## Models used in the experiment
Because of the _big_ size of models checkpoint files, we do not storage them on the repo. </br> 
If you want to recontruct the experiment below, you can type the comamnd:
```shell
mim download mmdet --config  yolox_tiny_8x8_300e_coco --dest ./models/
mim download mmdet --config  ssdlite_mobilenetv2_scratch_600e_coco --dest ./models/
mim download mmdet --config yolov3_mobilenetv2_320_300e_coco --dest ./models/
```


## Experiment
I compared three models which are available on CPU (I assume that the person who wants to pre-label the data does not have a graphics card. He probably has a simple laptop). The models are:
 - ssd - [Single Shot MultiBox Detector](https://arxiv.org/abs/1512.02325)
 - yolov3 - [You Only Look Once](https://arxiv.org/abs/1804.02767) 
 - yolox - [You Only Look Once X](https://arxiv.org/abs/2107.08430)

</br>

I examined the following elements of the models:
- model loading time
- model labeling time (every model has the same data set)
- model avg Jaccard index
- Images without correct detections

</br>

### Experiment results
| Name | AVG JI | Size [mb] | Loading time [s] | Labeling time [s] | Without detections |
| :---: | ---: | ---: | ---: | ---: | ---: |
| yolov3 | 0.43 | 17 | 0.15 | 30.25 | 246 |
| ssdlite | 0.47 | 15 | 0.16 | 42.50 | 230 |
| yolox | 0.60 | 20 | 0.20 | 49.20 | 158 |

As you can see, yolox is the _largest_ model, but it has the best Jaccard index value and the smallest number of images without correct detections - so we can choose the model for production.


## Recreating the experiment
If you want to reconstruct the experiment, you can run this command:
```shell
python ./compare_models.py
```
Please note that experiment results may vary slightly due to processor power or random elements in the models.
