# Introduction #

This page will guide you on how to install django-blocks in your enviorment.


# Installation #

The easiest way to test django-blocks is to get it from svn
```
svn co http://django-blocks.googlecode.com/svn/trunk/src/python/blocks/
```

NOTE: blocks needs to be on your system python path to be used globally.

TODO: write some help on installing blocks system wide.

Django needs you to install PIL (python-imaging).

For additional database support (optional):

> - For supporting MySQL you need to install MySQLDB (python-mysqldb)

> - For supporting PostgreSQL you need to install PyGreSQL (python-pgsql)

## Linux ##
Almost all distribuitions of GNU/Linux comes with Python installed so you just need to install Django.

## Macintosh ##
The latest Macintosh comes with Python installed so you just need to install Django.

## Windows ##
Format it and install a real OS :-). Ok, if you don't want to do that you need to install Python and Django first.

# Running Demo Sample #

## Get Demo Sample ##
```
svn co http://django-blocks.googlecode.com/svn/trunk/samples/demo
cd demo/python/demo
./manage runserver
```

## Requirements ##
Need to put django-tagging in your PYTHONPATH like:
```
svn co http://django-tagging.googlecode.com/svn/trunk/tagging/
```

or you can install it:
```
svn co http://django-tagging.googlecode.com/svn/trunk/ tagging-trunk
cd tagging-trunk
python setup.py install (might need sudo perms)
```

## Admin User ##
By default the user is admin and the password is... password :-)
You can change that by entering the administration site (url: /admin/) or (in the demo sample dir):
```
./manage shell
from django.contrib.auth.models import User
u = User.objects.get(username='admin')
u.set_password('secret')
u.save()
```


**WORK IN PROGRESS**