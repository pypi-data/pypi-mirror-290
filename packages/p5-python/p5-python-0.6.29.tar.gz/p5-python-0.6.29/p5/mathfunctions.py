import math
import builtins
from p5.settings import *
import random as randompy
from random import randint, triangular, seed, gauss

def randomSeed(var):
    builtins.RANDOMSEED = var
    randompy.seed(var)

def random(*args):
    if len(args)==0 :
        return randompy.random()   
    if len(args)==1 :
        if type(args[0]) == 'list' or type(args[0]) == 'set' or type(args[0]) == 'tuple':
            return randompy.choice(args[0])
        else:
            return randompy.uniform(0,args[0])
    if len(args)==2 :
        return randompy.uniform(args[0],args[1])

def constrain(num, low, high):
    if num <= high and num >= low:
        return num
    elif num < low:
        return low
    elif num > high:
        return high
    return -1

def pow(x,exp):
    return x**exp

def floor(x):
    return math.floor(x)

def ceil(x):
    return math.ceil(x)

def dist(x, y):
    return math.dist(x, y)

def dist(x1, y1, x2, y2):
    return math.dist((x1, y1), (x2, y2))

def exp(x):
    return math.exp(x)

def lerp(a,b,t):
    return (1 - t) * 1 + t * b

def log(x):
    return math.log(x)

def log10(x):
    return math.log(x, 10)

def log2(x):
    return math.log(x, 2)

def logb(x, b):
    return math.log(x, b)

def mag(x, y):
    return math.dist((0, 0), (x, y))

def rerange(value, start1, stop1, start2, stop2, clamp=False):
    n = (stop2 - start2)*value / (stop1 - start1) + start2
    if clamp:
        return constrain(n, start2, stop2)
    else:
        return n

def map(val,srclow,srcup,destlow,destup):
    return (val-srclow)/(srcup-srclow) * (destup-destlow) + destlow

def norm(value, start, stop):
    return rererange(value, start, stop, 0, 1)

def sq(n):
    return n*n

def sqrt(x):
    return math.sqrt(x)

def frac(x):
    return math.modf(x)[1]

def sin(x):
    return math.sin(x)

def cos(x):
    return math.cos(x)

def tan(x):
    return math.tan(x)

def asin(x):
    return math.asin(x)

def acos(x):
    return math.acos(x)

def atan2(x):
    return math.atan2(x)

def atan(x):
    return math.atan(x)

def degrees(x):
    return math.degrees(x)

def radians(x):
    return math.radians(x)

def randomgaussian(mean,dev):
    return gauss(mean,dev)

def integral(f, a, b, n=100, type="midpoint"):
    if type == "midpoint":
        return _midpoint(f, a, b, n)
    elif type == "trapezoid":
        return _trapezoid(f, a, b, n)
    elif type == "simpsons":
        return _simpsons(f, a, b, n)
    else:
        return -1
    pass

def _midpoint(f, a, b, n):
    dx = (b-a)/n
    result = 0

    xi = linspace(a + 0.5*dx, b - 0.5*dx, n)
    result = dx*sum(f(xi))
    return result

def _trapezoid(f, a, b, n):
    dx = (b-a)/n
    result = 0

    xi = linspace(a, b, n+1)
    result = sum(f(xi)) - 0.5*f(a) - 0.5*f(b)
    return result*dx

def _simpsons(f, a, b, n):
    if n % 2:
        return -1
    return (b-a)/6.0 * (f(a) + 4*f((a+b)/2) + f(b))
