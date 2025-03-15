from bigfish.libs.uo.map import get_facet_name, FARAAN, FELUCCA


def create_marker(x, y, name, color = "blue", facet = None, zoom = 0):
    facet_name = get_facet_name(facet)
    facet = FELUCCA if facet == FARAAN else facet
    return "{},{},{},{},,{},{}".format(x, y, facet, name, color, zoom)