# add mytool.py to your python library
# ! not sure this program work successfully

import os;

FILES = ["lazy_import.py", "mytool.py"]

for file in FILES:
    code_file = open(file, "rb");
    dest_file = open(os.__file__.rsplit(os.sep, 1)[0] + os.sep + file, "wb");

    dest_file.write(code_file.read());

    dest_file.close();
    code_file.close();

print("files copying are done!")
print("exit after 1 second...")

from time import sleep
sleep(1);
