from numarray import *
import numarray.random_array
from pystats import *

def run(d):
	print "----"
	print "dataset =", d
	print "mean =", mean(d)
	print "median =", median(d)
	print "mode(s) =", mode(d)
	print "range =", rang(d)
	print "midrange =", midrange(d)
	print "mean deviation =", meandev(d)
	print "standard deviation =", stddev(d)
	print "variance =", variance(d)
	print "bias-corrected variance =", bvariance(d)
	
	print "----\n"

o = random_array.random(3) * 10
e = random_array.random(4) * 10
ao = random_array.random([3,3]) * 10
ae = random_array.random([3,4]) * 10
h = array([[1, 2, 3], [1, 4, 5], [3, 2, 8], [1, 8, 5]])

run(o)
run(e)
run(ao)
run(ae)
run(h)

print "----\nNormal Distribution"

r = normpdf(0, 0, 1)
print "normpdf(0, 0, 1) =", r

s = normcdf(1, 0, 1) - normcdf(-1, 0, 1)
print "normcdf(1, 0, 1) - normcdf(-1, 0, 1) =", s

t = normicdf(s)
print "normicdf(.) =", t

print "normcdf(.) =", normcdf(t, 0, 1)
print "----"

print "\n----\nCauchy Distribution"

r = cauchypdf(0, 0, 1)
print "cauchypdf(0, 0, 1) =", r

s = cauchycdf(1, 0, 1) - cauchycdf(-1, 0, 1)
print "cauchycdf(1, 0, 1) - cauchycdf(-1, 0, 1)=", s

print "----"

print "\n----\nChi Distribution"

r = chipdf(10, 0, 1, 50)
print "chipdf(10, 0, 1, 50) =", r

s = chicdf(10, 0, 1, 50)
print "chicdf(10, 0, 1, 50) =", s

print "chimean(0, 1, 50) =", chimean(0, 1, 50)
print "chivar(0, 1, 50) =", chivar(0, 1, 50)

print "----"

print "\n----\nCosine Distribution"

r = cospdf(0, 0, 1)
print "cospdf(0, 0, 1) =", r

s = coscdf(1, 0, 1) - coscdf(-1, 0, 1)
print "coscdf(1, 0, 1) - coscdf(-1, 0, 1)=", s

print "----"

print "\n----\nExponential Distribution"

print "exppdf(4, 1, 2) =", exppdf(4, 1, 2)
print "expcdf(4, 1, 2) =", expcdf(4, 1, 2)
print "expmean(1, 2) =", expmean(1, 2)
print "expvar(1, 2) =", expvar(1, 2)
print "exprand(1, 2) =", exprand(1, 2)

print "----"

print "\n----\nBinomial Distribution"

print "binompdf(4, 0.5, 8) =", binompdf(4, 0.5, 8)
print "binommean(0.5, 8) =", binommean(0.5, 8)
print "binomvar(0.5, 8) =", binomvar(0.5, 8)

print "----"

print "\n----\nNegative Binomial Distribution"

print "nbinompdf(8, 0.5, 4) =", nbinompdf(8, 0.5, 4)
print "nbinommean(0.5, 4) =", nbinommean(0.5, 4)
print "nbinomvar(0.5, 4) =", nbinomvar(0.5, 4)

print "----"

print "\n----\nGeometric Distribution"

print "geopdf(4, 0.5) =", geopdf(4, 0.5)
print "geomean(0.5) =", geomean(0.5)
print "geovar(0.5) =", geovar(0.5)

print "----"

print "\n----\nLogarithmic Distribution"

print "logpdf(4, 0.5) =", logpdf(4, 0.5)
print "logmean(0.5) =", logmean(0.5)
print "logvar(0.5) =", logvar(0.5)

print "----"

print "\n----\nPoisson Distribution"

print "poispdf(4, 2) =", poispdf(4, 2)
print "poismean(2) =", poismean(2)
print "poisvar(2) =", poisvar(2)

print "----"