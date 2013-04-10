# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, request, redirect
from models.orm import Template, User
from zp_tools import s_user, login_required, login_required_ajax
from zp_web import app, get_db


@app.route("/templates/")
@login_required
def pg_templates():
    user = s_user()
    db = get_db()
    templates = db.query(Template).filter(User.id == user.id)
    return render_template("templates.html", templates=templates, user=s_user())


@app.route("/template/", methods=['get'])
@login_required
def pg_template():
    return render_template("template.html", user=s_user())


@app.route("/template/", methods=['post'])
@login_required
def pg_template_save():
    title = request.form["title"]
    content = request.form["content"]
    user = s_user()
    c_temp = Template(title=title, content=content, create_date=datetime.now(), user_id=user.id)
    db = get_db()
    db.add(c_temp)
    db.commit()
    return redirect("/templates/")


@app.route("/template/<int:id>/")
@login_required
def pg_my_template(id):
    return render_template("template.html", user=s_user())


@app.route("/template/share/")
@login_required
def pg_template_share():
    return "share"