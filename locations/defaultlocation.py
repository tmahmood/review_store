try:
    from review_store.db import DbModel
except ImportError:
    from db import DbModel


class DefaultLocation(DbModel):
    """
    Default location handler, consist of city, and country. It could also include state
    """

    def __init__(self, db, data, oid=None):
        super().__init__(db)
        if oid:
            self.id = oid
            self.city, self.country, self.state,  self.address = data[0], data[1], data[2], data[3]
        else:
            self.address = data
            if data.strip() == '':
                self.state = None
                self.city = None
                self.country = None
                return
            split = [s.strip() for s in data.split(',')]
            # To derive "city", "territory", "country" from "Reviewers Address",
            # we can split the string by comma. If the resulting array has a length of 2.
            # Then city = [0] and country = [1]. If the resulting array is 3,
            # then city = [0], territory = [1], territory = [2].
            if len(split) == 3:
                self.city, self.state, self.country = split
            elif len(split) == 2:
                self.city, self.country = split
                self.state = None
            else:
                self.city = data[0]
                self.country = None
                self.state = None

    def save(self):
        q = DefaultLocation.build_query()
        self.id = self.db.execute(q, (self.city, self.country, self.state, self.address))
        if self.id:
            return True
        return False

    @staticmethod
    def load(db, oid):
        city, state, country, address = db.load(f"select city, state, country, address from locations where id = {oid}")
        return DefaultLocation(db, [city, country, state, address], oid)

    @staticmethod
    def build_query():
        return """insert into locations (id, date_created, city, country, state, address) 
        values (nextval('locations_seq'), now(), %s, %s, %s, %s) returning id"""
