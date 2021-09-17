import unittest

from review_store.location import Location
from review_store.hotel_orm import HotelOrm
from review_store.review_orm import ReviewOrm
from review_store.reviewer_orm import ReviewerOrm
from review_store.review_storage import parse_row
from review_store.tests.base_test_case import BaseTestCase


class TestApp(BaseTestCase):

    def setUp(self) -> None:
        self.init()

    def test_parse_row_and_create_objects(self):
        test_row = {'Hotel': '1 Homes Preview Cabo',
                    'Address': 'Calle Paseo de La Marina 4732 Col. El Medano, Cabo San Lucas 23450 Mexico',
                    'Reviewer': 'Devan S', 'Date': 'Aug-21', 'Reviewer Address': 'Riverside, California',
                    'Review Title': 'First Time at 1 Homes', 'Review Star': '5',
                    'Full Review': 'After Cabo trips for 30 years, our first time at 1 Homes was one of the best. '
                                   'Impeccable service and such kind and accomodating staff, especially Marcos and '
                                   'Johel. The residences, pool, and views are beautiful as well. We will be back!'}
        hotel_id, location_id, reviewer_location_id, review_id, reviewer_id = parse_row(self.db, test_row)
        # check hotel data
        hotel = HotelOrm(self.db, by_fields={"id": hotel_id})
        self.assertEqual(test_row['Hotel'], hotel.get('hotel_name'))
        # check review data
        review = ReviewOrm(self.db, by_fields={"id": review_id})
        self.assertEqual(review.get('reviewer_id'), reviewer_id)
        self.assertEqual(review.get('hotel_id'), hotel_id)
        # check reviewer data
        reviewer = ReviewerOrm(self.db, by_fields={"id": review.get('reviewer_id')})
        self.assertEqual(reviewer.get('id'), review.get('reviewer_id'))
        # check location data
        location = Location.load(self.db, location_id, 'Mexico')
        self.assertEqual('Cabo San Lucas', location.city)
        self.assertEqual('Mexico', location.country)
        self.assertEqual('Baja California Sur', location.state)


if __name__ == '__main__':
    unittest.main()
