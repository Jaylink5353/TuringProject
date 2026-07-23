# Webcam Stream Flask Application

## Table of Contents
- [Webcam Stream Flask Application](#webcam-stream-flask-application)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Code Explanation](#code-explanation)
  - [Troubleshooting](#troubleshooting)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction

This project is a Flask-based web application that streams webcam video to a web browser. It captures video from the default camera of the system and displays it in real-time on a web page.

## Requirements

The project requires Python and several Python packages. The full list of requirements can be found in the `requirements.txt` file. Key requirements include:

- Flask
- OpenCV (cv2)
- numpy

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/ibrahimmansur4/Server.git
   
   cd Server/Stream\ Video\ Flask/
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. You should see the webcam stream on the page.

4. To stop the server, press CTRL+C in the terminal where the server is running.

## Code Explanation

The main application code is in `app.py`. Here's a breakdown of its key components:

```python
cap = cv2.VideoCapture(0)  # Global video capture

def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
```

This function `gen_frames()` continuously captures frames from the webcam, encodes them as JPEG, and yields them as bytes. This is used to create a continuous stream of images.

```python
@app.route('/video_feed')
def video_feed():
    return Response(stream_with_context(gen_frames()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
```

This route sends the video stream to the client. It uses `stream_with_context` to ensure the stream is properly managed by Flask.

```python
@app.route('/')
def index():
    return render_template('index.html')
```

This route renders the main page where the video stream is displayed.

```python
@app.route('/shutdown', methods=['POST'])
def shutdown():
    global cap
    cap.release()  # Release the video capture
    return "Capture released"
```

This route provides a way to properly release the video capture when shutting down the application.

## Troubleshooting

If you encounter issues:

1. Ensure your webcam is properly connected and not in use by another application.
2. Check that you have the necessary permissions to access the webcam.
3. If you're accessing from another device on the network, ensure your firewall isn't blocking the connection.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
