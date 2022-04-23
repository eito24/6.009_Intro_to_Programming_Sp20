def rangify(n,dimension):
    """gets range for neighbors"""
    rangified={n}
    if n<dimension-1:
        rangified.add(n+1)
    if n>0:
        rangified.add(n-1)
    return rangified


def neighbors(dimensions,coordinates):
    """A function that returns (or a generator--introduced in week 4's lecture--that yields) all the neighbors of a given set of coordinates in a given game."""
    neighborhood=[]
    if len(dimensions)==1:
        ranges=rangify(coordinates[0],dimensions[0])
        for val in ranges:
            neighborhood.append((val,))
    else:
        current_neighbors=neighbors(dimensions[1:],coordinates[1:])
        ranges=rangify(coordinates[0],dimensions[0])
        for stuff in current_neighbors:
            for val in ranges:
                neighborhood.append((val,)+stuff)
    return neighborhood

print(neighbors((3,4),(2,0)))
