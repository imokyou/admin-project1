# -*- coding: utf-8 -*-
# db_router, 用于django多数据库


class Router(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        if model.__module__.startswith('dbmodel.ziben'):
            return 'zibenguodu'
        if model.__name__ in ('User'):
            return 'zibenguodu'
        return 'default'

    def db_for_write(self, model, **hints):
        if model.__module__.startswith('dbmodel.ziben'):
            return 'zibenguodu'
        if model.__name__ in ('User'):
            return 'zibenguodu'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        db_list = ('zibenguodu', 'default')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return 'default'

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label == 'dbmodel.ziben':
            return db == 'zibenguodu'
        else:
            return db == 'default'
