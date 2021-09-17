import unittest

from review_store.db import DatabaseStringBuilder


class MyTestCase(unittest.TestCase):
    def test_default(self):
        db = DatabaseStringBuilder('pg', 'pg_user')
        self.assertEqual(db.get_connection_string(), 'dbname=pg user=pg_user')

    def test_with_password(self):
        db = DatabaseStringBuilder('pg', 'pg_user')
        db.set_key('password', '12345')
        self.assertEqual(db.get_connection_string(), 'dbname=pg user=pg_user password=12345')

    def test_with_invalid_ky(self):
        db = DatabaseStringBuilder('pg', 'pg_user')
        db.set_key('pg', '12345')
        self.assertEqual(db.get_connection_string(), 'dbname=pg user=pg_user')


if __name__ == '__main__':
    unittest.main()
