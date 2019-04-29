Index
============

Index is a python script that allows you to determine diffraction spot indices from a calibrated TEM diffraction pattern of a known crystal structure. Index is very helpful to determine the stereographic projection quite rapidly. 

## Requirements

* Python 2.7 with numpy, matplotlib, PIL, Tkinter (use Enthought Canopy or Anaconda)
* Mac Users need Active Tcl installed
* If you want to use the script index-pyqt.py you'll need to install PyQt4.

# User guide

## Interface

![img1](/img1.png?raw=true)

## Procedure

* Open an image from the menu bar
* Enter the crystal parameters (a,b,c, alpha, beta, gamma)(in angstroem), or import it from the menu bar. The structure can be modified/added by modifying the structure.txt file. The format is: name a b c alpha beta gamma space group. 
* Enter the space group or use the group given in the structure. It can be changed by modifying the space_group.txt. The format is:

name 

atomic-structure-factor-1 x1 y1 z1

atomic-structure-factor-n xn yn zn

where x, y and z are the atom positions in the unit cell.

* Enter the calibration. It can be modified in the calibration.txt file with the format: name energy camera-length binning product-px-times-d (px is the measured distance in the reciprocal space in pixels and d is the interplanar distance in angstroem)
* Click on the image to set the reference point
* Set the "number of spots" field corresponding to X times the shortest distance in the reciprocal space (useful if you have a systematic diffraction row to gain in precision)
* Click on the diffracted spot.  The output window gives the interplanar distance measured and the inclination angle with respect to the tilt axis of the TEM holder taken here along the vertical direction)
* Click on calculate to identify the diffracted plane (by default the script will search for planes with indices smaller than 5, but it can be changed in the "max indices" field). The output gives, the interplanar distance, the 3 indices of the planes and an arbitrary intensity (depends on the atomic structure factor you enter in space_group.txt)
* Use these data to draw stereographic projection using [stereo-proj](https://github.com/mompiou/stereo-proj).
* Plot the diffraction spectrum (for a given "maximum indices" value) from the menu bar.




