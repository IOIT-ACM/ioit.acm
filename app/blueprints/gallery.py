import os
from flask import Blueprint, render_template

gallery_bp = Blueprint("gallery", __name__, template_folder="../templates")


def generate_collections(static_path):
    """
    Generates a flat list of image file data from the app/static/gallery.

    :param static_path: The base path to the gallery folder.
    :return: A flat list of image file data with "name" and "desc".
    """
    collections = []

    if not os.path.exists(static_path):
        return collections

    for folder_name in os.listdir(static_path):
        folder_path = os.path.join(static_path, folder_name)

        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith((".jpeg", ".jpg", ".png")):
                    file_path = "{}/{}".format(folder_name, file_name)
                    collections.append(
                        {
                            "name": file_path,
                            "desc": folder_name,
                        }
                    )

    return collections


@gallery_bp.route("/gallery")
def home():
    static_path = os.path.join(os.getcwd(), "app/static/img/gallery/")
    collections = generate_collections(static_path)
    return render_template("gallery.html", collections=collections)
