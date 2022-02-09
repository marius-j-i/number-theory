
from math import gcd, sqrt
from sys import argv


def nextarg(arg, argv, callback = None):
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

def logstep(step, x, y, n, p):
	if "--log-step" not in argv:
		return
	out = f"step = {step}, "
	out += f"a_{step} = {x}, "
	out += f"a_{2*step} = {y}, "
	out += f"a_{step+1} = {f(x,n)}, "
	out += f"a_{2*step+2} = {g(y,n)}, "
	out += f"gcd(a_{step+1} - a_{2*step+2}, n) = {p} "
	print(out)

def f(x, n):
	return (x**2 + 1) % n

def g(x, n):
	return f(f(x, n), n)

def _pollard_rho(x, y, n, step = 0):
	ai = f(x,n) ; a2i = g(y,n)
	p = gcd(ai-a2i, n)
	logstep(step, x, y, n, p)
	if p == n:
		return n, step+1 # failed
	elif p != 1:
		return p, step+1
	return _pollard_rho(ai, a2i, n, step+1)

def pollard_rho(a, n):
	p, steps = _pollard_rho(a, a, n)
	q = n // p
	return p, q, steps


if __name__ == "__main__":
	a, n = 2, 32399
	if "-a" in argv:
		a = nextarg("-a", argv, int)
	if "-n" in argv:
		n = nextarg("-n", argv, int)

	p, q, steps = pollard_rho(a, n)
	print(p,q, p*q)
	assert p * q == n, f":|"

	if q == 1 or p == n:
		exit(f"Algorithm failure (step {steps}); \np = n --> {p} = {n} \n")
	
	if "--output" in argv:
		print(
			f"n = pq: {n} = {p} x {q} \n" + 
			f"steps, sqrt(p), sqrt(q); {steps}, {sqrt(p)}, {sqrt(q)} "
		)
