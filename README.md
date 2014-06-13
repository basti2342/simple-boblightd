simple boblightd
================

This is a pretty hackish implementation of the [boblight](https://code.google.com/p/boblight/) deamon.

It is designed to provide basic boblight functionality and to control IKEA dioder LED strips using an Arduino.

It is based upon Daniel Kennetts ["Nerd++: Controlling Dioder RGB LED Strips With Arduino (Pt. 1)"](http://ikennd.ac/blog/2011/09/arduino-dioder-part-one/). His Arduino sketch can be found (here on GitHub)[https://github.com/iKenndac/Arduino-Dioder-Playground/tree/master/Arduino%20Projects/FourChannelRGBSmartListener].

Disclaimer:
-----------
This is most definitely not the way to use boblight and there are ways to achieve similar results using the official boblightd, but I needed somehting quick and dirty to communicate with the Arduino and filter/smooth colors and intensity.
