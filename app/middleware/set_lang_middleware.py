# coding=utf8


class SetLangMiddle(object):
    def process_request(self, request):
        if 'changelang' not in request.GET:
            if 'lang' not in request.session or not request.session['lang']:
                lang = request.GET.get('lang', 'cn')
                request.session['lang'] = lang
