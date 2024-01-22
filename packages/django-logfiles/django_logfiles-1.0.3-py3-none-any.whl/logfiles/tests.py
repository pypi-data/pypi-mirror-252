import os.path
import sys
import unittest
import random
import datetime
import timeit

from . import models


class RandomLogFileGenerator:
    filename = 'random.log'

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    # vowel weight = 2, consonant weight = 1
    weights = [(2 if (x in 'aeiou') else 1) for x in alphabet]

    def create_random_word(self, length):
        return ''.join(random.choices(self.alphabet, self.weights, k=length))

    def generate(self, once=False):
        if once and os.path.isfile(self.filename): return
        logfile = open(self.filename, 'w')
        for l in range(10_000_000):
            if l % 100_000 == 0:
                sys.stdout.write('+')
                sys.stdout.flush()
            words = []
            for _ in range(random.randint(2, 16)):
                words.append(self.create_random_word(random.randint(2, 16)))
            timestamp = datetime.datetime.now()
            line_ = '{}: {}\n'.format(timestamp, ' '.join(words))
            logfile.write(line_)


class DjangoLogfilesSettingsTest(unittest.TestCase):
    def setUp(self):
        RandomLogFileGenerator().generate(once=True)

    def test_paths(self):
        logs = models.LogQuerySet().get_logs()
        self.assertNotEquals(logs, [])

    def test_tail_read_speed_baseline(self):
        # Baselining old read speed
        duration = timeit.timeit('log.retrieve_tail(ignore_path_check=True, slow=True)',
                                 setup='log = models.Log(filepath="random.log")',
                                 number=1,
                                 globals=globals())
        # No assert statement, just baselining
        print(duration)

    def test_tail_read_faster_speed(self):
        # Testing new read speed
        duration = timeit.timeit('log.retrieve_tail(ignore_path_check=True)',
                                 setup='log = models.Log(filepath="random.log")',
                                 number=1,
                                 globals=globals())
        print(duration)
        # Anything less then 100 milliseconds is definitely speedy enough
        self.assertLessEqual(duration, 0.100)

    def test_tail_read_functional(self):
        log = models.Log(filepath=RandomLogFileGenerator.filename)
        tail = log.retrieve_tail(ignore_path_check=True)
        lines = tail.splitlines()
        self.assertEqual(len(lines), 100)
