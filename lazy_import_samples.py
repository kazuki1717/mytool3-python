# samples of lazy_import usage
# from lazy_import_examples import *

from lazy_import import lazy_import


cv2 = lazy_import("cv2", "opencv-python")
pil_image = lazy_import("PIL.Image", "Pillow")
numpy = lazy_import("numpy")

pytube = lazy_import("pytube", upgrade = True)
pydub = lazy_import("pydub", ["ffmpeg", "pydub"])

tkinter_filedialog = lazy_import("tkinter.filedialog", "tkinter")

googletrans = lazy_import("googletrans", "googletrans==4.0.0rc1")
translator = None;

clipboard = lazy_import("clipboard")

pandas = lazy_import("pandas")
plt = lazy_import("matplotlib.pyplot", "matplotlib")



WordCloud = lazy_import("wordcloud.WordCloud", "wordcloud")

