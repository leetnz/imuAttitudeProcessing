# Script to use on bittle to capture video and csv log.
# 
# There isn't an easy way to synchronize the video capture and logging.
# When starting the capture, tap bittle to get a frame to sync the logs and video on.

from datetime import datetime

now = datetime.now()

logSuffix = now.strftime("%Y%m%d%H%M")

LOG_NAME = "bittle"+logSuffix+".log"
VID_NAME = "bittle"+logSuffix+".h264"


import subprocess 

MAXIMUM_RUNTIME_MS=300000

proc_video = None

def closeProcesses():
    print("Cleaning up")
    proc_video.terminate()
    print("Done")
    

import atexit
atexit.register(closeProcesses)

import serial

PORT="/dev/ttyS0"
BAUD=57600

from datetime import datetime
import time
time.sleep(5)

print(f"Writing logs to {LOG_NAME}")
print(f"Writing video to {VID_NAME}")

proc_video = subprocess.Popen(f"raspivid -o {VID_NAME} -t {MAXIMUM_RUNTIME_MS} -fps 25".split())

with open(LOG_NAME, "wb") as logf:
    with serial.Serial(PORT, BAUD) as ser:
        ser.flush()
        _ = ser.readline() # Drop first line

        while True:
            try:
                logf.write(ser.readline())
            except Exception as e: 
                print("Capture cancelled")
                break
