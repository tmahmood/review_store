from review_store.db import build_select_query
from review_store.hotel_orm import HotelOrm
from review_store.location import Location
from review_store.tests.base_test_case import BaseTestCase


class TestDbOrm(BaseTestCase):

    def setUp(self) -> None:
        self.init()
        self.db.execute_no_result('truncate locations cascade')
        self.location = Location.new_location(self.db, "Kind of 23493 Mexico", 'Mexico')
        self.location.save()

    def test_select_query_build_multi_fields(self):
        q = build_select_query(
            'hotels',
            ['hotel_name', 'address', 'location_id', 'id', 'date_created'],
            {'hotel_name': 'Test', 'address': "Somewhere"}
        )
        self.assertEqual(
            q,
            """select hotel_name, address, location_id, id, date_created from hotels 
        where hotel_name = %s and address = %s"""
        )

    def test_select_query_build(self):
        q = build_select_query(
            'hotels',
            ['hotel_name', 'address', 'location_id', 'id', 'date_created'],
            {'id': 3}
        )
        self.assertEqual(
            q,
            """select hotel_name, address, location_id, id, date_created from hotels 
        where id = %s"""
        )

    def test_hotel_entry(self):
        h = HotelOrm(self.db, {
            "hotel_name": "Test",
            "address": "Somewhere",
            "location_id": self.location.id
        })
        self.assertTrue(h.save())
        r = self.db.query_get("select * from hotels where id = %s", (h.id,))
        self.assertEqual(r[0][3], "Test")

    def test_hotel_load(self):
        h = HotelOrm(self.db, {"hotel_name": "Somewhere", "location_id": self.location.id})
        self.assertTrue(h.save())
        h1 = HotelOrm(self.db, by_fields={"hotel_name": "Somewhere"})
        self.assertIsNotNone(h1)
        self.assertEqual(h1.id, h.id)

    def test_hotel_load_by_id(self):
        h = HotelOrm(self.db, {"hotel_name": "Somewhere", "location_id": self.location.id})
        self.assertTrue(h.save())
        h1 = HotelOrm(self.db, by_fields={"id": h.id})
        self.assertIsNotNone(h1)
        self.assertEqual(h1.data['hotel_name'], h.data['hotel_name'])

    def test_loading_non_existent_hotel(self):
        self.assertRaises(Exception, HotelOrm, self.db, by_fields={'hotel_name': 'Test No Hotel'})
