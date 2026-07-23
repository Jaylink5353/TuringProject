import cv2
from flask import Flask, Response, render_template, stream_with_context


class CamServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.cap = cv2.VideoCapture(0)
        self._register_routes()

    def run(self, host="0.0.0.0", port=5000, **kwargs):
        self.app.run(host=host, port=port, **kwargs)

    def _register_routes(self):
        self.app.add_url_rule("/", view_func=self.index)
        self.app.add_url_rule("/video_feed", view_func=self.video_feed)
        self.app.add_url_rule("/shutdown", view_func=self.shutdown, methods=["POST"])

    def gen_frames(self):
        while True:
            success, frame = self.cap.read()
            if not success:
                break

            ret, buffer = cv2.imencode(".jpg", frame)
            if not ret:
                continue

            frame_bytes = buffer.tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )

    def video_feed(self):
        return Response(
            stream_with_context(self.gen_frames()),
            mimetype="multipart/x-mixed-replace; boundary=frame",
        )

    def index(self):
        return render_template("index.html")

    def shutdown(self):
        self.cap.release()
        return "Capture released"


if __name__ == "__main__":
    server = CamServer()
    server.app.run(host="0.0.0.0", port=5000)

