PROGRAM_VERSION = "3.2.0 2026-03-28"

# == library ==

import os
import _io
import importlib.util
import subprocess
import fnmatch
import time
from threading import Thread


# load when use

cv2 = None
pil_image = None
numpy = None

pytube = None
pydub = None

tkinter_filedialog = None

googletrans = None
translator = None

clipboard = None

pd = None
plt = None


# load method

def load_library(var, library_name: str|None, install_name: str|None = None, install_message: bool = True, upgrade: bool = False):
	if (var):
		return var

	try:
		spec = importlib.util.find_spec(library_name)
	except:
		spec = None

	if (spec == None):
		if (install_name == None):
			install_name = library_name
		
		if (install_message):
			print(f"NOTE: load_library: installing library {install_name}...")
		

		args = ["py", "-m", "pip", "install", install_name, "--quiet"]

		if (upgrade):
			args.append("--upgrade")

		subprocess.run(
			args,
			stdout = subprocess.DEVNULL,
			stderr = subprocess.DEVNULL
		)

	if (library_name == None):
			return None

	return importlib.import_module(library_name)

    


# == constants ==

IS_WIN: bool = os.name == "nt"

if (IS_WIN):
	os.system("color")


TERMCOLOR_CLEAR: str = "\033[0m"

TERMCOLOR_RED: str = "\033[31m"
TERMCOLOR_GREEN: str = "\033[32m"
TERMCOLOR_YELLOW: str = "\033[33m"
TERMCOLOR_BLUE: str = "\033[34m"

TERMCOLOR_BOLD: str = "\033[1m"
TERMCOLOR_GRAY: str = "\x1b[2m"




# == ask_file ==

def ask_file(file_types: list[tuple[str, str]] = [("All Files", "*")]) -> str:
	"provide user to select file by explorer, return file path in success, throw exception in failed"
	global tkinter_filedialog
	tkinter_filedialog = load_library(tkinter_filedialog, "tkinter.filedialog", "tkinter")

	file = tkinter_filedialog.askopenfilename(filetypes = file_types)
	if (file == None):
		raise Exception("No file chosen!")
	
	return file



# == OS / terminal ==

is_file = os.path.isfile
is_dir = os.path.isdir


class clear_t:
    def __repr__(self):
        self.clear()
        return ""
    def __call__(self):
        self.clear()
    
    def clear(self):
        if (IS_WIN):
            os.system("cls")
        else:
            print("\x1b[2J\x1b[00H", end = "")
        return ""

cls = CLS = clear = CLEAR = clear_t()



class chdir_t:
    def __repr__(self):
        return os.getcwd()
    def __call__(self, path = ""):
        self.set(path)

    def set(self, path = ""):
        if (not path):
            return
        try:
            os.chdir(path)
        except FileNotFoundError:
            print("ERROR: chdir: Couldn't find path!")

cd = chdir = chdir_t()



class list_dir_t:
	def __repr__(self):
		self.listdir()
		return ""
	def __call__(self, path = ""):
		self.listdir(path)

	def listdir(self, path = ""):
		os.system(("dir " if IS_WIN else "ls ") + ('"' + path + '"' if (path) else ""))

ls = list_dir = list_dir_t()




class list_tree_t:
	def __repr__(self):
		self.list_tree()
		return ""

	def __call__(self, top = os.curdir, patterns = ("*")):
		self.list_tree(top, patterns)

	def list_tree(top = os.curdir, patterns = ("*")):
		topLength = len(top)
		
		for r, ds, fs in os.walk(top):
			totalSpace = r[topLength:].count(os.sep)
			
			files = [fn for pattern in patterns for fn in fnmatch.filter(fs, pattern)]
			
			if (files and r != top):
				print(f"\x1b[1m{r[topLength+1:]}{os.sep}\x1b[0m")
			
			for fn in files:
				print("\t" * totalSpace + fn)


list_tree = list_tree_t()



