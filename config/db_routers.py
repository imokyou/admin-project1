# -*- coding: utf-8 -*-
# db_router, 用于django多数据库


class Router(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        # if model.__module__.startswith('dbmodel.youmi'):
        #     return 'youmi'
        # if model.__module__.startswith('dbmodel.admin'):
        #     return 'youmi_admin'
        # if model.__name__ in ('User'):
        #     return 'default'
        # return None
        return 'default'

    def db_for_write(self, model, **hints):
        # if model.__module__.startswith('dbmodel.youmi'):
        #     return 'youmi'
        # if model.__module__.startswith('dbmodel.admin'):
        #     return 'youmi_admin'
        # if model.__name__ in ('User'):
        #     return 'default'
        # return None
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        db_list = ('default',)
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        # if app_label == 'dbmodel.youmi':
        #     return db == 'youmi'
        # elif app_label == 'dbmodel.admin':
        #     return db == 'youmi_admin'
        # else:
        #     return db == 'default'
        return db == 'default'
