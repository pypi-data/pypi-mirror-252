import math
from . import svgop as svg
def cycle_xstart(xstart, c):
    #xstart is for moving the line to the left or right, but never more than c
    #c is the line spacing
    #return the new xstart
    print ("cycle_xstart")
    print(xstart)
    if xstart > c:
        direction = -1
    elif xstart < 0:
        direction = 1
    
    while True:
        if abs(xstart) < 2*c:
            break
        else:
            xstart += direction*c*2
    print(xstart)
    return xstart

def simple(dl, c, angle, xsize,ysize, xstart = None):
    angle = math.radians(angle)
    sinb = math.sin(angle) #So we aren't calculating it every time like a retard
    cosb = math.cos(angle)
    c2 = 1/(1/c - sinb/dl) # no indef
    if not xstart:
        xstart = -xsize/2
    else:
        xstart = cycle_xstart(xstart,c2) - xsize/2
    
    
    angle = math.radians(angle)
    
    minx = -xsize/2
    miny = -ysize/2
    maxx = xsize/2
    maxy = ysize/2
    
    actual_pos = xstart
 
    #check direction:
    x_f_max = (cosb*maxy/dl)/(1/c - sinb/dl) + actual_pos  
    x_f_min = (cosb*miny/dl)/(1/c - sinb/dl) + actual_pos
    print("actual c2")
    print(c2)
    
    if x_f_min >= x_f_max:
        
        while True:
            actual_pos -= 2*c2
            x_f_min = (cosb*miny/dl)/(1/c - sinb/dl) + actual_pos
            if x_f_min < xstart:
                
                break 
        #lines construction from bottom to top -> always black first, and the line always start in cut at -sizex/2,0 (or startx)
    else:
        while True:
            actual_pos -= 2*c2
            x_f_max = (cosb*maxy/dl)/(1/c - sinb/dl) + actual_pos  
            if x_f_max < xstart:
                break
        
        
    poly = []
    x_cut_list = []
    
    while True:
        
        x_f_max = (cosb*maxy/dl)/(1/c - sinb/dl) + actual_pos  
        x_f_min = (cosb*miny/dl)/(1/c - sinb/dl) + actual_pos #elegant as fuck
        
        pt2 = [x_f_max,maxy]
        pt1 = [x_f_min,miny]
        
        actual_pos += c2 # where the line cut at 0
        x_cut_list.append(actual_pos)
        
        x_f_max = (cosb*maxy/dl)/(1/c - sinb/dl) + actual_pos  
        x_f_min = (cosb*miny/dl)/(1/c - sinb/dl) + actual_pos
        
        pt4 = [x_f_min,miny]
        pt3 = [x_f_max,maxy]
        
        actual_pos += c2 #always generating a complete line
        
        line = [pt1,pt4,pt3,pt2]
        
        poly.append(line)
        x_cut_list.append(actual_pos)
        
        if (x_f_max > maxx and x_f_min > maxx):
            
            break
                
    
    x_rightside_distance = findlastblackline(maxx, x_cut_list,c2)
    x_leftside_distance = xstart + xsize/2
    

    
    return poly, x_rightside_distance, x_leftside_distance, x_cut_list

def check_blackstart (xstart, x_cut_list, c2):
    #check if the first line in the canvas start with black
    #return true if it start with black
    #return false if it start with white
    #xstart is the x position of the first line in y = 0
    linecount = 0
    for x in x_cut_list:
        linecount += 1
        if x >= xstart:
            break
    if linecount % 2 == 0: 
        return True
    else:
        return False
    
def findlastblackline(maxx, x_cut_list,c2):
    #find the last black line in the pattern
    #return the difference between the last black line and maxx
    count = 0
    for x in x_cut_list:
        count += 1
        if x >= maxx:
            if count % 2 != 0:
                return  (x-c2) - maxx
            else:
                return (x-2*c2) - maxx
        
                
            
                
def invert(poly, x_cut_list):
    #invert the color of the pattern TODO add the x_cut list to this function in order to return it modified accordingly
    #return the inverted pattern
    newpoly = []

    i = 0 #TODO check first and last points (x_cut and the others 2 things that i have to check in the "main" function)
    while True:
        #delete elements from next line
        line_left_pt1 = poly[i][3]
        line_left_pt2 = poly[i][2]
        
        if len(poly) - 1 == i:
            break
       
        line_right_pt1 = poly[i+1][1]
        line_right_pt2 = poly[i+1][0]
        
        newpoly.append([line_left_pt1,line_left_pt2,line_right_pt1,line_right_pt2])
        
        i += 1
        
    #delete first and last elements from x_cut_list    
     
    x_cut_list = x_cut_list[1:]
    x_cut_list = x_cut_list[:-1]  
    linecount = 0
    for line in newpoly:
        
        if len(line) != 4:
            poly.pop(linecount)
        
        linecount += 1      
    
    return newpoly, x_cut_list
    
def base(c, xsize, ysize):
    p1 = [-xsize/2, -ysize/2]
    p2 = [-xsize/2 + c, -ysize/2]
    p3 = [-xsize/2 + c, ysize/2]
    p4 = [-xsize/2, ysize/2]
    export = [p1, p2, p3, p4]
    base = []
    while True:
        base.append(export)
        p1 = [p1[0] + 2*c, p1[1]]
        p2 = [p2[0] + 2*c, p2[1]]
        p3 = [p3[0] + 2*c, p3[1]]
        p4 = [p4[0] + 2*c, p4[1]]
        export = [p1, p2, p3, p4]
        if p1[0] >= xsize/2:
            break
    return base
        
