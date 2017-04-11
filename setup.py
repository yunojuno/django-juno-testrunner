from __future__ import unicode_literals
import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-juno-testrunner',
    version='0.4.2',
    description='Django (1.8+) test runner with added (colour) output.',
    long_description=README,
    author='YunoJuno',
    author_email='code@yunojuno.com',
    maintainer='YunoJuno',
    maintainer_email='code@yunojuno.com',
    url='https://github.com/yunojuno/django-juno-testrunner.git',
    license='MIT',
    packages=find_packages(),
    install_requires=['colorama'],
    extras_require={'junorunner': ['colorama', ]},
    classifiers=[
            'Environment :: Web Environment',
            'Framework :: Django',
            'Framework :: Django :: 1.8',
            'Framework :: Django :: 1.9',
            'Framework :: Django :: 1.10',
            'Framework :: Django :: 1.11',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
