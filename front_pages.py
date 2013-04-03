#coding: utf-8
import datetime
import urllib
from flask import render_template, request, session, make_response, redirect
from models.project import table, col
from models.orm import User, Project, Template
from zp_tools import rdm_code, hash_pwd, json_res, is_name, str2bool
from zp_web import app, get_db
from zp_tools import s_user, s_project
from zp_types import types_map

__author__ = 'cloudbeer'


@app.route("/")
def pg_index():
    return render_template("index.html", user=s_user())


@app.route("/projects/")
def pg_projects():
    return render_template("projects.html", projects=None, user=s_user())


@app.route("/project/")
def pg_project():
    user = s_user()
    if user:
        project = s_project()
        sql_types = None
        db = project.db
        if db in types_map:
            sql_types = types_map[db]['sql']
        return render_template("project.html", project=project, user=s_user(), types_map=types_map, sql_types=sql_types)
    else:
        return redirect('/account/login/?' + urllib.urlencode({'back': request.path}))


@app.route("/project/<int:id>/")
def pg_my_project(id):
    return "i love ..." + str(id)
    import yaml

    content = ""
    project = yaml.load(content)
    session['project'] = project
    db = project.db
    sql_types = None
    if db in types_map:
        sql_types = types_map[db]['sql']
    return render_template("project.html", project=project, user=s_user(), types_map=types_map, sql_types=sql_types)


@app.route("/project/save/", methods=['post'])
def pg_project_save():
    title = request.form["title"]
    content = request.form["content"]
    db = request.form["db"]
    project = s_project()
    project.title = title
    project.content = content
    project.db = db
    session['project'] = project
    return json_res(True).str()


@app.route("/project/save2db/", methods=['post', 'get'])
def pg_project_save_to_db():
    project = s_project()
    user = s_user()
    import yaml
    content = yaml.dump(project)
    m_project = Project(title=project.title, content=content, user_id=user)
    db = get_db()
    db.add(m_project)
    db.commit()
    project.dbid = m_project.id
    session['project'] = project
    return json_res(True).str()


@app.route("/project/get_project/", methods=['post', 'get'])
def pg_project_get():
    project = s_project()
    res = json_res(True)
    res.title = project.title
    res.content = project.content
    res.db = project.db
    return res.str()


@app.route("/project/save_table/", methods=['post', 'get'])
def pg_table_save():
    name = request.form["name"]
    if not is_name(name):
        return json_res(False, message='Invalid name, must begin with letter and no blank.').str()

    ref_name = request.form["ref_name"]
    title = request.form["title"]
    content = request.form["content"]
    act = request.form['act']
    project = s_project()
    xtable = None

    if act == 'create':
        yy_tables = [mmtable for mmtable in project.tables if mmtable.name == name]
        if yy_tables is not None and len(yy_tables) > 0:
            return json_res(False, message='Table name must be unique. Change it please.').str()
        xtable = table() #name=name, title=title, content=content)
        project.tables.append(xtable)
    elif act == 'modi':
        yy_tables = [mmtable for mmtable in project.tables if mmtable.name == ref_name]
        if yy_tables is not None and len(yy_tables) == 1:
            xtable = yy_tables[0]
    xtable.name = name
    xtable.title = title
    xtable.content = content
    session["project"] = project
    res = json_res(True)
    return res.str()


@app.route("/project/get_table/", methods=['post', 'get'])
def pg_table_get():
    flag = request.form["flag"]
    project = s_project()
    yy_tables = [mmtable for mmtable in project.tables if mmtable.name == flag]
    xtable = None
    if yy_tables is not None and len(yy_tables) == 1:
        xtable = yy_tables[0]
    if xtable is None:
        return json_res(False, message='Table not found.').str()
    res = json_res(True)
    res.name = xtable.name
    res.title = xtable.title
    res.content = xtable.content
    return res.str()


