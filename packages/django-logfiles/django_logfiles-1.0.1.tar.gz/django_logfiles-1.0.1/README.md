# Django Logfiles

This Django Admin plugin provides a simply way to view logfiles from the Django Admin
panels. 

Install it on your system using PIP:

```
pip install django-logfiles
```

Configuration can be set in settings.py:

```
INSTALLED_APPS = [
    ...  # All other apps
    'logfiles'
]

LOGFILES = {
    'PATHS': ['/var/log/**.log'],
    'TAIL': 100,
    'SORT': ('-date',)
}
```

All settings are optional, so even if you don't provide any settings, the above settings are
the default settings.

The example project allows to play around with the plugin.
It comes with an SQlite3 database with one superuser
named `test` and password `test`.
