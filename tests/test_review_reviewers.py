import unittest

from review_store.hotel_orm import HotelOrm
from review_store.location import Location
from review_store.review_orm import ReviewOrm
from review_store.reviewer_orm import ReviewerOrm
from review_store.tests.base_test_case import BaseTestCase


class MyTestCase(BaseTestCase):
    def setUp(self) -> None:
        self.init()
        self.location = Location.new_location(self.db, "Hatirjheel, Dhaka")
        self.location.save()
        self.reviewer = ReviewerOrm(self.db, data={ "name": "Davis S", "address": "Niketon, Dhaka",
                                                    "location_id": self.location.id})
        self.hotel = HotelOrm(self.db, data={"hotel_name": "Sheraton", "address": "Hatirjheel, Dhaka",
                                             "location_id": self.location.id})
        self.reviewer.save()
        self.hotel.save()

    def test_review(self):
        data = {'Reviewer': 'Devan S', 'Date': 'Aug-21', 'Reviewer Address': 'Riverside, California',
                'Review Title': 'First Time at 1 Homes', 'Review Star': '5',
                'Full Review': 'After Cabo trips for 30 years, our first time at 1 Homes was one of the best. '
                               'Impeccable service and such kind and accomodating staff, especially Marcos and '
                               'Johel. The residences, pool, and views are beautiful as well. We will be back!'}
        review = ReviewOrm(self.db, {
            'title': data['Review Title'],
            'rating': data['Review Star'],
            'full_review': data['Full Review'],
            'review_date': data['Date'],
            'word_count': len(data['Full Review'].split()),
            'reviewer_id': self.reviewer.id,
            'hotel_id': self.hotel.id
        })
        review.save()
        self.assertEqual(review.get('word_count'), 42)


if __name__ == '__main__':
    unittest.main()
