import os
from flask import Blueprint, render_template, request, jsonify

gallery_bp = Blueprint("gallery", __name__, template_folder="../templates")

ITEMS_PER_PAGE = 30


def paginate_collections(collections, page, per_page):
    """
    Paginate a list of collections.

    :param collections: The complete list of collections.
    :param page: The current page number (1-based).
    :param per_page: Number of items per page.
    :return: A slice of the list for the current page.
    """
    start = (page - 1) * per_page
    end = start + per_page
    return collections[start:end]


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
    first_page_collections = paginate_collections(collections, 1, ITEMS_PER_PAGE)
    return render_template(
        "gallery.html", collections=first_page_collections, total=len(collections)
    )


@gallery_bp.route("/gallery/load-more", methods=["GET"])
def load_more():
    static_path = os.path.join(os.getcwd(), "app/static/img/gallery/")
    collections = generate_collections(static_path)
    page = int(request.args.get("page", 1))
    paginated_collections = paginate_collections(collections, page, ITEMS_PER_PAGE)
    return jsonify(paginated_collections)
