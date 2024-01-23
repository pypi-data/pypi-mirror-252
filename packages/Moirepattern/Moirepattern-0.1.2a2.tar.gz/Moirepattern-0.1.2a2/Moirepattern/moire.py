
from . import constructor as cns
from . import svgop as svg
from . import vis
import math

class Structure:
    def __init__(self,c):
        self.components = [] #Component is a moiré pattern
        self.rows = 1 
        self.columns = 1
        self.c = c
        

    class Moire:
        def __init__(self, d, c, angle):
            self.d = d
            self.c = c
            self.angle = angle
            self.type = ""

        def set_size(self, xsize, ysize):
            self.xsize = xsize
            self.ysize = ysize
        
        def make(self, type, xstart = None):
            if not self.xsize or not self.ysize:
                print("Error: size not set, please use set_size() first")
            
            if type == "simple":
                self.type = "simple"
                poly, x_rightside_distance, x_leftside_distance, x_cut_list  = cns.simple(self.d, self.c, self.angle, self.xsize, self.ysize, xstart)    
                self.poly = poly
                self.x_rightside_distance = x_rightside_distance
                self.x_leftside_distance = x_leftside_distance
                self.x_cut_list = x_cut_list
            elif type == "cylinder":
                self.type = "cylinder"
                poly, x_cut_list, x_rightside_distance, x_leftside_distance= cns.cylinder(self.xsize/2, self.ysize, self.d, self.c, self.angle, xstart)
                self.poly = poly
                self.x_rightside_distance = x_rightside_distance
                self.x_leftside_distance = x_leftside_distance
                self.x_cut_list = x_cut_list

    def create(self, d, angle, xsize, ysize, type = "simple", xstart = None):
    
        pattern = self.Moire(d, self.c, angle)
        pattern.set_size(xsize, ysize)
        self.components.append(pattern)
        pattern.make(type, xstart)
        
    def export_component(self, index, filename):
        filename = filename + ".svg"
        basename = filename + "_base.svg"
        poly = self.components[index].poly
        poly = svg.crop(poly, self.components[index].xsize, self.components[index].ysize)
        svg.export(poly, self.components[index].xsize, self.components[index].ysize, filename)
        
        base = cns.base(self.components[index].c, self.components[index].xsize, self.components[index].ysize)
        base = svg.crop(base, self.components[index].xsize, self.components[index].ysize)
        svg.export(base, self.components[index].xsize, self.components[index].ysize, basename)
    
    def extend(self, newangle, lsize, d = 0):
        d = self.components[-1].d
        if self.components == []:
            print("Error: no components to extend")
            return
        if self.components[-1].type == "simple":
            #get last x
            xstart = self.components[-1].x_rightside_distance
            actual_angle = self.components[-1].angle
            actual_d = self.components[-1].d
            if self.components[-1].angle % 90 != 0 and newangle % 90 != 0 :
                l1 = actual_d
                l1_angle = actual_angle
                l2_angle = newangle
                l1_angle = math.radians(l1_angle)
                l2_angle = math.radians(l2_angle)
                l2 = l1 * math.cos(l2_angle)/math.cos(l1_angle)
                newd = l2
            else:
                newd = d
                newangle  = actual_angle
            self.create(newd, newangle, lsize, self.components[-1].ysize, "simple", xstart)

            self.columns += 1
        else:
            print("Error: last component is not simple")
            return
    
    def export(self, filename):
        size = 0
        poly0 = []
        for i in range(self.columns):
            size += self.components[i].xsize
            if i == 0:
                moire = self.components[i]
                poly = moire.poly
                poly = svg.crop(poly, moire.xsize, moire.ysize)
                poly0 = poly
                continue
            else:
                moire = self.components[i]
                #get poly and crop it, then add size
                poly = moire.poly
                poly = svg.crop(poly, moire.xsize, moire.ysize)
                poly = svg.translate(poly, size/2 , 0)
                poly0 += poly
                #move poly to center
                poly0 = svg.translate(poly0, -moire.xsize/2 , 0)
      
        svg.export(poly0, size, self.components[0].ysize, filename + ".svg")
        base = cns.base(self.c, size, self.components[0].ysize)
        base = svg.crop(base, size, self.components[0].ysize)
        svg.export(base, size, self.components[0].ysize, filename + "_base.svg")
                       
    def view(self,distance):
        size = 0
        #join all components poly
        for i in range(self.columns):
            size += self.components[i].xsize
            if i == 0:
                moire = self.components[i]
                poly = moire.poly
                poly = svg.crop(poly, moire.xsize, moire.ysize)
                poly0 = poly
                continue
            else:
                moire = self.components[i]
                #get poly and crop it, then add size
                poly = moire.poly
                poly = svg.crop(poly, moire.xsize, moire.ysize)
                poly = svg.translate(poly, size/2 , 0)
                poly0 += poly
                #move poly to center
                poly0 = svg.translate(poly0, -moire.xsize/2 , 0)
        #translate to center:
        
        base = cns.base(self.c, size, self.components[0].ysize)
        vis.visualize(poly0, base, distance )