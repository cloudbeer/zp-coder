#coding: utf-8
import json

__author__ = 'cloudbeer'


class project:
    def __init__(self, dbid=0, name=None, title=None, content=None, db=None, tables=None):
        """
        初始化项目
        :param name: 名称
        :param title: 标题
        :param tables: 包含的表
        """
        self.dbid = dbid
        self.name = name
        if title is None:
            title = "Untitle"
        self.title = title
        if db is None:
            db = "postgres"
        self.db = db
        if tables is not None:
            self.tables = tables
        else:
            self.tables = []
        self.content = content

    def __repr__(self):
        return json.dumps(self.__dict__)


class table:
    def __init__(self, name=None, title=None, content=None, cols=None):
        """
        初始化表
        :param name:
        :param title:
        :param cols:
        """
        self.name = name
        self.title = title
        if cols is not None:
            self.cols = cols
        else:
            self.cols = []
        self.content = content

    def __repr__(self):
        return json.dumps(self.__dict__)


class col:
    def __init__(self, name=None, py_type=None, sql_type=None, title=None, content=None, length=0, init_val=None,
                 auto_incres=False, is_pk=False, is_null=False, is_index=False, is_unique=False, fk_table=None,
                 fk_col=None, fk_col_show=None):
        """
        初始化列
        :param content:
        :param name:
        :param py_type:
        :param sql_type:
        :param title:
        :param length:
        :param init_val:
        :param auto_incres:
        :param is_pk:
        :param is_null:
        :param is_index:
        :param is_unique:
        :param fk_table:
        :param fk_col:
        :param fk_col_show:
        """
        self.name = name
        self.title = title
        self.py_type = py_type
        self.sql_type = sql_type
        self.length = length
        self.is_pk = is_pk
        self.fk_col_show = fk_col_show
        self.fk_col = fk_col
        self.fk_table = fk_table
        self.is_unique = is_unique
        self.is_index = is_index
        self.is_null = is_null
        self.auto_incres = auto_incres
        self.init_val = init_val
        self.describ = content

    def __repr__(self):
        return json.dumps(self.__dict__)