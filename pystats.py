#--------
# pystat
# A full-featured statistical analysis
# and inference module for Python.
# Intended to be used alongside the 
# numarray package, the succesor to 
# Numeric.
#
# Author: Michael Bommarito 
#	  michael.bommarito@gmail.com
# Revision: 20050621
# 
# numarray: http://www.stsci.edu/resources/software_hardware/numarray
#--------

from cmath import *
from random import random
from numpy import *
#from numarray import *
from inspect import isfunction

# Constants
sqrt2 = sqrt(2.)
sqrtpi = sqrt(pi)
isqpi = 1./(sqrt2*sqrtpi)

# Emulated ternary operator
# q(cond, on_true, on_false)
# cond: expression
# on_true: expression
# on_false: expression
def q(cond, on_true, on_false):
    if cond: 
        try:
        	return eval(on_true)
        except TypeError:
        	try:
        		return apply(on_true)
        	except TypeError:
        		return on_true
    else:
		try:
			return eval(on_false)
		except TypeError:
			try:
				return apply(on_false)
			except TypeError:
				return on_false

# Arithmetic mean
# mean(data)
# data: array
def mean(data):
	return data.sum()/float(data.size())

# Median value
# median(data)
# data: array
def median(data):
	d = sort(ravel(data))
	n = data.size()
	return q(n % 2 == 0, (d[(n/2)-1]+d[n/2])/2, d[n/2])

# Modes
# mode(data, lim)
# data: array
def mode(data):
	data = sort(ravel(data))
	cur = 1
	freq = {}
	freq[data[0]] = 1
	m = [data[0]]
	for i in range(1, len(data)):
		if data[i] in freq:
			freq[data[i]] += 1
		else:
			freq[data[i]] = 1

		if freq[data[i]] > cur:
			cur = freq[data[i]]
			m = [data[i]]
		elif freq[data[i]] == cur:
			m.append(data[i])

	return q(len(m) == len(data), None, q(len(m) == 1, m[0], m))

# Range
# rang(data) (funny, right?  built-in function problems)
# data: array
def rang(data):
	try:
		data = sort(ravel(data))
		return (data[data.size()-1]-data[0])
	except TypeError:
		return 

# Midrange
# midrange(data)
# data: array
def midrange(data):
	data = sort(ravel(data))
	return (data[data.size()-1]+data[0])/2.0

# Square
# sqr(s)
# s: s is in C
def sqr(s):
	return pow(s, 2)

# Biased variance
# variance(data)
# data:array
def variance(data):
	return sum(map(lambda x: pow(x-mean(data), 2), ravel(data)))/data.size()

# Bias-corrected variance
# bvariance(data)
# data:array
def bvariance(data):
	return sum(map(lambda x: pow(x-mean(data), 2), ravel(data)))/(data.size()-1)

# Standard deviation
# stddev(data)
# data:array
def stddev(data):
	return sqrt(variance(data))

# Mean deviation
# meandev(data)
# data: array
def meandev(data):
	return sum(map(lambda x: x-mean(data), ravel(data)))/data.size()

# Gamma function
# gamma(x)
# x: float
def gamma(x):
	tp = 2 * pi
	r = exp(log(x) + log(sinh(1.0 / x))) + exp(-6 * log(810 * x))
	n = log(x / e) + log(sqrt(r))
	o = x * log(exp(n)) + log(sqrt(tp / x))
	return exp(o)

# Incomplete gamma function
# igamma(x, a)
# x: float
# a: float
def igamma(x, a):
	r = 1./gamma(x)
	#t^(a-1)*exp(-t)
	s = 0.0
	step = (abs(a*100) - a)/100.
	for i in range(a, abs(a*100)):
		t = i * step
		s += pow(t, a-1.)*exp(-t)
	return r*s/step

#--
# Beta Distribution
#--

# PDF
# betapdf(x, a, b)
# x: float
# a: float, location parameter
# b: float, scale parameter
def betapdf(x, a, b, c, d):
	return (1./(2.*b*gamma(c)))*abs(pow(((x-a)/b), c-1.))*exp(-abs((x-a)/b))

#--

#--
# Normal Distribution
#--

# PDF
# normpdf(x, m, s)
# x: float
# m: float, mean
# s: float, standard deviation
def normpdf(x, m, s):
	return exp(-pow((x-m)/s, 2)/2)*(isqpi/s)

