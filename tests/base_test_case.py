from unittest import TestCase

from review_store.db import DB


class BaseTestCase(TestCase):

    def init(self) -> None:
        with open('tests/dsn_test.txt', 'r') as fp:
            dsn = fp.readline()
        self.db = DB(dsn)
