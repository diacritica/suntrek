#!/usr/bin/python
# -*- coding: utf-8 -*-

from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('suntrek', 'jinjatemplates'))

# INDEX file
indextemplate = env.get_template('index.html')
indexfile = open("index.html","w")
indexfile.write(indextemplate.render())
indexfile.close()

#EIT file
eitfilterstemplate = env.get_template('eitfilters.html')
eitfiltersfile = open("eitfilters.html","w")
eitfiltersfile.write(eitfilterstemplate.render())
eitfiltersfile.close()

#Particles file
particlefluxtemplate = env.get_template('particleflux.html')
particlefluxfile = open("particleflux.html","w")

solarparticlep10flux = open('output/solarparticleP10flux.txt','r').read()
solarparticlep100flux = open('output/solarparticleP100flux.txt','r').read()

result = particlefluxtemplate.render(dataseries01=solarparticlep10flux, dataseries02=solarparticlep100flux)

particlefluxfile.write(result)
particlefluxfile.close()

#Electrons file
electronfluxtemplate = env.get_template('electronflux.html')
electronfluxfile = open("electronflux.html","w")

solarelectron08flux = open('output/solarelectron08flux.txt','r').read()
solarelectron20flux = open('output/solarelectron20flux.txt','r').read()

result = electronfluxtemplate.render(dataseries01=solarelectron08flux, dataseries02=solarelectron20flux)

electronfluxfile.write(result)
electronfluxfile.close()

#XRayy file
xrayfluxtemplate = env.get_template('xrayflux.html')
xrayfluxfile = open("xrayflux.html","w")

solarxrayshortflux = open('output/solarxrayshortflux.txt','r').read()
solarxraylongflux = open('output/solarxraylongflux.txt','r').read()

result = xrayfluxtemplate.render(dataseries01=solarxrayshortflux, dataseries02=solarxraylongflux)

xrayfluxfile.write(result)
xrayfluxfile.close()


#Sunspot file
sunspotstemplate = env.get_template('sunspots.html')
sunspotsfile = open("sunspots.html","w")

sunspotlabels = open('output/sunspot_labels.txt','r').read()

result = sunspotstemplate.render(dataseries01=sunspotlabels)

sunspotsfile.write(result)
sunspotsfile.close()
