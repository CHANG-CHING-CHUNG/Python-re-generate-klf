import os
from subprocess import call

dir_path = "/home/blpha/data/"

call("sudo chmod 777 /home/", shell=True)

print(f'dir_path: {dir_path}')

# check if directory exists or not yet
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

if os.path.exists(dir_path):
    # copy files into created directory
    call(f"cp -r ./AI2OQA/ {dir_path}", shell=True)
    call(f"cp -r ./input_klf_backup/ {dir_path}", shell=True)
