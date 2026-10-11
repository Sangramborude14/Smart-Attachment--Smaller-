#This file converts the CSI input of Pi 5 to v4l2, because motionEYE works best with v4l2
#Keep in mind, this file requires the virtual environment "motioneye-env" command to activate - source ~/motioneye-venv/bin/activate
import subprocess
import time
import signal
import sys
import os

#These are specifications of output video, increasing fps can heatup the CPU, I used 30 because that is the highest MotionEye supports
VIDEO_OUT = "/dev/video40"
WIDTH = "1280"
HEIGHT = "720"
FPS = "30"

#CMD arguments for video input tool (RPI-CAM)
RPICAM_CMD = [
    "rpicam-vid",
    "-t", "0",
    "--codec", "yuv420",
    "--width", WIDTH,
    "--height", HEIGHT,
    "--framerate", FPS,
    "--inline",
    "--nopreview",
    "-o", "-"
]

#CMD arguments for video convertor tool (ffmpeg)
FFMPEG_CMD = [
    "ffmpeg",
    "-hide_banner",
    "-loglevel", "error",
    "-fflags", "nobuffer",
    "-flags", "low_delay",
    "-f", "rawvideo",
    "-pix_fmt", "yuv420p",
    "-video_size", f"{WIDTH}x{HEIGHT}",
    "-framerate", FPS,
    "-i", "-",
    "-f", "v4l2",
    VIDEO_OUT
]

running = True

#This function creates a new device "DummyCam"
def ensure_loopback():
    if not os.path.exists(VIDEO_OUT):
        print("[+] Creating v4l2loopback device")
        subprocess.run(
            [
                "modprobe", "v4l2loopback",
                "video_nr=40",
                "card_label=DummyCam",
                "exclusive_caps=1"
            ],
            check=True
        )

def shutdown(sig, frame):
    global running
    print("\n[!] Shutting down cleanly")
    running = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

#This function converts the video input to v4l2 and directs it to DummyCam
def start_v4l2_camera():
    ensure_loopback()

    while running:
        print("[+] Starting rpicam → v4l2 pipeline")

        try:
            cam = subprocess.Popen(
                RPICAM_CMD,
                stdout=subprocess.PIPE
            )

            ff = subprocess.Popen(
                FFMPEG_CMD,
                stdin=cam.stdout
            )

            cam.stdout.close()
            ff.wait()

        except Exception as e:
            print("[ERROR]", e)

        if running:
            print("[!] Pipeline stopped, restarting in 2s")
            time.sleep(2)

start_v4l2_camera()
