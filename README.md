# PreannotationObjects
Pre annotation of objects project.

### 1. Repository content:
* [IoU informations](./iou/README.md)
* [Comparing models](./models/README.md)
* [Label Studio configuration](./label_studio/README.md)
* [Unit tests](./tests/README.md)

</br>

### 2. Files structure
```
.
├── coco                        <-- images for models experiments
│   ├── annotations
│   ├── images
│   ├── iou
│   └── panoptic_val2017.json
├── iou                         <-- data for IoU experiments
│   ├── images
│   └── README.md
├── label_studio                <-- microservis with example using
│   ├── test_images
│   ├── README.md
│   ├── call_*.py
│   └── server.py
├── models                      <-- models config and checkpoints files
│   ├── README.md
│   └── experiment_models.json
├── tests                       <-- unit tests
│   ├── README.md
│   └── test_*.py
├── tools                       <-- math and auxiliary functions
├── README.md
├── env.sh                      <-- preparing conda virtual environment
└── requirements.txt
```


### 3. Getting started
Clone this repo to your computer:
```shell
git clone https://github.com/LJaremek/PreannotationObjects.git
cd ./PreannotationObjects/
```

Please run env.sh to create the conda environment 'preannotation':
```shell
chmod +x env.sh
./env.sh
```

Then, activate the environment:
```shell
conda activate preannotation
``` 

</br>

### 4. Upload file to Label-Studio
The complete instruction is in [Label Studio folder README](./label_studio/README.md).


### 5. Images with annotations
For reproducing experiments you can download the `coco` folder to root project folder from:
https://drive.google.com/drive/folders/1JNP46nw0OVIX_uzomTteNaHThS8vcb_t?usp=sharing


### 6. Short demo:
To run local server with endpoints:
```bash
python server.py
```


You can create Label Studio project by execute example file:
```bash
python label_studio/call_create_ls_project.py
```

And then preapre json file for Label Studio project:
```bash
python label_studio/call_prepare_ls_json.py
```
