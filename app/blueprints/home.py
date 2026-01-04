# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from app.data.events import events
from app.data.stories import stories
from flask import redirect, url_for

# Define the blueprint
home_bp = Blueprint("home", __name__, template_folder="../templates")

images = [
    "https://ioit.acm.org/tenet/mun/2024/1.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/2.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/3.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/4.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/5.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/6.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/7.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/8.jpeg",
]
images_2 = [
    "https://ioit.acm.org/tenet/mun/2024/9.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/10.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/11.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/12.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/13.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/14.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/15.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/16.jpeg",
]


@home_bp.route("/")
def home():
    return render_template(
        "home.html",
        events=events[:6],
        images=images,
        images_2=images_2,
        stories=stories[:4],
    )


@home_bp.route("/calendar")
def calender():
    return render_template(
        "calender.html",
    )


@home_bp.route("/cal")
def calender_redirect():
    return redirect(url_for("home.calender"))


@home_bp.route("/services")
def services():
    projects = [
        {
            "title": "ManWithIndies",
            "subtitle": "Wildlife Rescue Portal",
            "description": "End-to-end digital portal replacing manual paper-based wildlife rescue reporting. Supports GPS tracking and workflow digitization.",
            "image": "wildlife_rescue.jpeg",
            "link": "https://manwithindies-form.vercel.app/",
        },
        {
            "title": "Bit-by-Mail",
            "subtitle": "Bulk Mailing System",
            "description": "Self-hosted bulk mailing application with a modern UI. Features live previews, preflight configuration checks, and real-time logging.",
            "image": "bit_by_mail.jpeg",
            "link": "https://pypi.org/project/bit-by-mail/",
        },
        {
            "title": "Tenet Hack 2025",
            "subtitle": "Hackathon Management Platform",
            "description": "Official portal for the flagship Tenet Hackathon, featuring registration workflows and event information built with Next.js.",
            "image": "tenet_hack_2025.jpeg",
            "link": "https://hack.ioittenet.com/",
        },
        {
            "title": "IOIT ACM ChapterOS",
            "subtitle": "Organizational CRM & Dashboard",
            "description": "Central management hub for internal operations, handling recruitment data, event planning, and documentation for the student chapter.",
            "image": "chapter_os.jpeg",
            "link": "https://os.ioit.acm.org/",
        },
        {
            "title": "Mamata Andh",
            "subtitle": "Anath Kalyan Kendra",
            "description": "Platform for managing resources and donations for blind individuals, focusing on food and waste management support.",
            "image": "mamata_andh_anath_kalyan_kendra.jpeg",
            "link": "https://mamatha-andh.vercel.app",
        },
        {
            "title": "Sarvasparshi Foundation",
            "subtitle": "Social Welfare Platform",
            "description": "Comprehensive platform supporting healthcare, education, and disaster relief initiatives.",
            "image": "sarvasparshi_foundation.jpeg",
            "link": "https://ioit-acm.github.io/sarvasparshi-foundation/",
        },
        {
            "title": "Vasantdada Patil School",
            "subtitle": "Educational Platform",
            "description": "Dynamic educational website showcasing modern facilities and holistic student development programs.",
            "image": "dr_vasantdada_patil_school.jpeg",
            "link": "https://maji-sainik-sikshan-git-main-akashmajis-projects.vercel.app/#/",
        },
        {
            "title": "TENET 2024",
            "subtitle": "Event Platform",
            "description": "Event website that attracted over 15,000 visitors, featuring interactive WebGL experiences.",
            "image": "tenet_2024.jpeg",
            "link": "https://www.ioittenet.com/",
        },
        {
            "title": "IOIT MUN",
            "subtitle": "Academic Simulation",
            "description": "Academic simulation platform for Model United Nations, enabling diplomacy training.",
            "image": "ioit_mun.jpeg",
            "link": "https://www.ioitmun.com/",
        },
        {
            "title": "Bit By Query",
            "subtitle": "SQL Competition Platform",
            "description": "Platform for hosting and judging SQL competitions with real-time evaluation.",
            "image": "bbq.jpeg",
            "link": "https://bit-by-query.onrender.com/",
        },
        {
            "title": "Heads Up",
            "subtitle": "Mobile Game",
            "description": "Flutter-based mobile word-guessing game where players collaborate in real time.",
            "image": "headsup.jpeg",
            "link": "https://github.com/adimail/headsup",
        },
    ]

    return render_template("services.html", projects=projects)
