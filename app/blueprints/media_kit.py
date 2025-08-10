from flask import Blueprint, render_template, url_for

media_kit_bp = Blueprint('media_kit', __name__, template_folder='../templates', static_folder='../static')

@media_kit_bp.route('/mediakit')
def media_kit():
    assets_data = [
        { 
            "title": "ACM Blue Logo", 
            "category": "Logo",
            "files": [
                { "format": "PNG", "url": url_for('static', filename='media/acm_logo_blue.png') },
                { "format": "JPG", "url": url_for('static', filename='media/acm_logo_blue.jpg') }
            ]
        },
        { 
            "title": "ACM White Logo", 
            "category": "Logo", 
            "files": [
                { "format": "PNG", "url": url_for('static', filename='media/acm_logo_white.png') },
                { "format": "JPG", "url": url_for('static', filename='media/acm_logo_white.jpg') }
            ]
        },
        { 
            "title": "College Logo", 
            "category": "Logo", 
            "files": [
                { "format": "PNG", "url": url_for('static', filename='media/college_logo.png') },
                { "format": "JPG", "url": url_for('static', filename='media/college_logo.jpg') }
            ]
        },
        { 
            "title": "Tenet Logo", 
            "category": "Logo",
            "files": [
                { "format": "PNG", "url": url_for('static', filename='media/tenet_logo.png') },
                { "format": "JPG", "url": url_for('static', filename='media/tenet_logo.jpg') }
            ]
        },
        { 
            "title": "MUN Logo", 
            "category": "Logo", 
            "files": [
                { "format": "PNG", "url": url_for('static', filename='media/mun_logo.png') },
                { "format": "JPG", "url": url_for('static', filename='media/mun_logo.jpg') }
            ]
        }
    ]

    categories = sorted(list(set(asset['category'] for asset in assets_data)))

    return render_template('media_kit.html', assets=assets_data, categories=categories)