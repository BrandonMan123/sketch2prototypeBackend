from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import time
from flask_cors import CORS
import json
from hard_code import text_to_image_hardcode, image_to_3d_hardcode


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes and methods
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

with open("text2image.json") as f:
    sketch_to_text_json = json.load(f)


def sketch_to_text_mock(img):
    time.sleep(3)
    return f"lorem ipsum dolor jlksdjtopin wp4 asdlyfoweir hklsjdfhg kjlsdhkjsn dflkjsnfvlksdfjlkjdshglkjsdjhglksdhg ;ljdfhglksdglkjsdncvkldfnsgindsflhdfskj lhnsdfkjlvdsflkjnsdflk j sd.lknv lskdjn vdsfklnbutoewir tpoiseu gnk sdkm oipewrut"




@app.route("/sketch_to_text", methods=["POST"])
def sketch_to_text():
    data = request.json["data"]
    text = sketch_to_text_json[str(data)]
    return jsonify({"data" : text})

@app.route("/text_to_image", methods=["POST"])
def text_to_image():
    data = request.json["data"]
    print("Generating image...")
    assets = text_to_image_hardcode(data)
    return jsonify({"data" : assets})



@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("message")
def handle_message(data):
    print(data)
    assets = text_to_image_hardcode(data)
    socketio.emit('image', assets)

@app.route("/prototype", methods=["POST"])
def generate_3d():
    print ("received")
    image_ref = request.json["image_ref"]
    image_id = request.json["image_id"]
    return jsonify({"data" : image_to_3d_hardcode(image_ref, image_id)})



if __name__ == '__main__':
    socketio.run(app, debug=True)
