# coding=utf-8
import hashlib
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=64)

    def encryte_password(self):
        m = hashlib.md5()
        m.update(self.password)
        self.password = m.hexdigest()

    def save(self, *args, **kwargs):
        self.encryte_password()
        super(User).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'user'