def touch(files: str, *others: list[str]):
	# Touch files input by multi-line or path split text
	for filename in [fn for fn in files.split('\n') for fn in fn.split(os.pathsep)]:
		if (filename and not os.path.exists(filename)):
			open(filename, "x")
	
	# Touch files input by multi-args
	for filename in others:
		if (filename and type(filename) == str and not os.path.exists(filename)):
			open(filename, "x")



# ==== video ====

# == load ==

def load_video(object = None):
	"""load video by different type
	
	- object (cv2.VideoCapture) : return object
	- object (str) : load video from object
	- object (None) : provide explorer to select video file and load it
	"""
	global cv2
	cv2 = load_library(cv2, "cv2", "opencv-python")

	object_type = type(object)

	if (object_type == cv2.VideoCapture):
		return object

	if (object_type == str):
		return cv2.VideoCapture(object)

	if (object == None):
		return cv2.VideoCapture(ask_file([("Video files", "*.mp4 *.webm *.avi *.mov *.wmv *.flv"), ("All files", "*.*")]))

	raise Exception(f"invalid input type {object_type.__name__}")


# == get ==

def get_video_pos(video) -> int:
    return int(video.get(1))

def get_video_width(video) -> int:
    return int(video.get(3))

def get_video_height(video) -> int:
    return int(video.get(4))

def get_video_fps(video) -> float:
    return video.get(5)

def get_video_duration(video) -> int:
    return 1000 // video.get(5)

get_video_rate = get_video_duration		# alias


# == check ==

def is_vaild_video(video) -> bool:
    global cv2
    cv2 = load_library(cv2, "cv2", "opencv-python")

    return type(video) == cv2.VideoCapture and video.isOpened()


# == set ==

def set_video_pos(video, position: int):
	if (not is_vaild_video(video)):
		print("set_video_pos: not a video variable!")
		return
	
	video.set(1, int(position))


# == play ==

def play_video(video = None, window_name: str = "play_video", fullscreen: bool = False, loop: bool = True):
    global cv2
    cv2 = load_library(cv2, "cv2", "opencv-python")

    video = load_video(video)
    if (video == None):
        return

    video.set(1, 0)

    V_WIDTH = get_video_width(video)
    V_HEIGHT = get_video_height(video)
    V_FRAME_COUNT = video.get(7)

    V_FPS = get_video_fps(video)
    V_DURATION = get_video_duration(video)

    cv2.namedWindow(window_name,
        cv2.WINDOW_FULLSCREEN if fullscreen else cv2.WINDOW_NORMAL
    )
    cv2.resizeWindow(window_name, V_WIDTH, V_HEIGHT)


    screenshot_number = 1
    while (os.path.isfile(f"screenshot-{screenshot_number}.png")):
        screenshot_number += 1


    playing = True

    ret = False
    frame = None
    now = -1

    while (True):
        start = cv2.getTickCount()
		
        if (playing or not ret):
            ret, frame = video.read()
            now += 1

            if (ret == False):
                if (loop == True):
                    video.set(1, 0)
                else:
                    video.set(1, V_FRAME_COUNT - 1)
            
                ret, frame = video.read()

            cv2.imshow(window_name, frame)

        end = cv2.getTickCount()


		# delay_time around 1 to V_DURATION, calculate by V_DURATION - used_time
        used_time = (end - start) / 1e6
        delay_time = int(max(1, min(V_DURATION, V_DURATION - used_time)))

        key = cv2.waitKeyEx(delay_time)

        # == exit handle ==

        try:		# User closed window : Quit out
            cv2.getWindowProperty(window_name, 0)
        except:
            print(f"NOTE: play_video: ウィンドウ {window_name} を閉じる!")
            break

        if (key == 27):
            break

        # == option ==

        if (key == ord('t')):	# T : Take photo
            filename = f"screenshot-{screenshot_number}.png"
            screenshot_number += 1

            cv2.imwrite(filename, frame)
            print(f"NOTE: play_video: Screenshot saved to {filename}")
            continue
        
        if (key == ord(' ')):	# SPACE : Switch playing
            playing = not playing
            if (playing == True and video.get(1) == V_FRAME_COUNT):
                video.set(1, 0)
            continue
        
        if (key == ord('l')):
            loop = not loop
            print("NOTE: play_video: Loop play is " + ("enable" if (loop) else "disable") + " now!")
            if (loop == True and playing == False):
                playing = True
            continue
        
        if (key == 0x7a0000):
            fullscreen = not fullscreen
            cv2.setWindowProperty(window_name,
                cv2.WND_PROP_FULLSCREEN, (cv2.WINDOW_FULLSCREEN if fullscreen else 0)
            )
            continue

        # == move ==

        if (key >= ord('0') and key <= ord('9')):
            offset = V_FRAME_COUNT / 10 * (key - ord('0'))
        
        # 'A' : Move back 5 seconds
        elif (key == ord('a')):
            offset = now - V_FPS * 5 - 1
        
        # 'D' : Move front 5 seconds
        elif (key == ord('d')):
            offset = now + V_FPS * 5
        
        # ',' : Move back frame
        elif (key == ord(',')):
            offset = now - 1
        
        # '.' : Move front frame
        elif (key == ord('.')):
            offset =  now + 1
        else:
            continue

        offset = round(max(0, min(offset, V_FRAME_COUNT - 1)))
        now = offset
        video.set(1, offset)
        
        # Flush Frame after offset moved
        ret, frame = video.read()
        cv2.imshow(window_name, frame)



