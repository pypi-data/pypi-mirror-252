import os
from pathlib import Path
import glob
import datetime

from django.db import models
from django.db.models.query import QuerySet
from .settings import settings
from django.core.exceptions import PermissionDenied

# This model file contains some fancy trickery to define a model, but avoid database
# access to that model for at least the purpose of what it is used for: viewing logfiles
# Attempting to use this model in code would probably run into issues, it's purely
# there for viewing logfiles in the admin section.


class LogQuerySet(QuerySet):
    ordered = ()

    def get_logs(self):
        if self._result_cache is not None:
            return self._result_cache
        logs = []
        for path in settings.PATHS:
            for logfile in glob.glob(str(path)):
                if os.access(logfile, os.R_OK):
                    log = Log(filepath = logfile)
                    log.date = datetime.datetime.fromtimestamp(os.path.getmtime(logfile))
                    log.size = os.path.getsize(logfile)
                    logs.append(log)
        if self.ordered:
            ordering = self.ordered[0].strip('-')
            def get_sort_field(log):
                return getattr(log, ordering)
            logs.sort(key=get_sort_field, reverse=self.ordered[0].startswith('-'))
        self._result_cache = logs
        return logs

    def get(self, **args):
        return Log(**args)

    def order_by(self, *ordering):
        # A bit of a hack, but OK since there's really only one sort order used anyway
        LogQuerySet.ordered = ordering
        return self

    def __len__(self):
        return len(self.get_logs())

    count = __len__


class LogManager(models.Manager):
    _db = None

    def get_queryset(self, **args):
        return LogQuerySet(model=Log, using=None)


class Log(models.Model):
    class Meta:
        managed = False

    filepath = models.CharField(max_length=2048, primary_key=True)
    tail = models.TextField(max_length=100000)
    date = models.DateTimeField()
    size = models.IntegerField()
    objects = LogManager()

    def __str__(self):
        return self.filename

    @property
    def filename(self):
        return Path(self.filepath).name

    def path_is_legal(self):
        for path in settings.PATHS:
            for logfile in glob.glob(str(path)):
                if self.filepath == logfile and os.access(logfile, os.R_OK):
                    return True
        return False

    def retrieve_tail(self):
        if not self.path_is_legal():
            raise PermissionDenied()
        tail = []
        for line_ in open(self.filepath):
            tail.append(line_)
            if len(tail) > settings.TAIL:
                tail = tail[-settings.TAIL:]
        return '\n'.join(tail)

    def __getattribute__(self, item):
        if item == 'tail':
            # Override the actual retrieval, just get it straight from storage
            return self.retrieve_tail()
        return super().__getattribute__(item)
