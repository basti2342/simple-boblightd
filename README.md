simple boblightd
================

This is a pretty hackish implementation of the [Boblight](https://code.google.com/p/boblight/) deamon.

It is designed to provide basic Boblight functionality and to control IKEA dioder LED strips using an Arduino.

It is based upon Daniel Kennetts ["Nerd++: Controlling Dioder RGB LED Strips With Arduino (Pt. 1)"](http://ikennd.ac/blog/2011/09/arduino-dioder-part-one/). His Arduino sketch can be found [here on GitHub](https://github.com/iKenndac/Arduino-Dioder-Playground/tree/master/Arduino%20Projects/FourChannelRGBSmartListener).

Disclaimer
----------
This is most definitely not the way to use Boblight and there are ways to achieve similar results using the official boblightd, but I needed somehting quick and dirty to communicate with the Arduino and filter/smooth colors and intensity.

Dependencies
------------
* [pyserial](http://pyserial.sourceforge.net/)

`pip install pyserial`

How to use it
-------------
`$ ./boblightd.py localhost:5555`

Now you can start a Boblight client, e.g.

* `$ boblight-X11 -slocalhost:5555 -y off`
* [XBMC Boblight addon](http://wiki.xbmc.org/index.php?title=Add-on:XBMC_Boblight) (see notes below!)

Notes
-----
* a timeout prevents the XBMC Boblight addon from connecting to simple boblightd. You can increase the timeout in the connect method in `~/.xbmc/addons/script.xbmc.boblight/resources/lib/boblight.py` (currently on line 132)

