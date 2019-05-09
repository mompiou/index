Index
============

Index is a python script that allows you to determine diffraction spot indices from a calibrated TEM diffraction pattern of a known crystal structure. It allows crystal orientation determination when at least 3 non-coplanar diffraction vectors are given.

## Requirements

Python 2.7 with numpy, matplotlib, PIL, PyQt4.


# User guide

Run index-pyqt.py or alternatively, with less features, index.py (use Tkinter)

## Interface

![img1](/img1.png?raw=true)

## Procedure

* Open an image from the menu bar
* Enter the crystal parameters (a,b,c, alpha, beta, gamma)(in Angstroem), or import it from the menu bar. The structure can be modified/added by modifying the structure.txt file. The format is: 

`name a b c alpha beta gamma space group` 

* Enter the space group or use the group given in the structure. It can be changed by modifying the space_group.txt. The format is:

```
name

atom-1-name x1 y1 z1

atom-n-name xn yn zn

```

where `x`, `y` and `z` are the atom positions in the unit cell.

The structure factors are entered in the scattering.txt file with the format

`atom-1-name a1 b1 a2 b2 a3 b3 a4 b4 c`

where the coefficients correspond to the Gaussian decomposition (cf. [TU Graz - Database](http://lampx.tugraz.at/~hadley/ss1/crystaldiffraction/atomicformfactors/formfactors.php)).

* Enter the calibration. It can be modified in the calibration.txt file with the format: 

`name energy camera-length binning product-px-times-d`

`px` is the measured distance in the reciprocal space in pixels and `d` is the interplanar distance in Angstroem.
* Click on the image to set the reference point. Use zoom, `reset points` or `reset all` (view and points), if necessary.
* Set the `number of spots` field corresponding to X times the shortest distance in the reciprocal space (useful if you have a systematic diffraction row to gain in precision)
* Click on the diffracted spot.  The output box `distance, inclination` gives the interplanar distance measured and the inclination angle with respect to the tilt axis of the TEM holder taken here along the vertical direction.
* Click on `Find diffraction spots` to identify the diffracted plane (by default the script will search for planes with indices smaller than 5, but it can be changed in the `max indices` field). The output gives in the `Theo distance` box, the interplanar distance, the 3 indices of the planes and the spot intensity (depends on the atomic structure factor you enter in space_group.txt)
* Optional to do automatic indexation using at least three non coplanar diffraction vectors:
	* Select `distance, inclination` and a diffraction spot.
	* Fill the alpha-tilt field (along y-axis here).
	* Add a spot. The field `Diffraction spots` will show `tilt angle, inclination angle, h,k,l`.
	* Remove spots if needed.
	* Select at least 3 spots (and less than 5)
	* Get the orientation and get `Phi1, phi, Phi2, Mean angular deviation, Orthogonality, Residual`. `Mean angular deviation` measures the mean angle between calculated and observed diffraction vector (should be small typically 1°). `Orthogonality` is a measure of the orthogonality of the three x,y,z axies (should be very close to 1). A `residual` value is expected if the number of spots is more than 3 (least square minimization).	
	
* Use these data to draw stereographic projection using [stereo-proj](https://github.com/mompiou/stereo-proj).
* Plot the diffraction spectrum (for a given "maximum indices" value) from the menu bar.




