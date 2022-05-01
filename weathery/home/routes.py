# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import redirect, render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from weathery.home.weather import Forecast, WeatherAPI

from weathery.home import blueprint


@blueprint.route("/index")
@login_required
def index():

    return redirect("/dashboard")
    # return render_template("home/dashboard.html", segment="dashboard")


@blueprint.route("/dashboard")
@login_required
def dashboard():

    forecast: Forecast = WeatherAPI("Tunbridge Wells").get_forecast()
    return render_template(
        "home/dashboard.html", segment="dashboard", forecast=forecast
    )


@blueprint.route("/<template>")
@login_required
def route_template(template):

    try:

        if not template.endswith(".html"):
            template += ".html"

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template("home/page-404.html"), 404

    except:
        return render_template("home/page-500.html"), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split("/")[-1]

        if segment == "":
            segment = "index"

        return segment

    except:
        return None
