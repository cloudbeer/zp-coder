from flask import Flask, session, request, Blueprint, _app_ctx_stack
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE = 'postgresql+psycopg2://postgres:zhwell@localhost:5432/zp_coder'
DEBUG = True
SECRET_KEY = 'ihaveadream'
USERNAME = 'admin'
PASSWORD = 'coocaa'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'zpcoder_db'):
        engine = create_engine(app.config["DATABASE"])
        Database = sessionmaker(bind=engine)
        top.zpcoder_db = Database()
    return top.zpcoder_db


@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'zpcoder_db'):
        top.zpcoder_db.close()


# app.secret_key = "ihaveadream"
# app.debug = True

static_js = Blueprint('static_js', __name__, static_folder='js')
static_css = Blueprint('static_css', __name__, static_folder='css')
static_bootstrap = Blueprint('static_bootstrap', __name__, static_folder='bootstrap')


app.register_blueprint(static_js)
app.register_blueprint(static_css)
app.register_blueprint(static_bootstrap)




# from models.orm import *
#
#
#
# db = get_db()
#
# p = Project()
# p.title = '''I'm have a "dream".'''
# db.add(p)
# db.commit()






# sv_js = Blueprint('sv_js', __name__, static_folder='js')

# template = Template("""class  {{ name }}:
# {% for i in range(10): %}
#     I have a dream.
# {%endfor%}""")
#
# print template.render(name="Cloudbeer")


# @app.route('/')
# def hello_world():
#
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     app.run()
