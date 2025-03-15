import math

FELUCCA = 0
TRAMMEL = 1
ILSHENAR = 2
MALAS = 3
TOKUNO = 4
FARAAN = 10

FACETS = [
    FELUCCA,
    TRAMMEL,
    TOKUNO,
    MALAS,
    ILSHENAR,
    FARAAN,
]

STRING_TO_FACET = {
    "Trammel": TRAMMEL,
    "Felucca": FELUCCA,
    "Tokuno": TOKUNO,
    "Malas": MALAS,
    "Ilshenar": ILSHENAR,
    "Faraan": FARAAN,
}

FACET_TO_STRING = {
    TRAMMEL: 'Trammel',
    FELUCCA: 'Felucca',
    TOKUNO: 'Tokuno',
    MALAS: 'Malas',
    ILSHENAR: 'Ilshenar',
    FARAAN: 'Faraan',
}

def get_facet_id(text):
    for name, facet in STRING_TO_FACET.items():
        if name in text:
            return facet

def get_facet_name(facet):
    if facet in FACET_TO_STRING:
        return FACET_TO_STRING[facet]

def get_distance(from_point, to_point):
    return math.sqrt((to_point[0] - from_point[0])**2 + (to_point[1] - from_point[1])**2)

def is_within_range(point1, point2, max_range = 13):
    return get_distance(point1, point2) <= max_range