# == to ==

def to_cv2_image_list(video):
	video = load_video(video)

	frames = []
	while (True):
		ret, frame = video.read()
		if (ret == False):
			break
		frames.append(frame)
	return frames

def to_pil_image_list(video):
	video = load_video(video)

	frames = []
	while (True):
		ret, frame = video.read()
		if (ret == False):
			break
		frames.append(to_pil_image(frame))
	return frames






# == write ==

def write_mp4(object, output: str, fps: float, width: int, height: int):
	global cv2
	cv2 = load_library(cv2, "cv2", "opencv-python")

	def convert_thread(video, output: str, fps: float, width: int, height: int):
		writer = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

		orignal_pos = get_video_pos(video)
		set_video_pos(video, 0)
	
		while (True):
			ret, frame = video.read()
			if (ret == False):
				break

			if (frame.shape != (height, width, 3)):
				frame = cv2.resize(frame, (width, height))
			
			writer.write(frame)

		writer.release()
		set_video_pos(video, orignal_pos)

	video: None
	if (type(object) == cv2.VideoCapture):
		video = object
	elif (type(object) == str):
		video = cv2.VideoCapture(object)
	else:
		video = cv2.VideoCapture(ask_file([("Video files", "*.mp4 *.webm *.avi *.mov *.wmv *.flv"), ("All files", "*.*")]))

	Thread(target = convert_thread, args = [video, output, fps, width, height]).start()
	print("INFO: start writing " + output + " convertion!")






# ==== image ====

# == is ==

def is_pil_image(image):
	type_image = type(image)
	return type_image.__name__.find("PIL.", 0, 0) == 0 and type_image.__name__.find("Image") != -1



# == convert ==

def to_cv2_image(image):
	global numpy
	numpy = load_library(numpy, "numpy")

	numpy_img = numpy.array(image)
	return cv2.cvtColor(numpy_img, cv2.COLOR_RGB2BGR)

def to_pil_image(image):
	global cv2, pil_image
	pil_image = load_library(pil_image, "PIL.Image", "pillow")
	cv2 = load_library(cv2, "cv2", "opencv-python")

	frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	return pil_image.fromarray(frame_rgb)



# == load ==

def load_cv2_image(object: str|None = None):
	global pil_image, numpy, cv2
	pil_image = load_library(pil_image, "PIL.Image", "pillow")
	cv2 = load_library(cv2, "cv2", "opencv-python")

	object_type = type(object)
	if (object_type.__name__ == "numpy.ndarray"):
		return object

	if (object_type == str):
		return cv2.imread(object)

	if (is_pil_image(object)):
		return to_cv2_image(object)

	if (object == None):
		return cv2.imread(ask_file([("Image file", ".png *jpg *.jpeg *.ico"), ("All files", "*.*")]))

	raise Exception(f"invaild type {object_type.__name__}!")



