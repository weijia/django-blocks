#!/usr/bin/env python

from setuptools import setup, find_packages

SRC_PATH = 'src/python'

setup(
	name = "django-blocks",
	version = "0.1",
	packages = find_packages(SRC_PATH),
	package_dir = { '': SRC_PATH, },
	include_package_data = True,    # include everything in source control
	
	# blog still uses reStructuredText, so ensure that the docutils and Pygments get installed
	install_requires = ['Django'],
	
	# metadata for upload to PyPI
	author = "kimus",
	author_email = "kimus.linuxus@gmail.com",
	description = "Django Blocks will provide an easier way to build Web apps more quickly and with almost no code. ",
	license = "MIT License",
	url = "http://code.google.com/p/django-blocks/",
	download_url='http://code.google.com/p/django-blocks/downloads/detail?name=django-blocks-snapshot-r244.tar.gz',
	classifiers=['Development Status :: 4 - Beta',
		           'Environment :: Web Environment',
		           'Framework :: Django',
		           'Intended Audience :: Developers',
		           'License :: OSI Approved :: MIT License',
		           'Operating System :: OS Independent',
		           'Programming Language :: Python',
		           'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
		           'Topic :: Software Development',
		           'Topic :: Software Development :: Libraries :: Application Frameworks',
	],
)

