from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from picamera2 import Picamera2
from typing import Annotated
from auth import oauth2_scheme
import io
import time

router = APIRouter(prefix="/api", tags=["camera"])

picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size": (1920, 1080)})
picam2.configure(config)
picam2.start()

def mjpeg_stream():
    while True:
        stream = io.BytesIO()
        picam2.capture_file(stream, format="jpeg")
        jpg = stream.getvalue()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + jpg + b"\r\n"
        )

        time.sleep(0.05)

@router.get("/stream")
def stream(_token: Annotated[str, Depends(oauth2_scheme)]):
    return StreamingResponse(
        mjpeg_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
