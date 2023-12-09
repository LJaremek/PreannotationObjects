## Table of contents
- [Available models](#available-models)
- [How to download a model](#download-models)
- [Models used in the experiment](#used-models)


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


## 