#!$HOME/anaconda/bin/python
# -*- coding: utf-8 -*-
'''
Ripped from template.py 
- makes an apollonian gasket
'''

import inkex       # Required
import simplestyle # will be needed here for styles support
import ag

__version__ = '0.0'

inkex.localize()


### Your helper functions go here


def cplxs2pts(zs):
    tt = []
    for z in zs:
        tt.extend([z.real,z.imag])
    return tt


def draw_SVG_circle(parent, r, cx, cy, name):
    " structre an SVG circle entity under parent "
    circ_attribs = { 'cx': str(cx), 'cy': str(cy), 
                    'r': str(r),
                    inkex.addNS('label','inkscape'): name}
    
    
    circle = inkex.etree.SubElement(parent, inkex.addNS('circle','svg'), circ_attribs )
    
    
class Myextension(inkex.Effect): # choose a better name
    
    def __init__(self):
        " define how the options are mapped from the inx file "
        inkex.Effect.__init__(self) # initialize the super class
        
            
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

        
        # This finds center of current view in inkscape
        t = 'translate(%s,%s)' % (self.view_center[0], self.view_center[1] )
        
        # add a group to the document's current layer
        #all the circles inherit style from this group
        g_attribs = { inkex.addNS('label','inkscape'): 'zengon' + "_%d"%(self.options.depth),
                      inkex.addNS('transform-center-x','inkscape'): str(0),
                      inkex.addNS('transform-center-y','inkscape'): str(0),
                      'transform': t,
                      'style' : simplestyle.formatStyle(style_curve),
                      'info':'N: '}
        topgroup = inkex.etree.SubElement(self.current_layer, 'g', g_attribs )
        
        
        circles = ag.main(c1=self.options.c1,
                         c2=self.options.c2,
                         c3=self.options.c3,
                         depth=self.options.depth)
        
        #shrink the circles so they don't touch
        #useful for laser cutting
        
        if self.options.shrink:
            circles = circles[1:]
            for cc in circles:
                cc.r = abs(cc.r)
                if cc.r >.5:
                    cc.r -= .1
                else:
                    cc.r *= .9
                
        scale_factor = 200
        for c in circles:  
            cx, cy, r = c.m.real, c.m.imag, abs(c.r)
            
            #rescale and add circle to document
            cx, cy, r  = scale_factor*cx , scale_factor*cy, scale_factor*r
            draw_SVG_circle(topgroup,r,cx,cy,'apo')          
                         
         


if __name__ == '__main__':
    e = Myextension()
    e.affect()


