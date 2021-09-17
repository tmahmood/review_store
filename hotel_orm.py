from db import DbModel, DBOrm


class HotelOrm(DbModel):
    table_name = 'hotels'
    fields = ['hotel_name', 'address', 'location_id']
    expr = {
        "id": "nextval('hotels_seq')",
        "date_created": "now()"
    }

    def __init__(self, db, data=None, by_fields=None):
        super().__init__(db, {
            "table": HotelOrm.table_name,
            "fields": HotelOrm.fields,
            "expr": HotelOrm.expr,
            "data": data,
            "by_fields": by_fields
        })

    def validate(self):
        if not self.data['location_id']:
            return False
        return True
