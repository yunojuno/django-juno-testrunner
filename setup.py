import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-juno-testrunner',
    version='0.2.6',
    description='A more useful (and slightly more glamorous) test runner for Django 1.6+ from the folks at YunoJuno',
    long_description=README,
    author='Steve Jalim, Hugo Rodger-Brown',
    author_email='steve@somefantastic.co.uk, hugo@yunojuno.com',
    url='https://github.com/yunojuno/django-juno-testrunner.git',
    license='MIT',
    packages=['junorunner'],
    install_requires=['colorama'],
    extras_require={'junorunner': ['colorama', ]},
    classifiers=[
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License', # example license
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            # replace these appropriately if you are using Python 3
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ]
)
