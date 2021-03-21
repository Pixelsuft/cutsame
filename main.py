from os import access as file_exists
from os import F_OK as file_exists_param
from os import get_terminal_size as get_size
from os import name as os_type
from sys import argv as sargs
from sys import exit as return_exit
from colorama import init as colorama_init
from colorama import Cursor as Pointer
from time import time as get_ticks
import cv2

if os_type == 'nt':
    from os import system as cmd_run
    from ctypes import windll as windows_dll
    windows_dll.kernel32.SetConsoleTitleW('Pixelsuft cutsame')
    cmd_run('color 0a')
    del windows_dll

args = sargs[1:]
colorama_init(autoreset=True)
video_path = None
out_path = None
fps = 30
frames_read = 0
frames_wrote = 0
i = 0
while i < len(args):
    if args[i] == '-v' or args[i] == '--video':
        i += 1
        video_path = args[i]
    elif args[i] == '-o' or args[i] == '--out':
        i += 1
        out_path = args[i]
    elif args[i] == '-fps' or args[i] == '--framerate':
        i += 1
        fps = int(args[i])
    i += 1
if not video_path:
    out_path = str(input('Enter video path: '))

if not video_path:
    out_path = str(input('Enter new out video path: '))

if not file_exists(str(video_path), file_exists_param):
    return_exit(-1)

cap = cv2.VideoCapture(video_path)
codec = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter(out_path, codec, fps, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
last_frame = []
last_frame = cap.read()[1]

print('\033[2J', Pointer.UP() * 20, end='')

started_at = get_ticks()

while True:
    frame = cap.read()[1]
    frames_read += 1
    for_test = frame == last_frame
    if type(for_test) == bool:
        break
    if not (for_test).all():
        last_frame = frame
        out.write(frame)
        frames_wrote += 1
    print(Pointer.UP() * 5, Pointer.BACK() * (get_size()[0] + 1), end='')
    need_str = f'Frames read: {frames_read}\nFrames wrote: {frames_wrote}'
    print(need_str, ' ' * int(len(need_str) - 1), end='')

end_at = get_ticks()
all_ = end_at - started_at
all_min = int(all_ / 60)
all_sec = int()

out.release()
