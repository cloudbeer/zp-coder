#coding: utf-8
__author__ = 'cloudbeer'

types_map = dict(
    common={
        "sql": (
            'int', 'varchar', 'decimal', 'text', 'datetime', 'numeric',),
        "python": (),
        "php": (),
        "c++": (),
        "c#": ('int','string', 'decimal','string', 'Date', 'float'),
        "java": ('int','String', 'decimal','String', 'Date', 'float')
    },
    postgres={
        "sql": (
            'integer', 'bigint', 'varchar', 'decimal', 'text', 'smallint', 'numeric', 'real', 'double precision',
            'smallserial', 'serial', 'bigserial', 'money', 'char', 'bytea', 'timestamp', 'timestamp with time zone',
            'date', 'time', 'time with zone', 'interval', 'boolean', 'point', 'line', 'lseg', 'box', 'path', 'polygon',
            'circle', 'cidr', 'inet', 'macaddr', 'uuid',),
        "python": (),
        "php": (),
        "c++": (),
        "c#": (),
        "java": ()
    }, mysql={
        "sql": (),
        "python": (),
        "php": (),
        "c++": (),
        "c#": (),
        "java": ()
    }, sqlserver={
        "sql": (),
        "python": (),
        "php": (),
        "c++": (),
        "c#": (),
        "java": ()
    }, oracle={
        "sql": (),
        "python": (),
        "php": (),
        "c++": (),
        "c#": (),
        "java": ()
    })