# from lazy_import import *

import subprocess
import importlib, importlib.util

from sys import stderr, executable as python_executable
from threading import Thread, Lock
from time import sleep

class lazy_import:
    """lazy_import 1.1.0

url: https://github.com/kazuki-1717/mytool3-python

import module when use, also install library if module not installed

usage:
```
module = lazy_import(
    "module_name",              # import module by this
    ["install_option1", ...],   # if "module_name" not exist, installs modules by this list (default: refer to module_name)
    /,
    upgrade = False              # always upgrade module before import (default: false)
)
```


samples:
```python
# load lazy_import
from lazy_import import lazy_import

# import numpy. install numpy if not existed
numpy = lazy_import("numpy")

# import cv2. install cv2 by its fullname 'opencv2-python'
cv2 = lazy_import("cv2", "opencv2-python")

# import matplotlib.pyplot as plt. install matplotlib if not existed
plt = lazy_import("matplotlib.pyplot", "matplotlib")

# import pydub. install ffmpeg and pydub if not existed
pydub = lazy_import("pydub", ["ffmpeg", "pydub"])

# always upgrade pytube before import pytube**
pytube = lazy_import("pytube", upgrade = True)
```
"""

    _install_query = []
    _install_thread = None
    _lock = Lock()



    def __init__(self, module_name: str|None, install_names: list|str|None = None, /, upgrade: bool = False):
        if (module_name == None):
            raise ValueError("error: module name cannot be None")
        
        self.module_name = module_name
        self.install_names = install_names
        self.module = None
        self.upgrade = upgrade
        
        lazy_import._insert_install_task(-1, self)



    def _import(self):
        # exit if module already imported
        if (self.module is not None):
            return;
    
        # if module installed, import it here
        if (self.is_installed()):
            with lazy_import._lock:
                self.module = importlib.import_module(self.module_name);
            return;

        # waiting install finish
        lazy_import._insert_install_task(0, self);      # for first processing

        while (self.module is None):
            sleep(1);


    @staticmethod
    def _insert_install_task(index, task):
        with lazy_import._lock:
            lazy_import._install_query.insert(index, task);

            if (lazy_import._install_thread is None):
                lazy_import._install_thread = Thread(target = task._install_worker, daemon=True);
                lazy_import._install_thread.start();

    def _install(self):
        # == check if module imported or installed ==

        if (self.module is not None):
            return;
    
        # == install ==
        if (not self.is_installed()):
            # convert types
            if (self.install_names == None):
                self.install_names = [self.module_name];
            
            elif (type(self.install_names) == str):
                self.install_names = [self.install_names];
            
            # install
            for name in self.install_names:
                subprocess.run(
                    [python_executable, "-m", "pip", "install", name, "--quiet"] + (["--upgrade"] if self.upgrade else []),
                    stdout = subprocess.DEVNULL,
                    stderr = subprocess.DEVNULL
                );

        # == import ==
        try:
            with lazy_import._lock:
                self.module = importlib.import_module(self.module_name);
        except Exception as e:
            print("ERROR: lazy_import-thread: failed to import '" + self.module_name + "' since " + str(e), file = stderr);

    @staticmethod
    def _install_worker():
        while (lazy_import._install_query):
            with lazy_import._lock:
                task = lazy_import._install_query.pop(0)
            
            task._install()

            if (not lazy_import._install_query):
                sleep(1)

        lazy_import._install_thread = None;

    

    def is_installed(self) -> bool:
        try:
            return not self.upgrade and importlib.util.find_spec(self.module_name) is not None
        except ModuleNotFoundError:
            return False


    def __getattr__(self, attr_name):
        self._import();
        return getattr(self.module, attr_name);

    def __dir__(self):
        self._import();
        return dir(self.module);

    def __repr__(self):
        return "lazy_import(%s, %s%s)" % (
            self.module_name, self.install_names, ", upgrade = true" if self.upgrade else ""
        )

