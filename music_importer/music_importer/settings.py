# Django settings for music_importer project.

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

MYSQL_CONF = {
    'host' : '127.0.0.1',
    'name' : 'fakemusic',
    'user' : 'music',
    'password' : 'P@55word',
    'port' : '3306'
}

MYSQL_OFFLINE_CONF = {
    # 'host' : '192.168.1.109',
    'host' : '127.0.0.1',
    'name' : 'music',
    'user' : 'music',
    'password' : 'P@55word',
    'port' : '3306'
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': MYSQL_CONF['name'], # Or path to database file if using sqlite3.
        'USER':  MYSQL_CONF['user'], # Not used with sqlite3.
        'PASSWORD': MYSQL_CONF['password'], # Not used with sqlite3.
        'HOST': MYSQL_CONF['host'], # Set to empty string for localhost. Not used with sqlite3.
        'PORT': MYSQL_CONF['port'], # Set to empty string for default. Not used with sqlite3.
    },
    'offline' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  MYSQL_OFFLINE_CONF['name'],
        'USER':  MYSQL_OFFLINE_CONF['user'],
        'PASSWORD': MYSQL_OFFLINE_CONF['password'],
        'HOST': MYSQL_OFFLINE_CONF['host'],
        'PORT': MYSQL_OFFLINE_CONF['port'],
    }
}

class MysqlRouter(object):

    OFFLINE_TABLES = ['fs_entry', 'fs_entry_amazon', 'fs_vol']

    def db_for_read(self, model, **hints):
        if model._meta.db_table in self.OFFLINE_TABLES:
            return 'offline'
        else:
            return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.db_table in self.OFFLINE_TABLES:
            return 'offline'
        else:
            return 'default'

    def allow_syncdb(self, db, model):
        if model._meta.db_table in self.OFFLINE_TABLES:
            return db == 'offline'
        else:
            return db == 'default'

DATABASE_ROUTERS = ['music_importer.settings.MysqlRouter']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    #'django.contrib.staticfiles.finders.FileSystemFinder',
    #'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3#f-bt1c86#)z1c7^fxvt#o^(s001s9_9ytiud&amp;o7^w@!jzy(y'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    #'django.template.loaders.filesystem.Loader',
    #'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    #'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'music_importer.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'music_importer.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    #'django.contrib.auth',
    #'django.contrib.contenttypes',
    #'django.contrib.sessions',
    #'django.contrib.sites',
    #'django.contrib.messages',
    #'django.contrib.staticfiles',
    'data',
    'importer',
    'utils',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOG_ROOT = '/var/app/log/music-importer/'

LOGGERS_NAME = ["importer", "merger", "daemon", 'meta_db', 'rabbitmq', 'search']

def get_logging(loggers_name):
    logging = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(levelname)s %(asctime)s %(message)s'
            },
            'detail': {
                'format': '%(levelname)s %(asctime)s [%(module)s.%(funcName)s line:%(lineno)d] %(message)s',
            },
        }
    }
    handlers = {
       'console': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        }
    }
    loggers = {}
    for logger_name in LOGGERS_NAME:
        handlers[logger_name + "_file"] = {
            'level': 'DEBUG',
            'formatter': 'simple',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(LOG_ROOT, logger_name + ".log"),
         }
        handlers[logger_name + "_err_file"] = {
            'level': 'WARN',
            'formatter': 'detail',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(LOG_ROOT, logger_name + "_error.log"),
        }
        loggers[logger_name]  = {
            'handlers': [logger_name + '_file',  logger_name +'_err_file'],
            'level': 'DEBUG',
            'propagate': True,
        }

    logging['handlers'] = handlers
    logging['loggers'] = loggers

    return logging

LOGGING = get_logging(LOGGERS_NAME)

MQ_CONF = {
   'user' : 'music',
   'password' : '',
   'host' : '127.0.0.1',
   'port' : 5672,
   'vhost' : 'music',

   'normal_exchange' : 'music-import-normal',
   'normal_queue' : 'music-import-normal',
   'normal_routing_key' : 'music-import-normal',

   'quick_exchange' : 'music-import-quick',
   'quick_queue' : 'music-import-quick',
   'quick_routing_key' : 'music-import-quick',

   'vip_exchange' : 'music-import-vip',
   'vip_queue' : 'music-import-vip',
   'vip_routing_key' : 'music-import-vip',
}
