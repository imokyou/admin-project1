# coding=utf8
from ipware.ip import get_ip
import pygeoip
import re
from django.conf import settings


class SetLangMiddle(object):
    def process_request(self, request):
        if 'changelang' not in request.GET:
            if 'lang' not in request.session or not request.session['lang']:
                country = ''
                default_lang = ''
                gi = pygeoip.GeoIP('%s/%s' % (settings.DATA_PATH, 'GeoIP.dat'))
                ip = get_ip(request)
                if self.is_ipv4(ip) is True:
                    country = gi.country_name_by_addr(ip)
                else:
                    country = gi.country_name_by_name(ip)
                if country.lower() == 'china':
                    default_lang = 'cn'
                else:
                    default_lang = 'en'
                lang = request.GET.get('lang', default_lang)
                request.session['lang'] = lang

    def is_ipv4(self, ip):
        match = re.match("^(\d{0,3})\.(\d{0,3})\.(\d{0,3})\.(\d{0,3})$", ip)
        if not match:
            return False
        quad = []
        for number in match.groups():
            quad.append(int(number))
        if quad[0] < 1:
            return False
        for number in quad:
            if number > 255 or number < 0:
                return False
        return True
