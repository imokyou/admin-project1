# coding=utf8
import pygeoip
import re


def is_ipv4(ip):
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

if __name__ == '__main__':
    ip = '183.63.164.154'
    gi = pygeoip.GeoIP('./GeoIP.dat')
    if is_ipv4(ip) is True:
        print gi.country_name_by_addr(ip)
    else:
        print gi.country_name_by_name(ip)
