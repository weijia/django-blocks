#!/usr/bin/env python

from setuptools import setup, find_packages

SRC_PATH = 'src/python'

setup(
	name = "django-blocks",
	version = "0.1",

	packages = find_packages(SRC_PATH),
	package_dir = { '': SRC_PATH, },

	# blog still uses reStructuredText, so ensure that the docutils and Pygments get installed
	install_requires = ['PIL', 'docutils', 'Pygments'],


	# metadata for upload to PyPI
	author = "kimus",
	author_email = "kimus.linuxus@gmail.com",
	description = "Django Blocks will provide an easier way to build Web apps more quickly and with almost no code. ",
	license = "MIT License",
	url = "http://code.google.com/p/django-blocks/",
)
