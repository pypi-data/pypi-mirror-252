import shapely 

def boxintersect(a, sizex,sizey): #lets define that b is always the box
    b = [[-sizex/2,-sizey/2],[-sizex/2,sizey/2], [sizex/2,sizey/2], [sizex/2,-sizey/2]]
    poly1 = shapely.geometry.Polygon(a)
    poly2 = shapely.geometry.Polygon(b)
    intersection = poly1.intersection(poly2)
    if poly1.intersects(poly2) == False:
        return [False]        
    else:
        if intersection.geom_type == 'Polygon':
            return [list(intersection.exterior.coords)]
        elif intersection.geom_type == 'Point':
            return [False]
        else:
            return [False]  
        
        
def crop(a, sizex,sizey): #lets define that b is always the box
    ret = []
    for elements in a:
        toret = boxintersect(elements, sizex,sizey)
        toret = toret[0]
        if toret == False:
            continue
        toret = [list(tup) for tup in toret]
        ret.append(toret)
    
    #convert to list of lists (actually a list of tuples)
    return ret
    

def write(fp, points):
    if not points:
        return
    
    if isinstance(points, (list, tuple)):
        pass
    else:
        
        return
    if len(points) > 2:
        
        x, y = points[0]
    else:
       
        return
    data = 'M{},{} ' .format(x, y)
    for p in points[1:]:
        x, y = p
        data += 'L{},{} ' .format(x, y)
    data += 'Z'  
    fp.write('<path d="{}" fill="Black" stroke="none" />\n'.format(data))


def export(geo, xsize, ysize, filename):
    with open(filename, 'w') as fp:
        fp.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fp.write('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{}" height="{}" viewBox="{} {} {} {}">\n'.format(xsize, ysize,-xsize/2, -ysize/2, xsize, ysize))
        fp.write('<defs>\n')
        fp.write('</defs>\n')
        
        for lines in geo:
            
                
                write(fp, lines)    
        fp.write('</svg>')

def translate(poly, x, y):
    ret = []
    for elements in poly:
        toret = []
        for points in elements:
            toret.append([points[0] + x, points[1] + y])
        ret.append(toret)
    return ret