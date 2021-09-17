import re

try:
    from review_store.db import DbModel
except ModuleNotFoundError:
    from db import DbModel

STATE_DATA = {
    "00-16": "CDMX",
    "20": "Aguascalientes",
    "21-22": "Baja California",
    "23": "Baja California Sur",
    "24": "Campeche",
    "29-30": "Chiapas",
    "31-33": "Chihuahua",
    "25-27": "Coahuila",
    "28": "Colima",
    "34-35": "Durango",
    "36-38": "Guanajuato",
    "39-41": "Guerrero",
    "42-43": "Hidalgo",
    "44-49": "Jalisco",
    "50-57": "México",
    "58-61": "Michoacán 62 Morelos",
    "63": "Nayarit",
    "64-67": "Nuevo León",
    "68-71": "Oaxaca",
    "72-75": "Puebla",
    "76": "Querétaro",
    "77": "Quintana Roo",
    "78-79": "San Luis Potosí",
    "80-82": "Sinaloa",
    "83-85": "Sonora",
    "86": "Tabasco",
    "87-89": "Tamaulipas",
    "90": "Tlaxcala",
    "91-96": "Veracruz",
    "97": "Yucatán",
    "98–99": "Zacatecas"
}


def get_state_from_zip(postal_code):
    two_digits = int(postal_code[:2])
    for ky in STATE_DATA:
        try:
            s, e = [int(s) for s in ky.split('-')]
            if s <= two_digits <= e:
                return STATE_DATA[ky]
        except ValueError:
            if int(ky) == two_digits:
                return STATE_DATA[ky]
    raise IndexError("No key found")


class Mexico(DbModel):
    def __init__(self, db, data, oid=None):
        super().__init__(db)
        self.id = None
        if oid:
            self.city, self.country, self.state = data[0], data[1], data[2]
            self.id = oid
        else:
            self.address = data
            last_seg = data.split(',').pop().strip()
            split = re.split(r'(.*)(\d{5})(.*)', last_seg)
            failed = False
            try:
                self.city, self.country, postal = split[1].strip(), split[3].strip(), split[2].strip()
                self.state = get_state_from_zip(postal)
            except IndexError:
                self.city = None
                self.country = None
                self.state = None
                failed = True
            if not failed:
                r = db.load(
                    """select id, city, state, country from locations 
                    where city=%s and state=%s and country=%s""", (self.city, self.state, self.country)
                )
                if not r:
                    return
                pid, city, state, country = r
                self.id = pid

    def save(self):
        q = Mexico.build_query()
        self.id = self.db.execute(q, (self.city, self.country, self.state, self.address))
        if self.id:
            return True
        return False

    @staticmethod
    def load(db, oid):
        city, state, country = db.load("select city, state, country from locations where id = %s", (oid,))
        return Mexico(db, [city, country, state], oid)

    @staticmethod
    def build_query():
        return """insert into locations (id, date_created, city, country, state, address) 
        values (nextval('locations_seq'), now(), %s, %s, %s, %s) returning id"""
