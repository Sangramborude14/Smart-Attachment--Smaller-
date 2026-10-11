import RPi.GPIO as GPIO
import time
import requests
import subprocess
from datetime import datetime
import os
# ================= CONFIG =================
FLAME_PIN = 17          # Flame sensor DO (HIGH = flame detected)
SMOKE_PIN = 27          # Smoke/Gas sensor DO (LOW = smoke detected)
BUZZER_PIN = 18
PUSHBULLET_TOKEN = os.environ["PUSHBULLET_TOKEN"]
CONFIRM_COUNT = 3       # Number of consecutive detections
CHECK_DELAY = 1         # Seconds between checks
IMAGE_DIR = "/home/pi/alert_images"
CAMERA_CMD = "/usr/bin/rpicam-still"
# ---------------- GPIO SETUP ----------------
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLAME_PIN, GPIO.IN)
GPIO.setup(SMOKE_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)
# ---------------- UTILITY FUNCTIONS ----------------
def buzz_on():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
def buzz_off():
    GPIO.output(BUZZER_PIN, GPIO.LOW)
def capture_image():
    """
    Captures an image using CSI camera ONLY when called.
    Returns image path if successful, else None.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"{IMAGE_DIR}/alert_{timestamp}.jpg"
    result = subprocess.run(
        [
            CAMERA_CMD,
            "-o", image_path,
            "--timeout", "1000",
            "--nopreview"
        ],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("Camera capture failed")
        print(result.stderr)
        return None
    print(f" Image captured: {image_path}")
    return image_path
def send_pushbullet(image_path):
    """
    Sends Pushbullet notification with image
    """
    try:
        with open(image_path, "rb") as img:
            upload_req = requests.post(
                "https://api.pushbullet.com/v2/upload-request",
                headers={"Access-Token": PUSHBULLET_TOKEN},
                json={
                    "file_name": "alert.jpg",
                    "file_type": "image/jpeg"
                }
            )
            upload_data = upload_req.json()
            requests.post(
                upload_data["upload_url"],
                files={"file": img}
            )
            push_data = {
                "type": "file",
                "file_name": "alert.jpg",
                "file_type": "image/jpeg",
                "file_url": upload_data["file_url"],
                "body": " FIRE / GAS ALERT!\nSmoke or flame detected at home."
            }
            requests.post(
                "https://api.pushbullet.com/v2/pushes",
                headers={"Access-Token": PUSHBULLET_TOKEN},
                json=push_data
            )
        print(" Pushbullet alert sent")
    except Exception as e:
        print(" Pushbullet error:", e)
        
# ---------------- MAIN PROGRAM ---------------
def fire_smoke_monitor():
    os.makedirs(IMAGE_DIR, exist_ok=True)
    print(" Fire & Gas Monitoring Started")
    print(" Waiting for sensor trigger...")
    trigger_count = 0
    alert_sent = False
    try:
        while True:
            flame = GPIO.input(FLAME_PIN)   # HIGH = flame
            smoke = GPIO.input(SMOKE_PIN)   # LOW  = smoke/gas
            print(f"Flame: {flame} | Smoke: {smoke}")
            # Trigger if EITHER sensor detects danger
            if flame == GPIO.HIGH or smoke == GPIO.LOW:
                trigger_count += 1
                print(f" Trigger count: {trigger_count}")
            else:
                trigger_count = 0
                alert_sent = False
                buzz_off()
            if trigger_count >= CONFIRM_COUNT and not alert_sent:
                print(" DANGER CONFIRMED")
                buzz_on()
                image_path = capture_image()
                if image_path:
                    send_pushbullet(image_path)
                alert_sent = True
            time.sleep(CHECK_DELAY)
    except KeyboardInterrupt:
        print("\n Program stopped by user")
    finally:
        buzz_off()
        GPIO.cleanup()


fire_smoke_monitor()