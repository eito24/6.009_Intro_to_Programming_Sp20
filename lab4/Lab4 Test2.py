def rangify(n,dimension):
    rangified={n}
    if n<dimension:
        rangified.add(n+1)
    elif n>0:
        rangified.add(n-1)
    return rangified

def addingvals(neighborhood,rangified):
    return

    
def getneighbor(neighborhood,addingstuff):
    neighborhood=[]
    if len(neighborhood)==0:
        ranges=rangify(coordinates[0],dimensions[0])
        for val in ranges:
            neighborhood.append((val))
    else:
        for i in range(len(neighborhood)):
            ranges=rangify(coordinates[0],dimensions[0])
            for val in ranges:
                neighborhood[i].append((val))
    return neighborhood

    

r=98
c=8
d=998
neighborhood=[]
rrange=[r-1,r,r+1]
crange=[c-1,c,c+1]
drange=[d-1,d,d+1]
for rval in rrange:
    for cval in crange:
        for dval in drange:
            neighborhood.append((rval,cval,dval))
neighborhood.remove((r,c,d))
print(neighborhood)

#print(getneighbor((98,8,998),(100,10,1000)))
