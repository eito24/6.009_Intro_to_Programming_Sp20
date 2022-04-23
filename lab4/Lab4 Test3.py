def rangify(n,dimension):
    rangified={n}
    if n<dimension:
        rangified.add(n+1)
    elif n>0:
        rangified.add(n-1)
    return rangified

def neighbors(dimensions,coordinates):
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
    if coordinates in neighborhood:
        neighborhood.remove(coordinates)
    return neighborhood

print(neighbors((2,2),(0,0)))

dimension=(2,2)
coordinates=(1,1)
neighborhood=[]
rangex=rangify(coordinates[0],dimension[0])
for x in rangex:
    neighborhood.append((x))
rangey=rangify(coordinates[1],dimension[1])
for y in rangey:
    for coor in neighborhood:
        coor.append(y)
print 
