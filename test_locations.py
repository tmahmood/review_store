from flashgeotext.geotext import GeoText

TEST_LOCATIONS = [
    "Irvine",
    "Prague, Czech Republic",
    "San Francisco, CA",
    "Seattle, Washington ",
    "NWT",
    "Frisco, Texas",
    "Boulder, Colorado",
    "Los Angeles, California",
    "Moose Jaw, Canada",
    "Fort Worth, Texas, United States",
    "Show Low, Arizona",
    "Lacombe, Canada",
    "Smyrna, Georgia",
    "Calle Paseo de La Marina 4732 Col. El Medano, Cabo San Lucas 23450 Mexico",
    "00000 Baja California Sur (Cabo San Lucas Camino del Cerro S/N, Cabo San Lucas Mexico",
    "Fraccionamiento Diamante, Cabo San Lucas 23473 Mexico",
    "Blvd. Marina Lotes 9 y 10 Colonia Centro, Cabo San Lucas 23450 Mexico",
]


def parse_locations():
    geo_text = GeoText()
    input_text = '''Shanghai. The Chinese Ministry of Finance in Shanghai said that China plans
                    to cut tariffs on $75 billion worth of goods that the country
                    imports from the US. Washington welcomes the decision.'''

    for l in TEST_LOCATIONS:
        r = geo_text.extract(input_text=l)
        print(r)


if __name__ == '__main__':
    parse_locations()
