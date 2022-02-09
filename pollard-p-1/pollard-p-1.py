
from math import gcd
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

def logstep(i, a, p):
	if "--log-step" not in argv:
		return
	out = f"i = {i}, "
	out += f"a{i+1} = {a}, "
	out += f"gcd(a{i+1}-1, n) = {p}, "
	print(out)

def pollard_p_1(a, n):
	i = 0
	p = 1
	step = lambda x,i,n: (x**(i+1)) % n
	while p == 1:
		a = step(a, i, n)
		p = gcd(a-1, n)
		logstep(i, a, p)
		i += 1
		if p == n:
			return n, i
	return p, i


if __name__ == "__main__":
	a = 2
	n = 19511
	if "-a" in argv:
		a = nextarg("-a", argv, int)
	if "-n" in argv:
		n = nextarg("-n", argv, int)

	p, i = pollard_p_1(a, n)
	
	if p == n:
		exit(f"Algorithm failure (step {i}); \np = n --> {p} = {n} \n")

	q = n // p

	print(f"n = pq: {n} = {p}x{q}, steps: {i} ")
