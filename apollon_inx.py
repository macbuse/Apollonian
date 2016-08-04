#!$HOME/anaconda/bin/python
# -*- coding: utf-8 -*-
'''
Ripped from template.py 
- makes a "zenagon"
'''

import inkex       # Required
import simplestyle # will be needed here for styles support
import os          # here for alternative debug method only - so not usually required.
import random

import ag


__version__ = '0.1'

inkex.localize()



### Your helper functions go here


def cplxs2pts(zs):
    tt = []
    for z in zs:
        tt.extend([z.real,z.imag])
    return tt


def  zen_tris(t = .1,
           depth=10,
           base_triangle=[0,200,200J],
           edges=True):
    
    tris  = [ base_triangle[:] ]
    
    indxs = [0,1,2,0]
    edges = zip(indxs, indxs[1:])
    for k in range(depth):
        tt = tris[-1]
        tris.append([ t*tt[i]  + (1-t)*tt[j] for i,j in edges] )
    
    return tris
        
    
def zengon(t = .1,
           depth=10,
           base_triangle=[0,200,200J],
           edges=True):
    
    pts  = base_triangle[:]
    pts.append(base_triangle[0])
    
    for k in range(depth*3):
        pts.append(t*pts[-2] + (1-t)*pts[-3])
    
    tx,ty = pts[0].real,pts[0].imag
    if not edges:
         pts = pts[3:]
    
    pts = ['%.2f,%.2f'%(z.real,z.imag) for z in pts ]
    return  "M %f %f L %s  "%(tx,ty,' '.join(pts))
      
    


class Myextension(inkex.Effect): # choose a better name
    
    def __init__(self):
        " define how the options are mapped from the inx file "
        inkex.Effect.__init__(self) # initialize the super class
        
        # Two ways to get debug info:
        # OR just use inkex.debug(string) instead...
        try:
            self.tty = open("/dev/tty", 'w')
        except:
            self.tty = open(os.devnull, 'w')  # '/dev/null' for POSIX, 'nul' for Windows.
            # print >>self.tty, "gears-dev " + __version__
            
        # list of parameters defined in the .inx file
        self.OptionParser.add_option("-d", "--depth",
                                     action="store", type="int",
                                     dest="depth", default=3,
                                     help="command line help")
        
        self.OptionParser.add_option("", "--c1",
                                     action="store", type="float",
                                     dest="c1", default=2.0,
                                     help="command line help")
        
        self.OptionParser.add_option("", "--c2",
                                     action="store", type="float",
                                     dest="c2", default=3.0,
                                     help="command line help")
        
        self.OptionParser.add_option("", "--c3",
                                     action="store", type="float",
                                     dest="c3", default=3.0,
                                     help="command line help")
        
        
        self.OptionParser.add_option("-x", "--shrink",
                                     action="store", type="inkbool", 
                                     dest="shrink", default=True,
                                     help="command line help")
        
        # here so we can have tabs - but we do not use it directly - else error
        self.OptionParser.add_option("", "--active-tab",
                                     action="store", type="string",
                                     dest="active_tab", default='title', # use a legitmate default
                                     help="Active tab.")
        
 
           
    def calc_unit_factor(self):
        """ return the scale factor for all dimension conversions.
            - The document units are always irrelevant as
              everything in inkscape is expected to be in 90dpi pixel units
        """
        # namedView = self.document.getroot().find(inkex.addNS('namedview', 'sodipodi'))
        # doc_units = self.getUnittouu(str(1.0) + namedView.get(inkex.addNS('document-units', 'inkscape')))
        unit_factor = self.getUnittouu(str(1.0) + self.options.units)
        return unit_factor


### -------------------------------------------------------------------
### Main function and is called when the extension is run.

    
    def effect(self):

        #set up path styles
        path_stroke = '#DD0000' # take color from tab3
        path_fill   = 'none'     # no fill - just a line
        path_stroke_width  = 1. # can also be in form '0.6mm'
        page_id = self.options.active_tab # sometimes wrong the very first time
        
        style_curve = { 'stroke': path_stroke,
                 'fill': 'none',
                 'stroke-width': path_stroke_width }
        
        styles = [ { 'stroke': 'none', 'fill': '#000000', 'stroke-width': 0 },
                   { 'stroke': 'none',  'fill': '#FFFF00', 'stroke-width': 0 }]
        
        styles = [simplestyle.formatStyle(x) for x in styles]

        

        # This finds center of current view in inkscape
        t = 'translate(%s,%s)' % (self.view_center[0], self.view_center[1] )
        
        # Make a nice useful name
        g_attribs = { inkex.addNS('label','inkscape'): 'zengon' + "_%d"%(self.options.depth),
                      inkex.addNS('transform-center-x','inkscape'): str(0),
                      inkex.addNS('transform-center-y','inkscape'): str(0),
                      'transform': t,
                      'style' : simplestyle.formatStyle(style_curve),
                      'info':'N: '}
        # add the group to the document's current layer
        topgroup = inkex.etree.SubElement(self.current_layer, 'g', g_attribs )
        
        ff = 200
        circles = ag.main(c1=self.options.c1,
                         c2=self.options.c2,
                         c3=self.options.c3,
                         depth=self.options.depth)
        
        if self.options.shrink:
            circles = circles[1:]
            for cc in circles:
                cc.r = abs(cc.r)
                if cc.r >.5:
                    cc.r -= .1
                else:
                    cc.r *= .9
                
            
        for c in circles:
            
            cx, cy, r = c.m.real, c.m.imag, abs(c.r)
        
            cx, cy, r  = ff*cx , ff*cy, ff*r
            draw_SVG_circle(topgroup,r,cx,cy,'apo')          
                         
        
        
def xy_para(t, vx=50,vy=50):
    return vx*t, vy*t - 5*t*t


def draw_SVG_circle(parent, r, cx, cy, name):
    " structre an SVG circle entity under parent "
    circ_attribs = { 'cx': str(cx), 'cy': str(cy), 
                    'r': str(r),
                    inkex.addNS('label','inkscape'): name}
    
    
    circle = inkex.etree.SubElement(parent, inkex.addNS('circle','svg'), circ_attribs )    


if __name__ == '__main__':
    e = Myextension()
    e.affect()