import math
"""""
def cylinder(h, r, l, c, angle = 90, xstart = None, stepsize = None):
    
    if not stepsize:
        stepsize =h/100
    
    
    
    def obtain_dx(x, r, n):
        dx = r * 2 * math.sqrt(1 - (x / r) ** 2) * math.sin(math.pi / n)
        return dx
    
    def obtain_dl(dx, angle):
        sinb = math.sin(angle)
        dl = sinb * dx
     
        return dl
    
    def obtain_c(dx, angle, c):
        dl = obtain_dl(dx, angle)
        sinb = math.sin(angle) #So we aren't calculating it every time like a retard
        c2 = 1/(1/c - sinb/dl) # no indef
        return c2

    def n_from_l(r, l):
        perimeter = 2 * r * math.pi
        n = perimeter / l
        return n

    def construct_lines(h, points):
        lines = []
        for i in range(0, len(points), 2):
            point1 = [points[i], -h / 2]
            try:
                point2 = [points[i + 1], -h / 2]
            except IndexError:
                point2 = [h / 2, -h / 2]
            point3 = [point2[0], h / 2]
            point4 = [points[i], h / 2]

            line = [point2, point1, point4, point3]
            lines.append(line)
        return lines
   
    
    angle = math.radians(angle)
    if not xstart:
        xstart = -r
    else:
        c2 = obtain_c(obtain_dx(0, -r + stepsize, n_from_l(r, l)),angle, c)
        
        xstart = cycle_xstart(xstart,c2) - r
    

    n = n_from_l(r, l)
    actual_pos = xstart
    lcount = 0
    sinb = math.sin(angle) #So we aren't calculating it every time like a retard
    cosb = math.cos(angle)
    x_cut = [actual_pos]
    right_distance = False
    if math.degrees(angle)%90 == 0:
    
        while True:
            enter_pos = actual_pos
            
            
            while True:
                lcount += stepsize 
                actual_pos += stepsize
                if actual_pos >= r:
                    aprox_pos = actual_pos - stepsize
                    right_distance = enter_pos + obtain_c(obtain_dx(aprox_pos,r,n),angle,c) - r
                    break
                
                dx = obtain_dx(actual_pos, r, n)
                c2 = obtain_c(dx,angle, c)
                
                if c2 <= lcount:
                    point = c2 + enter_pos
                    actual_pos = point
                    break
                           
                
            if actual_pos >= r:
                    if not right_distance:
                        right_distance = point - r
                    break
            
            x_cut.append(point)
            
            

        # create the lines
        poly = construct_lines(h, x_cut)
        left_distance = xstart + r

        return poly, x_cut, right_distance, left_distance
    
    else:
        sinb = math.sin(angle) #So we aren't calculating it every time like a retard
        cosb = math.cos(angle)
        minx = -r
        miny = -h/2
        maxx = r
        maxy = h/2
        while True:
            enter_pos = actual_pos
            dl = obtain_dl(dx,angle)
            x_f_max = (cosb*maxy/dl)/(1/c - sinb/dl) + actual_pos  
            x_f_min = (cosb*miny/dl)/(1/c - sinb/dl) + actual_pos
    
            
            while True:
                lcount += stepsize 
                actual_pos += stepsize
                if actual_pos >= r:
                    right_distance = enter_pos + obtain_c(obtain_dx(enter_pos,r,n),angle,c) - r
                    break
                
                dx = obtain_dx(actual_pos, r, n)
                c2 = obtain_c(dx,angle, c)
                if dx == 0:
                    point = c2 + enter_pos
                    break 
                if c2 <= lcount:
                    point = c2 + enter_pos
                    actual_pos = point
                    break
                
            if actual_pos >= r:
                    if not right_distance:
                        right_distance = point - r
                    break
            
            x_cut.append(point)
            
            

        # create the lines
        poly = construct_lines(h, x_cut)
        left_distance = xstart + r

        return poly, x_cut, right_distance, left_distance
        
        """
        
def cylinder(r,h, l, c, angle = 90, xstart=None, stepsize = None):
    
    angle = math.radians(angle)
    dxi = l/math.sin(angle)
    dyi = l/math.cos(angle)
    l_sign = math.copysign(1,l)
    
   
    if not stepsize:
        stepsize = c
    if not xstart:
        xstart = None
    actual_pos = -r
    x_rightside_distance = 0
    final_poly = []
    poly_len = 0
    while True:
        
        actual_pos += stepsize
        print(actual_pos)
        dx = r * 2 * math.sqrt(1 - (actual_pos / r) ** 2) * math.sin(dxi/ (2*r))
        
        dl = dx*dyi/math.sqrt(dx**2 + dyi**2)*l_sign
        new_angle = math.atan(dyi/dx)
        print(dyi)  
        print("angle")
        print(new_angle)
       
        
        poly, x_rightside_distance, x_leftside_distance, x_cut_list = simple(dl,c,math.degrees(new_angle),2*stepsize,h,xstart)
        
        print("R/L")
        print(x_rightside_distance)
        print(x_leftside_distance)
        
        xstart = x_rightside_distance
        
        
        
        poly = svg.crop(poly, stepsize*2, h)
        svg.export(poly, stepsize*2, h, "test" + str(actual_pos) + ".svg")
        wearein = -stepsize
        andwannago = -r + poly_len
        dif =   andwannago - wearein
        poly = svg.translate(poly, dif,0)
        poly_len += 2*stepsize 
        final_poly += poly
        
        actual_pos += stepsize
        
        if actual_pos > r - stepsize:
            print(actual_pos)
            break
        
    return final_poly, x_cut_list, x_rightside_distance, x_leftside_distance

#pensar sobro
