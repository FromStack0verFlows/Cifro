from flask import url_for, redirect, render_template, request
from application.model.GlobalApplicationModel import GlobalApplicationModel


def index():
    return redirect(url_for("dashboard.dashboard"))


def dashboard():
    model = GlobalApplicationModel()
    return render_template("index.html", model=model)