@app.route("/project/save_col/", methods=['post'])
def pg_col_save():
    name = request.form["name"]
    if not is_name(name):
        return json_res(False, message='Invalid name, must begin with letter and no blank.').str()

    table_name = request.form['table']
    sql_type = request.form['sql_type']
    is_pk = request.form['is_pk']
    is_null = request.form['is_null']
    is_unique = request.form['is_unique']
    is_index = request.form['is_index']
    auto_incres = request.form['auto_incres']
    init_val = request.form['init_val']
    ref_name = request.form["ref_name"]
    title = request.form["title"]
    content = request.form["content"]
    act = request.form['act']
    project = s_project()

    xtable = None
    yy_tables = [mmtable for mmtable in project.tables if mmtable.name == table_name]
    if yy_tables is not None and len(yy_tables) == 1:
        xtable = yy_tables[0]
    else:
        return json_res(False, message='Table not found.').str()
    xcol = None
    if act == 'create':
        yy_cols = [mmcol for mmcol in xtable.cols if mmcol.name == name]
        if yy_cols is not None and len(yy_cols) > 0:
            return json_res(False, message='Col name must be unique. Change it please.').str()
        xcol = col()
        xtable.cols.append(xcol)
    elif act == 'modi':
        yy_cols = [mmcol for mmcol in xtable.cols if mmcol.name == ref_name]
        if yy_cols is not None and len(yy_cols) == 1:
            xcol = yy_cols[0]
    xcol.name = name
    xcol.title = title
    xcol.content = content
    xcol.auto_incres = str2bool(auto_incres)
    xcol.is_index = str2bool(is_index)
    xcol.is_null = str2bool(is_null)
    xcol.is_pk = str2bool(is_pk)
    xcol.is_unique = str2bool(is_unique)
    xcol.sql_type = sql_type
    xcol.init_val = init_val
    session["project"] = project
    res = json_res(True)
    return res.str()


@app.route("/account/reg/")
def pg_reg():
    return render_template("reg.html")


@app.route("/account/save_reg/", methods=['post'])
def pg_reg_save():
    email = request.form["email"]
    if not check_email(email):
        return json_res(state=False, message="Email is registered, please change.").str()

    password = request.form["password"]
    nick = request.form["nick"]
    salt = rdm_code(16)
    password = hash_pwd(password, salt)
    m_user = User(email=email, nick=nick, password=password, salt=salt)
    db = get_db()
    db.add(m_user)
    db.commit()
    return json_res(state=True).str()


@app.route("/account/valid_email/", methods=['post'])
def pg_reg_check_email():
    email = request.form["email"]
    db = get_db()
    m_user = db.query(User).filter(User.email == email).first()
    if m_user is not None:
        return "false"
    else:
        return "true"


def check_email(email):
    db = get_db()
    m_user = db.query(User).filter(User.email == email).first()
    return m_user is None


@app.route("/account/login/")
def pg_login():
    back = request.args.get('back','')
    if not back:
        back = '/'
    return render_template("login.html", back=back)


@app.route("/account/logout/")
def pg_logout():
    response = make_response(redirect("/"))
    if 'user' in session:
        del session['user']
    if 'email' in request.cookies:
        response.set_cookie("email", "", max_age=-1)
        response.set_cookie("emailtoken", "", max_age=-1)
    return response


@app.route("/account/login/", methods=["post"])
def pg_login_post():
    db = get_db()
    email = request.form["email"]
    m_user = db.query(User).filter(User.email == email).first()
    if m_user is None:
        return json_res(False, message="This email is not registered.").str()
    pwd = m_user.password
    salt = m_user.salt
    p_pwd = request.form["password"]
    if hash_pwd(p_pwd, salt) != pwd:
        return json_res(False, message="Password is wrong.").str()

    session['user'] = m_user
    response = make_response(json_res(True).str())
    max_age = 60 * 60 * 24 * 14
    response.set_cookie("email", email, max_age=max_age)
    response.set_cookie("emailtoken", hash_pwd('email', salt), max_age=max_age)
    return response


@app.route("/project/sql_types/", methods=["post"])
def pg_sql_types():
    db = request.form["db"]
    res = json_res(True)
    if db in types_map:
        xdb = types_map[db]["sql"]
        res.sql_types = xdb
    return res.str()


@app.route("/t/")
def test():
    response = make_response('test')
    return response