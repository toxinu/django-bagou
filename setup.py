# -*- coding: utf-8 -*-
import re
import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def get_version():
    VERSIONFILE = 'bagou/__init__.py'
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (VERSIONFILE,))

setup(
    name='django-bagou',
    version=get_version(),
    packages=['bagou'],
    include_package_data=True,
    license='MIT License',
    description='Django Websocket for Django',
    long_description=README,
    url='https://github.com/toxinu/django-bagou',
    author='toxinu',
    author_email='toxinu@gmail.com',
    install_requires=['tornado==3.1.1', 'pika==0.9.13'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
