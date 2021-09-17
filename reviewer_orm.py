from db import DbModel


class ReviewerOrm(DbModel):
    table_name = 'reviewers'
    fields = ['name', 'address', 'location_id']
    expr = {
        "id": "nextval('reviews_seq')",
        "date_created": "now()"
    }

    def __init__(self, db, data=None, by_fields=None):
        super().__init__(db, {
            'table': ReviewerOrm.table_name,
            'fields': ReviewerOrm.fields,
            'expr': ReviewerOrm.expr,
            "data": data,
            "by_fields": by_fields
        })

    def validate(self):
        return True


def new_reviewer_from_data(db, data):
    return ReviewerOrm(db, data['Reviewer'], data['Reviewer Address'])