def get_image_size(image) -> tuple[int, int]:
	if (is_pil_image(image)):
		return image.size

	image = load_cv2_image(image)
	return [image.shape[1], image.shape[0]]


def show_image(file: str|None = None, window_name: str = "imshow"):
	cv2.imshow(window_name, load_cv2_image(file))




# == GIF ==

def write_gif(object: list|str, output: str, duration: int = 0, loop: int = 0):
	global pil_image, cv2
	pil_image = load_library(pil_image, "PIL.Image", "pillow")

	# == convert object to pil_image list ==

	frames = []
	object_type = type(object)

	if (object_type == str and is_file(object)):
		video = load_video(object)
		frames = to_pil_image_list(video)

		if (duration == 0):
			duration = get_video_duration(video)
	
	elif (object_type == str and is_dir(object)):
		if (duration == 0):
			raise TypeError("missing 1 required positional argument: 'duration'")

		for file in os.listdir(object):
			if (file.rsplit(os.extsep, 1)[1] not in ("png", "jpg", "jpeg")):
				continue
			
			frames.append(pil_image.open(object + os.sep + file))

	elif (object_type == str):
		raise FileNotFoundError(f"{object} not exist")

	elif (object_type == list):
		if (duration == 0):
			raise TypeError("missing 1 required positional argument: 'duration'")

		for frame in object:
			if (type(frame).__name__ == "numpy.ndarray"):
				frames.append(to_pil_image(frame))
				continue
		
			frames.append(frame)

	elif (object_type == cv2.VideoCapture):
		if (duration == 0):
			duration = get_video_duration(object)

		frames = to_pil_image_list(object)

	else:
		raise Exception(f"Invalid object type {object_type.__name__}")


	# == write ==

	def write_gif_thread(output, frames, duration, loop):
		frames[0].save(output, save_all=True, append_images=frames[1:], duration=duration, loop=loop)

	Thread(target = write_gif_thread, args=[output, frames, int(duration), loop]).start()
	print(f"INFO: start writing {output}")



# ==== audio ====

def write_mp3(file: str, output: str):
    load_library(None, None, "ffmpeg")
    global pydub
    pydub = load_library(pydub, "pydub")

    def write_mp3_thread(file, dest):
        audio = pydub.AudioSegment.from_file(file)
        audio.export(dest, format = "mp3")

    Thread(target = write_mp3_thread, args = [file, output]).start()
    print(f"INFO: start writing {output}")


def download_youtube(url: str, dl_type: str = "video"):
	def rate_stream(stream, dl_type: str) -> int:
		quality_str: str = None
		if (dl_type == "audio"):
			quality_str = stream.abr
		else:
			quality_str = stream.resolution

		if (not quality_str):
			return 0

		quality_str = ''.join([ch for ch in quality_str if (ch.isdigit())])
		return int(quality_str)

	def work_thread(url, dl_type: str = "video"):
		# == load library ==

		global pytube, pydub
		load_library(None, None, "ffmpeg")

		pytube = load_library(pytube, "pytube", upgrade = True)
		pydub = load_library(pydub, "pydub")

		# == download ==

		video_urls = []

		if (url.find("https://www.youtube.com/playlist", 0) == 0):
			playlist = pytube.Playlist(url)
			video_urls = playlist.urls
		
			print(f"NOTE: download_youtube: プレイリスト {url} のダウンロードを始める")
		
		else:
			video_urls.append(url)
			print(f"NOTE: download_youtube: {dl_type} {url} のダウンロードを始める")
		

		success_count = 0

		for video_url in video_urls:
			try:
				yt = pytube.YouTube(video_url)
				adjusted_title = yt.title[:20]
			except:
				print(f"ERROR: download_youtube: {dl_type} {url} ダウンロードに失敗しました!")
				continue
			

			best_stream = None
			best_score = 0

			for stream in yt.streams:
				score = rate_stream(stream)

				if (score > best_score):
					best_stream = stream
					best_score = score

			if (best_stream == None):
				print(f"ERROR: download_youtube: {dl_type} {adjusted_title} に最適なストリームが見つかりませんでした!")
				continue

			file = best_stream.download()

			if (dl_type == "audio"):
				try:
					audio = pydub.AudioSegment.from_file(file)
				except:
					print(f"ERROR: download_youtube: {adjusted_title} の MP3 変換に失敗しました!")
					continue
				
				audio.export(file.rsplit(os.extsep, 1)[0] + ".mp3", format = "mp3")
				os.remove(file)
		
			success_count += 1

		print("NOTE: download_youtube: %s %s のダウンロードが完了しました (%d/%d)" % (
			dl_type, url, success_count, len(video_urls)
		))


	Thread(target = work_thread, args = [url, dl_type]).start()




