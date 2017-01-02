# coding=utf8
import traceback
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from dbmodel.ziben.models import UserOrderSell, CBCDPriceLog


class Command(BaseCommand):
    '''封盘'''
    def handle(self, *args, **kwargs):
        try:
            current_order = UserOrderSell.objects \
                .filter(status=0).order_by('id').first()

            try:
                pricelog = CBCDPriceLog.objects \
                    .filter(closing_date__startswith=timezone.now().date()).first()
                pricelog.price = float(current_order.price)
            except:
                pricelog = CBCDPriceLog(
                    price=float(current_order.price),
                    closing_date=timezone.now()
                )
            pricelog.save()
        except:
            traceback.print_exc()
        finally:
            print 'Script Run Over'
