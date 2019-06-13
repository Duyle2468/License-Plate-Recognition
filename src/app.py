import os

from flask import Flask, request, render_template, send_from_directory

__author__ = 'duyle'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

filenameforall = ""


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    IMAGE_FOLDER = os.path.join('static/images')
    app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
    target = os.path.join(APP_ROOT, 'static/images')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
        filenameforall = full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete.html", image_name=filename, user_image=full_filename, root=APP_ROOT)


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/gallery')
def get_gallery():
    image_names = os.path.join(filenameforall)
    print(image_names)
    return render_template("gallery.html", image_names=image_names)




if __name__ == "__main__":
    app.run(port=4555, debug=True)