# == show time ==

def show_time_loop():
    while (True):
        print("\r" + time.ctime(), end = "")

        now = time.time()
        time.sleep(int(now) + 1 - now)





##### attendance_t #####

class attendance_t:
	class row_t:
		def __init__(self, date, status, attendTime, lessonTime, room):
			self.date = date
			self.status = status
			self.attendTime = attendTime
			self.lessonTime = lessonTime
			self.room = room
	
		def __repr__(self):
			return self.date + '\t' + self.status + '\t\t' + self.attendTime + '\t\t' + self.lessonTime + '\t' + self.room + '\n'
	
		__str__ = __repr__
	
	
	def get_hours(self, time: str):
		splited = time.split(":")
		value = 0
		for part in splited:
			value *= 60
			value += float(part)
		return value
		
	def __init__(self, raw: str = None):
		self.rows = []
	
		if (not raw):
			global clipboard
			clipboard = load_library(clipboard, "clipboard")

			print("NOTE: download_youtube: input from clipboard")
			raw = clipboard.paste()
		
		if (raw.count('\n') == 0):
			try:
				raw = open(raw)
			except FileNotFoundError:
				print(f"ERROR: download_youtube: the input detected as file, but couldn't found that ({raw})")
		
		if (type(raw) == _io.TextIOWrapper):
			file = raw
			raw = file.read()
			file.close()
		
		for line in raw.splitlines():
			if (line.isspace()):
				continue
	
			splited = line.split('\t')
			idx = 0
			while (idx < len(splited)):
				if (not splited[idx]):
					splited.pop(idx)
				else:
					idx += 1
			if (len(splited) < 5):
				continue
	
			self.rows.append(self.row_t(splited[0], splited[1], splited[2], splited[3], splited[4]))
    
	def __repr__(self):
		output = "\x1b[1mDate\t\t\tStatus\t\tAttend Time\tLesson Time\tRoom\x1b[0m\n"
		for row in self.rows:
			if (row.status == "Absent"):
				output += TERMCOLOR_RED + str(row) + "\x1b[0m"
			else:
				output += str(row)
		output += '\n'

		output += "Record Count: %d\n" % (len(self.rows))
		output += "Attend Time: %.2f hour\n" % (self.get_attendance())
		output += "Miss Time: %.2f hour\n" % (self.get_missed())
		return output
	
	__str__ = __repr__
	
	def select(self, date = None, status = None, attendTime = None, lessonTime = None, room = None):
		result = attendance_t()
	
		for row in self.rows:
			if (status and row.status != status):
				continue
			if (lessonTime and row.lessonTime != lessonTime):
				continue
	
			result.rows.append(row)
	
		return result
	
	def get_attendance(self, totalHour: int = 1):
		attendMintues = 0
		for row in self.rows:
			if (row.status == "Absent"):
				continue
	
			lessonTime_splited = row.lessonTime.split(" - ")
			lessonEnd = self.get_hours(lessonTime_splited[1])
	
			if (row.status == "Present"):
				attendMintues += lessonEnd - self.get_hours(lessonTime_splited[0])
				continue
	
			attendMintues += lessonEnd - self.get_hours(row.attendTime)
	
		return attendMintues / (totalHour * 60)
	
	def get_missed(self, totalHour: int = 1):
		missedMintues = 0
		for row in self.rows:
			if (row.status == "Present"):
				continue
	
			lessonTime_splited = row.lessonTime.split(" - ")
			lessonStart = self.get_hours(lessonTime_splited[0])
	
			if (row.status == "Absent"):
				missedMintues += self.get_hours(lessonTime_splited[1]) - lessonStart
				continue
	
			missedMintues += self.get_hours(row.attendTime) - lessonStart
	
		return missedMintues / (totalHour * 60)


