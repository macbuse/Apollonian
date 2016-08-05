# Apollonian

[Inkscape](https://inkscape.org/en/) extension to make Apollonian gaskets.
Tested Inkscape 0.91.

>An Apollonian gasket can be constructed as follows. Start with three circles C1, C2 and C3, each one of which is tangent to the other two (in the general construction, these three circles can be any size, as long as they have common tangents). Apollonius discovered that there are two other non-intersecting circles, C4 and C5, which have the property that they are tangent to all three of the original circles – these are called Apollonian circles. Adding the two Apollonian circles to the original three, we now have five circles. 

>Take one of the two Apollonian circles – say C4. It is tangent to C1 and C2, so the triplet of circles C4, C1 and C2 has its own two Apollonian circles. We already know one of these – it is C3 – but the other is a new circle C6.
In a similar way we can construct another new circle C7 that is tangent to C4, C2 and C3, and another circle C8 from C4, C3 and C1. This gives us 3 new circles. We can construct another three new circles from C5, giving six new circles altogether. Together with the circles C1 to C5, this gives a total of 11 circles.

>Continuing the construction stage by stage in this way ad infinituum  one obtains  a set of circles which is an Apollonian gasket.

Source: [Wikipedia](https://en.wikipedia.org/wiki/Apollonian_gasket)


###Example Inkscape file

[example Inkscape file](https://github.com/macbuse/Apollonian/blob/master/apollonian.svg)


##Installation 

1. Edit the first line of apollon_inx.py to point to your python installation if you don't use [Anaconda](https://www.continuum.io/downloads) on OSX.
1. Copy the .inx and all the .py to  inkscape extensions folder :
For OS X - $HOME/.config/inkscape/extensions
1. Open Inkscape. 
1. Activate via the **Render** submenu of **Extensions** menu.

##Dependencies

Needs Anaconda python on OS X but should work with any python 2.7* installation
after modifying as per installation instructions.

##Notes

The module apollon_inx.py wraps Ludger Sandig's 
[code](https://lsandig.org/blog/2014/08/apollon-python/)
for generating the circles of the gasket.
In particular a slightly modified module ag.py.
