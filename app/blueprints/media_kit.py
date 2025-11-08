from flask import Blueprint, render_template, url_for
from collections import OrderedDict

media_kit_bp = Blueprint(
    "media_kit", __name__, template_folder="../templates", static_folder="../static"
)

BRAND_KITS = OrderedDict(
    [
        (
            "acm",
            {
                "name": "ACM Student Chapter",
                "title": "Logo",
                "download_link": "static/mediakit/mediakit.zip",
                "logos": [
                    {
                        "src": "static/mediakit/acm-logo-colour.png",
                        "alt": "ACM Logo Colour",
                        "download": "acm-logo-colour.png",
                        "class": "bg-white",
                    },
                    {
                        "src": "static/mediakit/acm-logo-dark.png",
                        "alt": "ACM Logo Dark",
                        "download": "acm-logo-dark.png",
                        "class": "bg-white",
                    },
                    {
                        "src": "static/mediakit/acm-logo-light.png",
                        "alt": "ACM Logo Light",
                        "download": "acm-logo-light.png",
                        "class": "dark",
                    },
                    {
                        "src": "static/mediakit/college-logo-full.png",
                        "alt": "College Logo Full",
                        "download": "college-logo-full.png",
                        "class": "bg-white",
                    },
                    {
                        "src": "static/mediakit/college-logo-half.png",
                        "alt": "College Logo Half",
                        "download": "college-logo-half.png",
                        "class": "bg-white",
                    },
                ],
                "colors": [
                    {
                        "name": "Sea",
                        "hex": "#4DA2FF",
                        "style": "background-color: #4DA2FF; color: white;",
                        "class": "md:col-span-2",
                    },
                    {
                        "name": "Ocean",
                        "hex": "#011829",
                        "style": "background-color: #011829; color: white;",
                    },
                    {
                        "name": "Aqua",
                        "hex": "#C0E6FF",
                        "style": "background-color: #C0E6FF; color: black;",
                    },
                ],
                "typeface": {
                    "name": "Inter",
                    "sample_text": "Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm Nn Oo Pp Qq Rr Ss Tt Uu Vv Ww Xx Yy Zz",
                    "class": "",
                },
            },
        ),
        (
            "tenet",
            {
                "name": "IOIT TENET",
                "title": "TENET'25",
                "logos": [
                    {
                        "src": "static/mediakit/tenet-logo-blue.png",
                        "alt": "TENET Logo Blue",
                        "download": "tenet-logo-blue.png",
                        "class": "bg-white",
                    },
                    {
                        "src": "static/mediakit/tenet-white-logo.png",
                        "alt": "TENET Logo White",
                        "download": "tenet-white-logo.png",
                        "class": "dark",
                    },
                    {
                        "src": "static/mediakit/tenet-icon-blue.png",
                        "alt": "TENET Icon Blue",
                        "download": "tenet-icon-blue.png",
                        "class": "bg-white",
                    },
                    {
                        "src": "static/mediakit/tenet-icon-white.png",
                        "alt": "TENET Icon White",
                        "download": "tenet-icon-white.png",
                        "class": "dark",
                    },
                ],
                "colors": [
                    {
                        "name": "Midnight Blue",
                        "hex": "#0A192F",
                        "style": "background-color: #0A192F; color: white;",
                        "class": "md:col-span-2",
                    },
                    {
                        "name": "Cyber Mint",
                        "hex": "#64FFDA",
                        "style": "background-color: #64FFDA; color: black;",
                    },
                    {
                        "name": "Light Slate",
                        "hex": "#CCD6F6",
                        "style": "background-color: #CCD6F6; color: black;",
                    },
                ],
                "typeface": {
                    "name": "Montserrat",
                    "sample_text": "Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm Nn Oo Pp Qq Rr Ss Tt Uu Vv Ww Xx Yy Zz",
                    "class": "font-montserrat",
                },
            },
        ),
        (
            "mun",
            {
                "name": "IOIT MUN",
                "title": "IOIT MUN'25",
                "logos": [
                    {
                        "src": "static/mediakit/mun-logo-blue.png",
                        "alt": "MUN Logo Blue",
                        "download": "mun-logo-blue.png",
                        "class": "bg-white",
                    },
                    {
                        "src": "static/mediakit/mun-logo-white.png",
                        "alt": "MUN Logo White",
                        "download": "mun-logo-white.png",
                        "class": "dark",
                    },
                    {
                        "src": "static/mediakit/mun-icon-blue.png",
                        "alt": "MUN Icon Blue",
                        "download": "mun-icon-blue.png",
                        "class": "bg-white",
                    },
                    {
                        "src": "static/mediakit/mun-icon-white.png",
                        "alt": "MUN Icon White",
                        "download": "mun-icon-white.png",
                        "class": "dark",
                    },
                    {
                        "src": "static/mediakit/unsc-icon-white.png",
                        "alt": "UNSC Icon White",
                        "download": "unsc-icon-white.png",
                        "class": "dark",
                    },
                    {
                        "src": "static/mediakit/uncsw-icon-white.png",
                        "alt": "UNCSW Icon White",
                        "download": "uncsw-icon-white.png",
                        "class": "dark",
                    },
                    {
                        "src": "static/mediakit/unhrc-icon-white.png",
                        "alt": "UNHRC Icon White",
                        "download": "unhrc-icon-white.png",
                        "class": "dark",
                    },
                    {
                        "src": "static/mediakit/aippm-icon-white.png",
                        "alt": "AIPPM Icon White",
                        "download": "aippm-icon-white.png",
                        "class": "dark",
                    },
                    {
                        "src": "static/mediakit/wto-icon-white.png",
                        "alt": "WTO Icon White",
                        "download": "wto-icon-white.png",
                        "class": "dark",
                    },
                    {
                        "src": "static/mediakit/ip-icon-white.png",
                        "alt": "IP Icon White",
                        "download": "ip-icon-white.png",
                        "class": "dark",
                    },
                ],
                "colors": [
                    {
                        "name": "Diplomatic Blue",
                        "hex": "#00205B",
                        "style": "background-color: #00205B; color: white;",
                        "class": "md:col-span-2",
                    },
                    {
                        "name": "Prestige Gold",
                        "hex": "#D4AF37",
                        "style": "background-color: #D4AF37; color: black;",
                    },
                    {
                        "name": "Parchment",
                        "hex": "#F5F5F5",
                        "style": "background-color: #F5F5F5; color: black;",
                    },
                ],
                "typeface": {
                    "name": "Lora",
                    "sample_text": "Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm Nn Oo Pp Qq Rr Ss Tt Uu Vv Ww Xx Yy Zz",
                    "class": "font-lora",
                },
            },
        ),
    ]
)


@media_kit_bp.route("/mediakit")
def media_kit():
    return render_template("media_kit.html", brand_kits=BRAND_KITS)
