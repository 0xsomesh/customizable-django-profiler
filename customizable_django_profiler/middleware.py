import pstats
from datetime import datetime
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

    def __call__(self, request):
        if self.can(request):
            self.profiler = profile.Profile()
            self.profiler.enable()
        response = self.get_response(request)
        if self.can(request):
            if 'dump' in  settings.PROFILER.get('output', ['console']):
                file_location = settings.PROFILER.get('file_location', 'profile')
                file_name =  '{file_location}{timestamp::%Y%m%d%H%M%S%f}.prof'.format(
                    file_location=file_location,
                    timestamp=datetime.now())
                self.profiler.dump_stats(file_name)

            self.profiler.create_stats()
            out = StringIO()
            stats = pstats.Stats(self.profiler, stream=out)
            stats.sort_stats(settings.PROFILER.get('sort', 'time'))
            stats.print_stats(int(settings.PROFILER.get('count', 100)))
            result = out.getvalue()
            for output in settings.PROFILER.get('output', ['console']):
                if output == 'console':
                    print(result)
                if output == 'file':
                    file_location = settings.PROFILER.get(
                        'file_location', 'profile.txt')
                    print(file_location)
                    with open(file_location, "a+") as f:
                        f.write(result)
                if output == 'response':
                    response = HttpResponse(result,
                                            content_type='application/liquid')
        return response

    def can(self, request):
        if settings.PROFILER['activate']:
            if settings.PROFILER.get('trigger', 'all') == 'all':
                return True
            elif settings.PROFILER['trigger'].split(':')[1] in str(request):
                return True
            return False
