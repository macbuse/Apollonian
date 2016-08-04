# Apollonian

[Inkscape](https://inkscape.org/en/) extension to make [Apollonian gaskets](https://en.wikipedia.org/wiki/Apollonian_gasket).

###Example Inkscape file

[example Inkscape file](https://github.com/macbuse/Apollonian/blob/master/apollonian.svg)


##Installation 

1. Edit the first line of apollon_inx.py to point to your python installation if you don't use [Anaconda](https://www.continuum.io/downloads) on OSX.
1. Copy the .inx and all the .py to  inkscape extensions folder :
For OS X - $HOME/.config/inkscape/extensions
1. Open Inkscape. 
1. Activate via the **Examples** submenu of **Extensions** menu.

##Dependencies

Needs Anaconda python on OS X.

##Notes

The module apollon_inx.py wraps Ludger Sandig's 
[code](https://lsandig.org/blog/2014/08/apollon-python/)
for generating the circles of the gasket.
In particular a slightly modified module ag.py.
