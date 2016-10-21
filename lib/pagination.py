# coding=utf-8
import math
from urlparse import parse_qs


class Pagination(object):
    request = None

    p = 1
    n = 25
    pages = 1
    tot = 0

    has_previous = False
    prev_url = ''

    has_next = False
    next_url = ''

    quick_jump_url = ''

    def __init__(self, request, tot):
        self. request = request
        self.p = int(request.GET.get('p', 1))
        self.n = int(request.GET.get('n', 25))
        self.tot = tot
        self.pages = int(math.ceil(self.tot*1.0 / self.n))

        self._gen_paging()

    def _gen_paging(self):
        self._gen_prev_url()
        self._gen_next_url()
        self._gen_quick_jump_url()

    def _parse_url(self):
        urls = self.request.META.get('REQUEST_URI').split('?')
        if len(urls) >= 2:
            query_strings = parse_qs(urls[1])
        else:
            query_strings = {}
        query_strings['n'] = self.n
        query_strings['p'] = self.p

        curr_url_info = {}
        curr_url_info['query_strings'] = query_strings
        curr_url_info['url'] = urls[0]
        return curr_url_info

    def _join_url(self, url, query_string):
        new_query = []
        for q in query_string:
            if type(query_string[q]) is list:
                new_query.append("%s=%s" % (q, query_string[q][0]))
            else:
                new_query.append("%s=%s" % (q, query_string[q]))
        return url + '?' + "&".join(new_query)

    def _gen_prev_url(self):
        if self.p > 1:
            self.has_previous = True
            url = self._parse_url()
            url['query_strings']['p'] -= 1
            url['query_strings']['pageType'] = 'prev'
            self.prev_url = self._join_url(url['url'], url['query_strings'])

    def _gen_next_url(self):
        if self.tot and self.p != self.pages:
            self.has_next = True
            url = self._parse_url()
            url['query_strings']['p'] += 1
            url['query_strings']['pageType'] = 'next'
            self.next_url = self._join_url(url['url'], url['query_strings'])

    def _gen_quick_jump_url(self):
        self.quick_jump_url = self.request.META.get('REQUEST_URI')

