#Reference of the applications and how to use Blocks

# Introduction #

This page describes all the application (or modules) that Blocks could give to your site and gives some help on how to begging in your first Block based site.


# Applications #

## blocks.apps.core ##
Core application that implements the base core components required for using Blocks.

## blocks.apps.administration ##
Administration templates that is almost a requirement for multi-language content models.

## blocks.apps.aggregator ##
Configure and display your favorite RSS/ATOM feeds.

## blocks.apps.blog ##
Pre configured blog application.

## blocks.apps.cart ##
Shopping cart application that implements a simple way to sell yours stuff (any model) in your site.

## blocks.apps.search ##
Adds search capabilities to your models. Indexes and searches using Xapian engine.

## blocks.apps.contacts ##
Adds a contact form handler to you site. Can handle multiple contact (or registration, etc) forms and each contact form can be emailed to different emails.


# Settings Example #
```
MIDDLEWARE_CLASSES = (
#    'django.middleware.cache.CacheMiddleware',
    'django.middleware.http.SetRemoteAddrFromForwardedFor',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    
    'blocks.core.middleware.CommonMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS =(
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    
    'blocks.core.context_processors.media'
)

INSTALLED_APPS = (
    # blocks applications #
    'blocks.apps.core',
    'blocks.apps.administration',
    'blocks.apps.cart',
    'blocks.apps.search',
    'blocks.apps.contacts',
    
    # django applications #
    'django.contrib.admindocs',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    
    # site applications #
    # put your site applications here

    # misc applications #
    'filebrowser',
    
    # accounts #
    'registration',
    'profiles'
)
```