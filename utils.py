import adbutils
import time
import logging

logger = logging.getLogger(__name__)

def get_device():
    try:
        adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
        devices = adb.device_list()
        if not devices: return None
        return devices[0]
    except Exception as e:
        logger.error(f"ADB Error: {e}")
        return None

def launch_app(device, package_name):
    logger.info(f"Restarting {package_name}...")
    device.shell(f"am force-stop {package_name}")
    time.sleep(1)
    device.shell(f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1")
    time.sleep(3)

def input_tap(device, x, y):
    device.shell(f"input tap {x} {y}")

def input_swipe(device, x1, y1, x2, y2, duration_ms):
    device.shell(f"input swipe {x1} {y1} {x2} {y2} {duration_ms}")

def input_text(device, text):
    safe_text = text.replace(" ", "%s") 
    device.shell(f"input text '{safe_text}'")