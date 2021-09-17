import unittest

from review_store.locations.mexico import get_state_from_zip


class Tests(unittest.TestCase):

    def test_get_state_from_zip_all(self):
        self.assertEqual(
            'CDMX',
            get_state_from_zip('001223')
        )

    def test_get_state_from_zip_single(self):
        self.assertEqual(
            'Campeche',
            get_state_from_zip('241223')
        )


if __name__ == '__main__':
    unittest.main()