# CDF
# Based on Chokri Dridi's algorithm
# http://econwpa.wustl.edu:8089/eps/comp/papers/0212/0212001.pdf
# normcdf(x, m, s)
# x: float
# m: float, mean
# float, standard deviation
def normcdf(x, m, s):
	if x >= 0.:
		return (1.+glquad(0, x/sqrt(2.)))/2.
	else:
		return (1.-glquad(0, -x/sqrt(2.)))/2.

# Composite fifth-order Gauss-Legendre quadrature estimation
def glquad(a, b):
	y = [0, 0, 0, 0, 0]
	x = [-sqrt(245.+14.*sqrt(70.))/21, -sqrt(245.-14.*sqrt(70.))/21, 0, sqrt(245.-14.*sqrt(70.))/21., sqrt(245.+14.*sqrt(70.))/21]
	w = [(322.-13.*sqrt(70.))/900., (322.+13.*sqrt(70.))/900., 128./225., (322.+13.*sqrt(70.))/900, (322.-13.*sqrt(70.))/900.]
	n = 4800
	s = 0
	h = (b-a)/n

	for i in range(0, n, 1):
		y[0] = h * x[0]/2.+(h+2.*(a+i*h))/2.
		y[1] = h * x[1]/2.+(h+2.*(a+i*h))/2.
		y[2] = h * x[2]/2.+(h+2.*(a+i*h))/2.
		y[3] = h * x[3]/2.+(h+2.*(a+i*h))/2.
		y[4] = h * x[4]/2.+(h+2.*(a+i*h))/2.
		
		f = lambda r: (2./sqrt(pi))*exp(-r**2.)
		s = s+h*(w[0]*f(y[0])+w[1]*f(y[1])+w[2]*f(y[2])+w[3]*f(y[3])+w[4]*f(y[4]))/2.
	return s

# Inverse CDF
def normicdf(v):
	if v > 0.5:
		r = -1.
	else:
		r = 1.
	xp = 0.
	lim = 1.e-20
	p = [-0.322232431088, -1.0, -0.342242088547, -0.0204231210245, -0.453642210148e-4]
	q = [0.0993484626060, 0.588581570495, 0.531103462366, 0.103537752850, 0.38560700634e-2]

	if v < lim or v == 1:
		return -1./lim
	elif v == 0.5:
		return 0
	elif v > 0.5:
		v = 1.-v
	y = sqrt(log(1./v**2.))
	xp = y+((((y*p[4]+p[3])*y+p[2])*y+p[1])*y+p[0])/((((y*q[4]+q[3])*y+q[2])*y+q[1])*y+q[0])
	if v < 0.5:
		xp *= -1.
	return xp*r
#--


#--
# Cauchy Distribution
#--

# PDF
# cauchypdf(x, a, b)
# x: float
# a: float, location parameter
# b: float, scale parameter
def cauchypdf(x, a, b):
	return exp(-log(pi)+log(b)+log(1+pow((x-a)/b, 2)))

# CDF
# cauchycdf(x, a, b)
# x: float
# a: float, location parameter
# b: float, scale parameter
def cauchycdf(x, a, b):
	return 0.5+(1./pi)*(arctan((x-a)/b))

def cauchyrand(a, b):
	return a + b*tan(pi*(random()-0.5))
#--

#--
# Cosine Distribution
#--

# PDF
# cospdf(x, a, b)
# x: float
# a: float, location parameter
# b: float, scale parameter
def cospdf(x, a, b):
	return (1./(2*pi*b))*(1.+cos((x-a)/b))

# CDF
# coscdf(x, a, b)
# x: float
# a: float, location parameter
# b: float, scale parameter
def coscdf(x, a, b):
	return (1./(2*pi))*(pi+((x-a)/b))+sin((x-a)/b)
#--


#--
# Beta Distribution
#--

# PDF
# betapdf(x, a, b)
# x: float
# a: float, location parameter
# b: float, scale parameter
def betapdf(x, a, b, c, d):
	return (1./(2.*b*gamma(c)))*abs(pow(((x-a)/b), c-1.))*exp(-abs((x-a)/b))

# CDF
# coscdf(x, a, b)
# x: float
# a: float, location parameter
# b: float, scale parameter
def betacdf(x, a, b, c, d):
	pass

