# mytool

some useful methods for python interpreter, this install require library dynamically

## How to install

First, make sure you have installed python in version 3. Then, download this package and run make_mytool3.py.

Or you can run this command to install

```
git clone https://github.com/kazuki1717/mytool3-python
py mytool3-python/add_mytool3.py
```

## Suggest to import

```python
from mytool3 import *
```

---

## Methods

**list_object_methods()**

list `object` all method name, colored and order by method type, also shows their value if possible

```python
def list_object_methods(object, findname: str = "", details: bool = True, colors: bool = True) -> None:
  pass
```
- object : a variable you want to know
- findname : filter methods by name to only show you wanted
- details : will the list show its value if possible (False would faster)
- colors : will the list content colored by method type (False would faster)


**clear**

clear terminal text

usage:
```python
clear    # no () needed
cls    # alias of clear
```


**chdir**

show/change working directory

```python
chdir          # print current path, no () needed
chdir(dest)    # change working directory to dest
```


**list_dir**

show directory files

```python
list_dir        # show all files in current directory
list_dir(path)  # show all files in path
```


**list_tree**

```python
list_tree        # show files tree in current directory
list_tree(path)  # show files tree in path
```


**load_video()**

load opencv2.VideoCapture from file path or explorer select

```python
video: cv2.VideoCapture = load_video(path);  # open file in `path`

video: cv2.VideoCapture = load_video();      # ask user file by open an exploer and open it
```
- path : video path in str, or open explorer to select if None


**play_video()**

play video in new monitor

```python
def play_video(video: str | None | cv2.VideoCapture = None) -> None:
  pass
```
- video : to play in display, you can put video object, file name or None to open explorer selecting


**get_video_...(video)**

get video information

```python
WIDTH     = get_video_width(video)
HEIGHT    = get_video_height(video)
FPS       = get_video_fps(video)
DURATION  = get_video_duration(video)
```


**is_valid_video()**

is the video vaild

```python
valid = is_valid_video(video);
```
- video : cv2.VideoCapture


**write_images_to_gif()**

make GIF

```python
# == constants ==
FOLDER = "frames/";
DURATION = 1000 / 25;
LOOP = 0;

# == useway 1 ==
write_images_to_gif(FOLDER, "output.gif", DURATION, LOOP);

# == useway 2 ==
frames = [load_image(file) for file in os.listdir(FOLDER)];
write_images_to_gif(frames, "output.gif", DURATION, LOOP):

```
- frames : GIF frames, it could be a directory path storing frames or image list
- output : ouput GIF name
- duration : every frame time to next frame
- loop : how many times the GIF will loops, default: 0 (mean infine)



## ライセンス

MIT License
