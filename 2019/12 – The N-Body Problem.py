def step_system(arg_moons):
	import itertools
	
	moons = [
		[
			list(direction)
			for direction in moon
		]
		for moon in arg_moons
	]
	
	for (moon_a, moon_b, ) in itertools.combinations(moons, 2):
		for i in (0, 1, 2, ):
			if moon_a[i][0] < moon_b[i][0]:
				moon_a[i][1] += 1
				moon_b[i][1] -= 1
			elif moon_b[i][0] < moon_a[i][0]:
				moon_b[i][1] += 1
				moon_a[i][1] -= 1
	
	for moon in moons:
		for i in (0, 1, 2, ):
			moon[i][0] += moon[i][1]
	
	return tuple(
		tuple(
			tuple(direction)
			for direction in moon
		)
		for moon in moons
	)

def energy_in_system(moons):
	total = 0
	
	for moon in moons:
		pot = 0
		kin = 0
		for direction in moon:
			pot += abs(direction[0])
			kin += abs(direction[1])
		total += pot * kin
	
	return total

def part_one(moons, steps):
	for _ in range(steps):
		moons = step_system(moons)
	return energy_in_system(moons)

def part_two(moons):
	systems = (set(),  set(), set(), )
	
	cycles_found = [False, False, False, ]
	while [True, True, True, ] != cycles_found:
		for i in (0, 1, 2, ):
			temp = tuple(
				moon[i]
				for moon in moons
			)
			if temp in systems[i]:
				cycles_found[i] = True
			else:
				systems[i].add(temp)
		moons = step_system(moons)
	
	import math
	
	result = 1
	result = result * len(systems[0]) // math.gcd(result, len(systems[0]))
	result = result * len(systems[1]) // math.gcd(result, len(systems[1]))
	result = result * len(systems[2]) // math.gcd(result, len(systems[2]))
	
	return result


def parse_input(input_file):
	parsed = list()
	
	import re
	regex = re.compile(r"""(?x)
		\x3C
		x\x3D(?P<x>\x2D?[0-9]+)
		\x2C\x20
		y\x3D(?P<y>\x2D?[0-9]+)
		\x2C\x20
		z\x3D(?P<z>\x2D?[0-9]+)
		\x3E
	""")
	
	import csv
	for row in csv.reader(input_file, delimiter="\xFF"):
		for cell in row:
			match = regex.fullmatch(cell)
			
			parsed.append(
				(
					(int(match["x"], base=10), 0, ),
					(int(match["y"], base=10), 0, ),
					(int(match["z"], base=10), 0, ),
				)
			)
	
	return tuple(parsed)

def generate_tests():
	test_input = parse_input([
		"<x=-1, y=0, z=2>",
		"<x=2, y=-10, z=-7>",
		"<x=4, y=-8, z=8>",
		"<x=3, y=5, z=-1>",
	])
	yield (part_one, (test_input, 10, ), 179, )
	yield (part_two, (test_input, ), 2772, )
	
	test_input = parse_input([
		"<x=-8, y=-10, z=0>",
		"<x=5, y=5, z=10>",
		"<x=2, y=-7, z=3>",
		"<x=9, y=-8, z=-3>",
	])
	yield (part_one, (test_input, 100, ), 1940, )
	
	test_input = parse_input([
		"<x=-8, y=-10, z=0>",
		"<x=5, y=5, z=10>",
		"<x=2, y=-7, z=3>",
		"<x=9, y=-8, z=-3>",
	])
	yield (part_two, (test_input, ), 4686774924, )

for test in generate_tests():
	result = test[0](*test[1])
	message = f"{test[0].__name__}{test[1]!r} should be {test[2]}, got {result}"
	assert result == test[2], message

from pathlib import Path
with open(Path(__file__).with_suffix(".txt")) as file:
	parsed = parse_input(file)
	print(f"{part_one(parsed, 1000)=}")
	print(f"{part_two(parsed)=}")
