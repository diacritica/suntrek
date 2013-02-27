suntrek
=======

A Star Trek like interface to our Sun's activity

Scientific advisor in Space Weather: Angela Rivera Campos @ghilbrae

Sinopsis
--------

The USS Enterprise NCC-1701-E arrives to a solar system that is governed by a star with suspicious behaviour. The crew has instructions to collect data for at least several days and send a report to Starfleet Command. What they don't know is that this star is an exact clone of Earth's Sun...

How to test it (on Linux distributions)
---------------------------------------

* Be sure to have python2 installes, as well as python-requests and python-imaging.

* In scripts folder execute run.sh. This script will fetch all data that is currently supported. It should take some minutes.

* After a successful run.sh execution, run generate.py script in web/test/ folder. It should take a second.

* Open index.html in web/test folder.

How to test it (online)
---------------------------------------

You can visit http://suntrek.diacritica.net to get a general idea. 

The characteristic LCARS Star Trek interface will come up shortly.


Data shown (planned)
--------------------

* Animated gifs showing the Sun through filters LASCO/C2, EIT 304A, EIT 195A, EIT 171A and EIT 284A. [http://sohowww.nascom.nasa.gov/data/realtime/gif/] 

* Picture of the Sun with last 24h sunspots + number of sunspots [http://www.spaceweather.com/] and [http://www.spaceweather.com/images2013/]

* Chart depicting GOES-13 Solar Particle Flux for the last 24h [http://www.swpc.noaa.gov/ftpdir/lists/particle/]

* Chart depicting GOES-13 Solar Electron Flux for the last 24h [http://www.swpc.noaa.gov/ftpdir/lists/particle/]

* Chart depicting GOES-14 Solar X-ray Flux for the last 24h [http://www.swpc.noaa.gov/ftpdir/lists/xray/]

* Chart depicting Solar Cycle Progression for the last 12 years (archive) + prediction for the next 5 years [http://www.swpc.noaa.gov/SolarCycle/]

* List of recent alerts regarding solar activity [http://www.swpc.noaa.gov/alerts/archive/current_month.html]

* 3-day Forecast [http://www.swpc.noaa.gov/ftpmenu/forecasts/three_day.html]

* Current conditions (solar wind, X-ray solar flares) [http://www.swpc.noaa.gov/ftpdir/lists/ace/ace_swepam_1m.txt]