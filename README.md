# PreannotationObjects
Pre annotation of objects project.

### Repository content:
* [IoU informations](./iou/README.md)

</br>

### Getting started
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

### Upload file to Label-Studio
Data in Label-Studio are stored in folder
```
/home/<USER>/.local/share/label-studio/media/upload/<PROJECT_ID>
```

To start local file hosting you can run a aserver.py by:
```
python server.py
```

And then, the files located in the UPLOAD_FOLDER (const variable in the file) could be hosted, for example:
```Python
# server.py
...
UPLOAD_FOLDER = Path("/home/user/my_images")
...
```
And then the url is:
```
http://127.0.0.1:8000/image_to_url/my_image.jpg
```

If you want to upload some photo to label-studio you can use the CURL command:
```
curl -H 'Content-Type: application/json' -H 'Authorization: Token <TOKEN>' -X POST 'http://localhost:8080/api/projects/<PROJECT_ID>/import' --data '[{"image": "http://127.0.0.1:8000/image_to_url/<IMAGE.jpg>"}]'
```

### Images with annotations:
https://drive.google.com/drive/folders/1JNP46nw0OVIX_uzomTteNaHThS8vcb_t?usp=sharing
