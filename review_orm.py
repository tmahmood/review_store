from db import DbModel


class ReviewOrm(DbModel):
    table_name = 'reviews'
    fields = ['title', 'rating', 'full_review', 'review_date', 'word_count', 'hotel_id', 'reviewer_id']
    expr = {
        "id": "nextval('reviews_seq')",
        "date_created": "now()"
    }

    def __init__(self, db, data=None, by_fields=None):
        super().__init__(db, {
            'table': ReviewOrm.table_name,
            'fields': ReviewOrm.fields,
            'expr': ReviewOrm.expr,
            "data": data,
            "by_fields": by_fields
        })

    def validate(self):
        return True
