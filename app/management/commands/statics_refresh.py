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
            stat.members = stat.members + random.randint(10, 50)
            stat.hits = float(stat.hits) + random.randint(500, 1000)
            stat.save()
        except:
            traceback.print_exc()
        finally:
            print 'Script Run Over'
