from datetime import datetime
import os
from time import sleep
import json

import requests
from dotenv import load_dotenv



from nanovicky.components.thread_component import ThreadComponent
from nanovicky.components.capture.base_capture_component import BaseCaptureComponent
from nanovicky.components.capture.cameras.usb_camera_component import UsbCameraComponent


from nanovicky.components.streamer.webstreamer import WebStreamerComponent
from nanovicky.components.performance.scheduler import SchedulerComponent
from nanovicky.models.links.link import FlowLink
from nanovicky.models.frame import Frame


load_dotenv()

IVSFLEX_API_URL: str = str(os.environ.get("IVSFLEX_API_URL"))
BUFFER_IMAGE: Frame = None


def send_data():
    global BUFFER_IMAGE
    if BUFFER_IMAGE is None:
        return

    base64_image = BUFFER_IMAGE.to64().decode("utf-8")
    payload = json.dumps(
        {
            "image": base64_image,
            "camera_id": int(os.environ.get("CAMERA_ID")),
            "timestamp": datetime.now().timestamp(),
            "count": 0,
        }
    )
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.request(
            "POST", f"{IVSFLEX_API_URL}/datas/add", headers=headers, data=payload
        )
        if not 200 <= response.status_code < 300:
            print("An error occured while sending the data to the API")
            print(response.text)
        print(response.status_code)
    except:
        print("Warning api not available")

def main():
    global BUFFER_IMAGE

    # Setup all components
    components = {
        "camera": BaseCaptureComponent("camera0", UsbCameraComponent(0, "cam1", (1920, 1080), 1), 1),
        "streamer": WebStreamerComponent("Webstreamer0", "0.0.0.0"),
    }

    thread_components = {
        "scheduler": SchedulerComponent(
            "schelduler0",
            [(os.getenv("SENDING_FREQUENCE", "* 7-20 * * 1-6"), send_data)],
        ),
    }
    # Setup all links
    FlowLink().entrypoint(components["camera"], "frames").destination(
        components["streamer"], "frames"
    )

    running = True

    threads = [
        ThreadComponent(component.start()).begin()
        for component in thread_components.values()
    ]

    try:
        [component.start() for component in components.values()]
        [component.initiate() for component in components.values()]
        while running:
            [component.run() for component in components.values()]
            try:
                BUFFER_IMAGE = components["camera"].current_frame
            except IndexError:
                BUFFER_IMAGE = None
    except KeyboardInterrupt:
        running = False
        [component.stop() for component in components.values()]
        [thread.end() for thread in threads]

    [print(component._benchmarker.report()) for component in components.values()]

    print("Exiting the program......")

if __name__ == "__main__":
    main()
