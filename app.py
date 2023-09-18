from flask import Flask
from flask import render_template
from flask import request
from utils import get_image_with_overlay
from pathlib import Path


app = Flask(__name__, static_folder="./static")


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/change_image", methods=["POST"])
def change_image():
    image_path = request.form.get("image_path")
    overlay_image = request.files.get("overlay_image")

    overlay_image_path = "overlay_image.jpg"
    overlay_image.save(overlay_image_path)

    new_image_path = get_image_with_overlay(image_path, overlay_image_path)

    file_to_rem = Path(overlay_image_path)
    Path.unlink(file_to_rem)
    return new_image_path


if __name__ == "__main__":
    app.run(debug=True)