##### Python Object #####

def get_string_view_length(text: str) -> int:
	length: int = 0
	for char in text:
		length += 1 + 1 - char.isascii()
	return length


def details(obj: any, language: str = "ja"):
	# == content ==

	content = repr(obj)
	lines = content.splitlines()

	print()
	print("    " + "\n    ".join(lines[:12]))

	if (len(lines) > 12):
		print("    ...")
	
	print()
	
	# == 情報表示 ==

	object_type = type(obj)
	print(f"\x1b[32mクラス: {object_type.__module__}.{object_type.__name__}\x1b[0m")

	# コメントがない
	if (not obj.__doc__):
		print("\x1b[2mこのメソッドにコメントがありません!\x1b[0m")
		print()
		return

	# 原文で表示
	if (not language):
		print(obj.__doc__)
		print()
		return
	
	# 訳文で表示
	global googletrans, translator
	googletrans = load_library(googletrans, "googletrans", "googletrans==4.0.0rc1")

	if (translator == None):
		translator = googletrans.Translator()


	length = len(obj.__doc__)

	for i in range(length // 5000 + (1 if length % 5000 else 0)):
		content = translator.translate(obj.__doc__[i * 5000  : i + 4999], dest = language)
		print(content.text)
		time.sleep(1)
	
	print()


def show_object_methods(obj: any, findname: str = None, show_content: bool = True, show_colors: bool = True):
	METHODCOLOURS = [
		TERMCOLOR_GREEN,
		TERMCOLOR_BOLD + TERMCOLOR_YELLOW,
		TERMCOLOR_BOLD + TERMCOLOR_BLUE,
		TERMCOLOR_YELLOW,
		TERMCOLOR_BOLD + TERMCOLOR_GREEN,
		TERMCOLOR_BLUE,
		"",
		"\x1b[2m",
		TERMCOLOR_RED,
	]

	METHOD_CLASS	= 0
	METHOD_FUNCTION	= 1
	METHOD_STRUCTURE= 2
	METHOD_STRING	= 3
	METHOD_NUMBER	= 4
	METHOD_BOOL		= 5
	METHOD_NORMAL	= 6
	METHOD_NONE		= 7
	METHOD_ERROR	= 8



	def read_method_info(obj: any, methodName: str, methodInfo: list):
		try:
			method = getattr(obj, methodName)
			methodClass = method.__class__

			if (method == None):
				methodInfo[0] = METHOD_NONE
				return
		
			if (methodClass == bool):
				methodInfo[0] = METHOD_BOOL
				methodInfo[2] = method
				return
		
			if (methodClass in [int, float]):
				methodInfo[0] = METHOD_NUMBER
				methodInfo[2] = method
				return
		
			if (methodClass in [str, bytes]):
				methodInfo[0] = METHOD_STRING
				methodInfo[2] = method
				return
		
			if (methodClass == type or methodClass.__name__ == "module"):
				methodInfo[0] = METHOD_CLASS
				return
		
			if (callable(method)):
				methodInfo[0] = METHOD_FUNCTION
				return
		
			methodInfo[0] = METHOD_STRUCTURE
		except Exception as e:
			methodInfo[0] = METHOD_ERROR
			methodInfo[2] = e

	### Cleaning input ###
	if (findname):
		findname = findname.lower()

	### Collect method info ###
	firstResults = []
	secondResults = []
	thirdResults = []
	longest_name_length = 0
	
	for methodName in dir(obj):
		methodInfo = [METHOD_NORMAL, methodName, None]

		# Filter method if findname enabled
		if (findname):
			methodName_lowered = methodName.lower()
			if (methodName_lowered == findname):
				firstResults.append(methodInfo)
			
			elif (methodName_lowered.find(findname) == 0):
				secondResults.append(methodInfo)
			
			elif (methodName_lowered.find(findname) != -1):
				thirdResults.append(methodInfo)
		
			else:
				continue
		else:
			firstResults.append(methodInfo)

		# Longest name length for print table
		longest_name_length = max(longest_name_length, len(methodName))

		# Collect method type and expand info if showdetails enabled
		if (show_content):
			read_method_info(obj, methodName, methodInfo)

	
	# == Ready to print table ==

	termWidth = os.get_terminal_size()[0]
	
	longest_name_length = min(termWidth, longest_name_length + 1)
	rowLength	= termWidth // longest_name_length
	indexLength	= termWidth // rowLength
	
	firstResults.sort()
	secondResults.sort()
	thirdResults.sort()

	### Print method table ###

	index = 0
	count = 0

	for info in thirdResults + secondResults + firstResults:
		display_name = info[1]
		length = len(display_name)

		# Create expend display if possible
		
		if (info[2] != None):
			# Different display by class
			if (info[0] == METHOD_BOOL):
				extend = " (T)" if (info[2]) else " (F)"
			elif (info[0] == METHOD_ERROR):
				extend = " (" + info[2].__class__.__name__ + ")"
			else:
				extend = " (" + repr(info[2]) + ")"
			
			# use expand display if indexLength enough
			extendLength = get_string_view_length(extend)
			if (length + extendLength < indexLength):
				display_name += extend
				length += extendLength
		
		# Print and count

		print("%s%s%s%s" % (
			METHODCOLOURS[info[0]] if (show_colors) else "",
			display_name,
			"\x1b[0m" if (show_colors and show_content) else "",
			" " * max(1, indexLength - length)
		), end = "")

		index += 1
		count += 1

		# Next line if row full
		if (index >= rowLength):
			print()
			index = 0
	if (index > 0):
		print()
	
	### Print number of method ###
	print("\nCount: " + str(count))





# == pandas ==

def load_dataframe(file: str = None, low_memory: bool|None = None):
	global pd
	pd = load_library(pd, "pandas")

	if (file == None):
		file = ask_file([("CSV files", "*.csv"), ("All files", "*.*")])

	# == loads ==

	file_type = file.rsplit(os.extsep, 1)[1]

	if (file_type == "csv"):
		return pd.read_csv(file, low_memory = low_memory)

	if (file_type in ["xls", "xlsx"]):
		return pd.read_excel(file)

	if (file_type == "json"):
		return pd.read_json(file)

	if (file_type == "xml"):
		return pd.read_xml(file)

	print(f"ERROR: load_dataframe: Unsupported file type: {file_type}")




def plot_hist(**args):
	global plt
	plt = load_library(plt, "matplotlib.pyplot", "matplotlib")

	return plt.hist(**args)


def plot_line(**args):
	global plt
	plt = load_library(plt, "matplotlib.pyplot", "matplotlib")

	return plt.plot(**args)


def plot_pie(**args):
	global plt
	plt = load_library(plt, "matplotlib.pyplot", "matplotlib")

	return plt.pie(**args)


def plot_bar(**args):
	global plt
	plt = load_library(plt, "matplotlib.pyplot", "matplotlib")

	return plt.bar(**args)








# == old names ==

write_images_to_gif = write_gif

write_audio_to_mp3 = write_mp3

list_object_methods = show_object_methods

time_display = show_time_loop

set_video_position = set_video_pos




# === all ==

__all__ = [
	method for method in globals().keys()
		if method not in [
			"_io", "importlib", ""
			"cv2", "pil_image", "numpy", "pytube", "pydub", "tkinter_filedialog", "googletrans", "translator", "clipboard", "pd",
			"clear_t", "chdir_t", "list_dir_t", "list_tree_t"
		]
]
