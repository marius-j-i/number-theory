
from math import gcd
from sys import argv
from typing import Sequence


def nextarg(arg: str, argv: Sequence, callback: callable = None) -> str:
	if arg not in argv:
		return None

	i = argv.index(arg) + 1

	if len(argv) == i or argv[i].startswith("--"):
		if callback is None:
			return None
		exit(f"{arg} flag requires positional argument {callback.__name__}")
	
	arg = argv[i]
	if callback is None:
		callback = str
	
	return callback(arg)

def log(a, b, q, r):
	if "--log" in argv:
		print(f"{a} = {b} x {q} + {r} ")

def _euclid(a:int, b:int, q:int, r:int, steps:dict = None) -> int:
	if steps is not None:
		steps[a] = b,q,r
	log(a, b, r, q)
	if r == 0:
		return b
	return _euclid(b, r, b//r, b % r, steps)

def euclid(a:int, b:int, c:int, steps:dict = None) -> int:
	# sort a and b after largest
	a,b = (a,b) if a > b else (b,a)
	# gcd, and record coefficients of b
	d = _euclid(a, b, a//b, a % b, steps)
	assert gcd(a,b) == d, f"Incorrect Euclid implementation: gcd(a,b) != d -> {gcd(a,b)} != {d}"
	return d if c % d == 0 else None

def rest_reverse(steps:dict) -> dict:
	rest = {}
	for a,v in steps.items():
		b,q,r = v
		if r == 0:
			continue
		rest[r] = a,b,-q
	return rest

def _back_sub(r:int, coef:int, rest:dict, xy:dict) -> int:
	if r not in rest:
		return r
	a,b,q = rest[r]
	if _back_sub(a, coef, rest, xy) not in rest:
		xy[a] += coef * 1
	if _back_sub(b, q * coef, rest, xy) not in rest:
		xy[b] += coef * q
	return r

def back_subsititute(a:int, b:int, d:int, rest:dict) -> tuple:
	xy = {a: 0, b : 0}
	_back_sub(d, 1, rest, xy)
	return xy.values()


def ext_euclid(a:int, b:int, c:int) -> tuple:
	steps = {}
	d = euclid(a, b, c, steps)
	assert c % d == 0, f"gcd(a,b) !| c --> c (mod gcd({a},{b})) = {c} (mod {d}) = {c % d} "
	
	rest = rest_reverse(steps)
	s,t = back_subsititute(a, b, d, rest)
	
	e = c // d
	x0 = s*e ; y0 = t*e
	x = x0 + b//d
	y = y0 - a//d
	
	if a*x + b*y != c:
		x,y = (y,x)
	assert a*x + b*y == c, f"ax + by != c --> {a} x {x} + {b} x {y} --> {a*x*e + b*y*e} != {c} "
	return x,y


if __name__ == "__main__":
	a = 3450 ; b = 5286 ; c = 132

	if "--equation" in argv:
		try:
			a,b,c = nextarg("--equation", argv, eval)
		except TypeError:
			exit(f"Equation must be comma separated without spaces, eg.; 1,2,3")

	x,y = ext_euclid(a,b,c)

	print(f"ax + by = c --> {a} x {x} + {b} x {y} = {c} --> {a*x + b*y} = {c}")
