import sys
import cProfile
import pstats
import io
from django.conf import settings



class ProfileMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if settings.DEBUG:
            print('yo')
            self.profiler.create_stats()
            out = io.StringIO()
            stats = pstats.Stats(self.profiler, stream=out)
            stats.sort_stats('time').print_stats(.2)
            print(out.getvalue())
        return response

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if settings.DEBUG:
            self.profiler = cProfile.Profile()
            args = (request,) + callback_args
            print("hello")
            return self.profiler.runcall(callback, *args, **callback_kwargs)
