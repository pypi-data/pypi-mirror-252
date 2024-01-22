# from django.test import TestCase
import unittest

import models

class DjangoLogfilesSettingsTest(unittest.TestCase):
    def test_paths(self):
        logs = models.LogQuerySet().get_logs()
        self.assertNotEquals(logs, [])
