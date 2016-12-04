# coding=utf8
import traceback
import random
from django.core.management.base import BaseCommand
from dbmodel.ziben.models import Statics


class Command(BaseCommand):
    '''更新首页左上角展示的数据
    '''
    def handle(self, *args, **kwargs):
        try:
            stat = Statics.objects.order_by('-id').first()
            stat.online = random.randint(50, 200)
            stat.save()
        except:
            traceback.print_exc()
        finally:
            print 'Script Run Over'