x = """
#--#--------
# pystat
# A full-featured statistical analysis
# and inference module for Python.
# Intended to be used alongside the 
# numarray package, the succesor to 
# Numeric.
#
# Author: Michael Bommarito 
#	  michael.bommarito@gmail.com
# Revision: 20050621
# 
# numarray: http://www.stsci.edu/resources/software_hardware/numarray
#--------

from cmath import *		#standard python module
from random import random
from numarray import *	#numarray module - see header
from inspect import isfunction


isqpi = (1.0/(sqrt(2.0*pi)))

# Emulated ternary operator
# q(cond, on_true, on_false)
# cond: expression
# on_true: expression
# on_false: expression
def q(cond, on_true, on_false):
    if cond: 
        try:
        	return eval(on_true)
        except TypeError:
        	try:
        		return apply(on_true)
        	except TypeError:
        		return on_true
    else:
		try:
			return eval(on_false)
		except TypeError:
			try:
				return apply(on_false)
			except TypeError:
				return on_false

# Arithmetic mean
# mean(data)
# data: array
def mean(data):
	return data.sum()/float(data.size())

# Median value
# median(data)
# data: array
def median(data):
	d = sort(ravel(data))
	n = data.size()
	return q(n % 2 == 0, (d[(n/2)-1]+d[n/2])/2, d[n/2])

# Modes
# mode(data, lim)
# data: array
def mode(data):
	data = sort(ravel(data))
	cur = 1
	freq = {}
	freq[data[0]] = 1
	m = [data[0]]
	for i in range(1, len(data)):
		if data[i] in freq:
			freq[data[i]] += 1
		else:
			freq[data[i]] = 1

		if freq[data[i]] > cur:
			cur = freq[data[i]]
			m = [data[i]]
		elif freq[data[i]] == cur:
			m.append(data[i])

	return q(len(m) == len(data), None, q(len(m) == 1, m[0], m))

# Range
# rang(data) (funny, right?  built-in function problems)
# data: array
def rang(data):
	try:
		data = sort(ravel(data))
		return (data[data.size()-1]-data[0])
	except TypeError:
		return 

# Midrange
# midrange(data)
# data: array
def midrange(data):
	data = sort(ravel(data))
	return (data[data.size()-1]+data[0])/2.0


# Mean deviation
# meandev(data)
# data: array
def meandev(data):
	return sum(map(lambda x: x-mean(data), ravel(data)))/data.size()


# Standard deviation
# stddev(data)
# data:array
def stddev(data):
	return sqrt(variance(data))

# Bias-corrected standard deviation
# bstddev(data)
# data:array
def bstddev(data):
	return sqrt(bvariance(data))

# Biased variance
# variance(data)
# data:array
def variance(data):
	return sum(map(lambda x: pow(x-mean(data), 2), ravel(data)))/data.size()

# Bias-corrected variance
# bvariance(data)
# data:array
def bvariance(data):
	return sum(map(lambda x: pow(x-mean(data), 2), ravel(data)))/(data.size()-1)

# Biased skew
# skew(data)
# data:array
def skew(data):
	return sum(map(lambda x: pow(x-mean(data), 3), ravel(data)))/data.size()

# Bias-corrected skew
# bskew(data)
# data:array
def bskew(data):
	return sum(map(lambda x: pow(x-mean(data), 3), ravel(data)))/(data.size()-1)

	
# Gamma function
# gamma(x)
# x: float
def gamma(x):
	tp = 2 * pi
	r = exp(log(x) + log(sinh(1.0 / x))) + exp(-6 * log(810 * x))
	n = log(x / e) + log(sqrt(r))
	o = x * log(exp(n)) + log(sqrt(tp / x))
	return exp(o)

# Incomplete gamma function
# Continued fraction expansion
# igamma(x, a)
# x: float
# a: float
def igamma(a, x):
	if a % 1. == 0. and a < 8:
		a += 0.00001

	r = pow(x, a) * exp(-x)
	s = 1./(x+((1.-a)/(1.+(1./(x+((2.-a)/(1.+(2./(x+((3.-a)/(1.+(3./(x+((4.-a)/(1.+(4./(x+((5.-a)/(1.+(5./+((6.-a)/7.)))))))))))))))))))))
	if a > x + 1:
		return r*s*log(gamma(a))
	else:
		return r*s


#--
# Normal Distribution
#--

# PDF
# normpdf(x, m, s)
# x: float
# m: float, mean
# s: float, standard deviation
def normpdf(x, m, s):
	return exp(-pow((x-m)/s, 2)/2)*(isqpi/s)

# CDF
# Based on Chokri Dridi's algorithm
# http://econwpa.wustl.edu:8089/eps/comp/papers/0212/0212001.pdf
# normcdf(x, m, s)
# x: float
# m: float, mean
# float, standard deviation
def normcdf(x, m, s):
	if x >= 0.:
		return (1.+glquad(0, x/sqrt(2.)))/2.
	else:
		return (1.-glquad(0, -x/sqrt(2.)))/2.

# Composite fifth-order Gauss-Legendre quadrature estimation
def glquad(a, b):
	y = [0, 0, 0, 0, 0]
	x = [-sqrt(245.+14.*sqrt(70.))/21, -sqrt(245.-14.*sqrt(70.))/21, 0, sqrt(245.-14.*sqrt(70.))/21., sqrt(245.+14.*sqrt(70.))/21]
	w = [(322.-13.*sqrt(70.))/900., (322.+13.*sqrt(70.))/900., 128./225., (322.+13.*sqrt(70.))/900, (322.-13.*sqrt(70.))/900.]
	n = 4800
	s = 0
	h = (b-a)/n

	for i in range(0, n, 1):
		y[0] = h * x[0]/2.+(h+2.*(a+i*h))/2.
		y[1] = h * x[1]/2.+(h+2.*(a+i*h))/2.
		y[2] = h * x[2]/2.+(h+2.*(a+i*h))/2.
		y[3] = h * x[3]/2.+(h+2.*(a+i*h))/2.
		y[4] = h * x[4]/2.+(h+2.*(a+i*h))/2.
		
		f = lambda r: (2./sqrt(pi))*exp(-r**2.)
		s = s+h*(w[0]*f(y[0])+w[1]*f(y[1])+w[2]*f(y[2])+w[3]*f(y[3])+w[4]*f(y[4]))/2.
	return s

# Inverse CDF
def normicdf(v):
	if v > 0.5:
		r = -1.
	else:
		r = 1.
	xp = 0.
	lim = 1.e-20
	p = [-0.322232431088, -1.0, -0.342242088547, -0.0204231210245, -0.453642210148e-4]
	q = [0.0993484626060, 0.588581570495, 0.531103462366, 0.103537752850, 0.38560700634e-2]

	if v < lim or v == 1:
		return -1./lim
	elif v == 0.5:
		return 0
	elif v > 0.5:
		v = 1.-v
	y = sqrt(log(1./v**2.))
	xp = y+((((y*p[4]+p[3])*y+p[2])*y+p[1])*y+p[0])/((((y*q[4]+q[3])*y+q[2])*y+q[1])*y+q[0])
	if v < 0.5:
		xp *= -1.
	return xp*r
#--


#--
# Cauchy Distribution
#--

# PDF
# cauchypdf(x, a, b)
# x: float
# a: float, location parameter
# b: float, scale parameter
def cauchypdf(x, a, b):
	return exp(-log(pi)+log(b)+log(1+pow((x-a)/b, 2)))

# CDF
# cauchycdf(x, a, b)
# x: float
# a: float, location parameter
# b: float, scale parameter
def cauchycdf(x, a, b):
	return 0.5+(1./pi)*(arctan((x-a)/b))

def cauchyrand(a, b):
	return a + b*tan(pi*(random()-0.5))
#--

#--
# Chi Distribution
#--
# Distribution Parameters
# a: float | location parameter
# b: float | scale parameter, b > 0
# c: float | shape parameter, 0 < c <= 100

# PDF
# chipdf(x, a, b, c)
# x: float | x > a
def chipdf(x, a, b, c):
	return (pow((x-a)/b, c-1.)*exp(-0.5*pow((x-a)/b, 2)))/(pow(2, (c/2.)-1.)*b*gamma(c/2.))

# CDF
# chicdf(x, a, b, c)
# x: float | x > a
def chicdf(x, a, b, c):
	return igamma(c/2., 0.5*pow((x-a)/b, 2))

# Distribution mean
# chimean(a, b, c)
def chimean(a, b, c):
	return a+((sqrt2*b*gamma((c+1.)/2.))/gamma(c/2.))

# Distribution variance
# chivar(a, b, c)
def chivar(a, b, c):
	return pow(b, 2.)*(c-((2*pow(gamma((c+1.)/2.), 2))/pow(gamma(c/2.), 2)))
#--


#--
# Cosine Distribution
#--

# PDF
# cospdf(x, a, b)
# x: float
# a: float, location parameter
# b: float, scale parameter
def cospdf(x, a, b):
	return (1./(2*pi*b))*(1.+cos((x-a)/b))

# CDF
# coscdf(x, a, b)
# x: float
# a: float, location parameter
# b: float, scale parameter
def coscdf(x, a, b):
	return (1./(2*pi))*(pi+((x-a)/b))+sin((x-a)/b)
#--

#--
# Exponential Distribution
#--
# Distribution parameters
# a: x >= a
# b: b > 0

# PDF
# exppdf(x, a, b)
# x: float | x >= a
def exppdf(x, a, b):
	return (1./b)*exp((a-x)/b)

# CDF
# expcdf(x, a, b)
# x: float | x >= a
def expcdf(x, a, b):
	return 1.-exp((a-x)/b)

# Distribution mean
# expmean(a, b)
def expmean(a, b):
	return a + b

# Distribution variance
# expvar(a, b)
def expvar(a, b):
	return b**2.

# Random value
# exprand(a, b)
def exprand(a, b):
	return a-(b*log(random()))



#--
#Binomial Distribution
#--

# PDF
# binompdf(x, a, b)
# x: integer
# a: 0 < a < 1
# b: integer, trials
def binompdf(x, a, b):
	return (gamma(b+1)/(gamma(b-x+1)*gamma(x+1.)))*pow(a, x)*pow(1.-a, b-x)

# Distribution mean
# binommean(a, b)
# a: 0 < a < 1
# b: integer, trials
def binommean(a, b):
	return a*b

# Distribution variance
# binomvar(a, b)
# a: 0 < a < 1
# b: integer, trials
def binomvar(a, b):
	return a*(1.-a)*b
#--

#--
#Negative Binomial Distribution
#--

# PDF
# nbinompdf(x, a, b)
# x: integer
# a: 0 < a < 1
# b: 1 <= b <= x
def nbinompdf(x, a, b):
	return (gamma(x)/(gamma(x-b+1.)*gamma(b)))*pow(a,b)*pow(1.-a, x-b)

# Distribution mean
# nbinommean(a, b)
# a: 0 < a < 1
# b: integer, trials
def nbinommean(a, b):
	return a*b

# Distribution variance
# nbinomvar(a, b)
# a: 0 < a < 1
# b: integer, trials
def nbinomvar(a, b):
	return a*(1.-a)*b
#--


#--
# Geometric Distribution
#--

# PDF
# geopdf(x, a)
# x: integer | x > 0
# a: 0 < a < 1
def geopdf(x, a):
	return a*pow(1.-a, x-1.)

# Distribution mean
# geomean(a)
# a: 0 < a < 1
def geomean(a):
	return 1./a

# Distribution variance
# geovar(a)
# a: 0 < a < 1
def geovar(a):
	return (1.-a)/a**2.
#--


#--
# Logarithmic Distribution
#--

# PDF
# logpdf(x, a)
# x: integer | x > 0
# a: 0 < a < 1
def logpdf(x, a):
	return -pow(a, x)/(log(1.-a)*x)

# Distribution mean
# logmean(a)
# a: 0 < a < 1
def logmean(a):
	return -a/((1.-a)*log(1.-a))

# Distribution variance
# logvar(a)
# a: 0 < a < 1
def logvar(a):
	return (-a*(a+log(1.-a)))/(pow(1.-a, 2)*pow(log(1.-a), 2))
#--

#--
# Poisson Distribution
#--

# PDF
# poispdf(x, a)
# x: integer | x >= 0
# a: expectation parameter | a > 0
def poispdf(x, a):
	return (exp(-a)*pow(a,x))/gamma(x+1)

# Distribution mean
# poismean(a)
# a: expectation parameter | a > 0
def poismean(a):
	return a

# Distribution variance
# poisvar(a)
# a: expectation parameter | a > 0
def poisvar(a):
	return a
#--

"""
