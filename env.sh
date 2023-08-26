#!/bin/bash
conda create --name testipykernel --file ./requirements.txt
eval "$(conda shell.bash hook)"
conda activate testipykernel
conda install ipykernel
# conda install -c esri mmdet
conda install pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch -c nvidia
pip install mmcv-full
pip install mmdet==2.28.2
