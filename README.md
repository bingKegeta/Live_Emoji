# Live Emoji

Live Facial Landmark Recognition and 3D model manipulation.

## To install:

1. Set up a python environment (conda/miniconda/system)
2. If using conda:

```shell
git clone https://github.com/bingKegeta/Live_Emoji
cd Live_Emoji
conda create -n emoji python=3.11
conda activate emoji
pip install -r installations
```
> If you have pip set up, it should be fine to just do pip install -r installations in the repo directory. If not, it is an exercise left to the reader.

## To Use (currently):

```shell
python face_detect.py
```
Currently, this is how to get the camera output along with the detected features onto the TKinter GUI.
This will be changed to reflect as development continues.

> Note: The "official" GUI is mostly made and can be seen by running:
> ```shell
>    python main.py
> ```
