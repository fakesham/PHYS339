# -*- coding: utf-8 -*-
"""

@author: mark.orchard-webb
"""

import urllib
import socket
import numpy
import matplotlib.pyplot as p

def get_histogram():
    workstation=socket.gethostname();
    params=urllib.urlencode({"workstation":workstation})
    f = urllib.urlopen("http://132.206.252.3/339/intro-get_histogram.php",params)
    result = f.read()
    if not result[0:9] == "HISTOGRAM":
        print result
        return False
    lines = result.split("\n")
    words = lines[0].split(" ")
    rows = int(words[1])
    columns = int(words[2])
    print("rows = %d, len(lines) = %d"%(rows,len(lines)))
    if not (rows+2) == len(lines):
        print "inconsistent data"
        return False
    data = numpy.zeros([rows,columns])
    for i in range(rows):
        words = lines[1+i].split(" ")
        for j in range(columns):
            data[i][j] = int(words[j])
    return data

h = get_histogram()
rows = numpy.size(h,0)
cols = numpy.size(h,1)
guesses = numpy.linspace(0,cols-1,cols)
# plot the 3rd histogram
p.bar(guesses-0.5,h[2,:],width=1)
p.xlabel("Number of guesses")
p.ylabel("Frequency")
p.xlim(-0.5,cols-0.5)
print h