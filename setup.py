from distutils.core import setup

setup(
        name='customizable_django_profiler',
        version='0.1',
        url='https://github.com/someshchaturvedi/customizable-django-profiler',
        description='Django middleware based on cProfile',
        author='Somesh Chaturvedi',
        author_email='somesh.08.96@gmail.com',
        license='MIT',
        packages=['customizable-django-profiler'],
        keywords = ['django','middleware','cProfile', 'Profile'],
        zip_safe=False,
        download_url = 'https://github.com/someshchaturvedi/customizable-django-profiler/archive/0.1.tar.gz'
      )
