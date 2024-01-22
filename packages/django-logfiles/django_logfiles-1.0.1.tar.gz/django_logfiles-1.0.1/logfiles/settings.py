import django.conf


DEFAULT_SETTINGS = {
    'PATHS': ['/var/log/**.log'],
    'TAIL': 100,
    'SORT': ('-date',)
}

class ServerLogSettings:
    def __getattr__(self, item):
        try:
            return django.conf.settings.LOGFILES.get(item, DEFAULT_SETTINGS[item])
        except AttributeError:
            return DEFAULT_SETTINGS[item]


settings = ServerLogSettings()
