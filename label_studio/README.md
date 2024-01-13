# Configure Label Studio

### 1. System environmnt variables
If you want to run Label Studio with local files hosting, you have to set two environment variables.

The first one make possible to use local storage.
The second one is the local storage path.

> [!NOTE]  
> When you will want to use local storage, you will have to use images from the folder in local storage.
> For example, if your `local_storage_path=/home/data`, your data for labeling could be in `local_storage_path=/home/data/images`.

Please open the file `/home/<user>/.bashrc` and at the end of the file add lines:
```bash
...

# Label Studio config
export LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
export LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=<local storage path>
```

Then restart the system.

More in documentation: https://labelstud.io/guide/start.html#Command-line-arguments-for-starting-Label-Studio


### 2. Create json file
You have to create a json file with images which you want to upload to Label Studio. Remember, that you can generate pre-annotations with the app!

You can use a `label_studio/server.py` with the endpoint `prepare_ls_json` to generate files json with annotations.


#### 2.1. Starting server
Run server by the command:
```bash
python label_studio/server.py
```

Use `prepare_ls_json` endpoint. You can check example calling in `label_studio/call_prepare_ls_json.py`

After call `call_prepare_ls_json`, you will see `files_with_annotations.json` file which you can upload to Label Studio project.

Remember, that you have to specify label names in project settings in "Label Interface" page.
