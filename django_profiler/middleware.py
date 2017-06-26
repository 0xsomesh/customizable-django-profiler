import pstats

from django.conf import settings
from django.http import HttpResponse


try:
    import cProfile as profile
except ImportError:
    import profile
try:
    from cStringIO import StringIO
except:
    from io import StringIO


class cProfileMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.profiler = profile.Profile()

    def __call__(self, request):
        response = self.get_response(request)
        if self.can(request):
            self.profiler.create_stats()
            out = StringIO()
            stats = pstats.Stats(self.profiler, stream=out)
            stats.sort_stats(settings.PROFILER.get('sort', 'time'))
            stats.print_stats(int(settings.PROFILER.get('count', 50)))
            result = out.getvalue()
            for output in settings.PROFILER.get('output', ['console']):
                if output == 'console':
                    print(result)
                if output == 'file':
                    file_location = settings.PROFILER.get('file_location', 'prof.txt')
                    print(file_location)
                    with open(file_location,"a+") as f:
                        f.write(result)
                if output == 'response':
                    response = HttpResponse(result,
                                        content_type='application/liquid')
        return response

    def can(self ,request):
        if settings.DEBUG and settings.PROFILER['activate']:
            if settings.PROFILER.get('trigger', 'all') == 'all':
                return True
            elif settings.PROFILER['trigger'].split(':')[1] in request.GET:
                return True
            return False

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if self.can(request):
            args = (request,) + callback_args
            return self.profiler.runcall(callback, *args, **callback_kwargs)
