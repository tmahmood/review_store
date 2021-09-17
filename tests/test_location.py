import unittest

from review_store.location import Location
from review_store.tests.base_test_case import BaseTestCase


class TestingLocation(BaseTestCase):

    def setUp(self) -> None:
        self.init()
        self.db.execute_no_result('truncate locations cascade')
        self.location = Location.new_location(self.db, "Kind of 23493 Mexico", 'Mexico')

    def test_no_duplicate_location(self):
        location = Location.new_location(self.db, "Leona Vicario, 11, Cabo San Lucas 23410 Mexico", 'Mexico')
        location.save()
        location2 = Location.new_location(self.db, "Leona Vicario, 11, Cabo San Lucas 23410 Mexico", 'Mexico')
        self.assertEqual(location2.id, location.id)

    def test_reg_exp(self):
        location = Location.new_location(
            self.db,
            "Leona Vicario, 11, Cabo San Lucas 23410 Mexico",
            'Mexico'
        )
        self.assertEqual('Cabo San Lucas', location.city)
        self.assertEqual('Mexico', location.country)
        self.assertEqual('Baja California Sur', location.state)

    def test_hotel_location(self):
        location = Location.new_location(self.db, "Leona Vicario, 11, Cabo San Lucas 23410 Mexico", 'Mexico')
        location.save()
        r = self.db.query_get("select city, country from locations where id = %s", (location.id,))
        self.assertEqual("Cabo San Lucas", r[0][0])
        self.assertEqual("Mexico", r[0][1])

    def test_hotel_default_location_with_all(self):
        location = Location.new_location(self.db, "San Diego, California, United States", 'DefaultLocation')
        self.assertEqual('San Diego', location.city)
        self.assertEqual('California', location.state)
        self.assertEqual('United States', location.country)

    def test_hotel_default_location(self):
        location = Location.new_location(self.db, "Bluffton, South Carolina", 'DefaultLocation')
        self.assertEqual('Bluffton', location.city)
        self.assertEqual('South Carolina', location.country)
