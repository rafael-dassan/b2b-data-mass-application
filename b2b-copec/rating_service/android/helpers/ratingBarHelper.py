def get_location_star(qtyStart, locationX, width):
    qtyStart = int(qtyStart)
    locationX = int(locationX)
    width = int(width)


    offset = (qtyStart * 0.17)
    aux = (width * offset) 
    clickPosition = aux + locationX
    return clickPosition