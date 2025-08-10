from flask import Blueprint, render_template

media_kit_bp = Blueprint('media_kit', __name__, template_folder='../templates')

@media_kit_bp.route('/mediakit')
def media_kit():
    return render_template('media_kit.html')
