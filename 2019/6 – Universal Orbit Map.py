def path_to_COM(orbits, you):
	while you != "COM":
		you = orbits[you]
		yield you

def part_one(orbits):
	return sum(len(list(path_to_COM(orbits, key))) for key in orbits.keys())

def part_two(orbits):
	return len(set(path_to_COM(orbits, "YOU")).symmetric_difference(path_to_COM(orbits, "SAN")))


def parse_input(input_file):
	import csv
	orbits = dict()
	for row in csv.reader(input_file, delimiter=")"):
		orbit = list()
		for cell in row:
			orbit.append(cell)
		orbits[orbit[1]] = orbit[0]
	return orbits

def generate_tests():
	part_one_input = parse_input([
		"COM)B",
		"B)C",
		"C)D",
		"D)E",
		"E)F",
		"B)G",
		"G)H",
		"D)I",
		"E)J",
		"J)K",
		"K)L",
	])
	yield (part_one, (part_one_input, ), 42, )
	
	part_two_input = parse_input([
		"COM)B",
		"B)C",
		"C)D",
		"D)E",
		"E)F",
		"B)G",
		"G)H",
		"D)I",
		"E)J",
		"J)K",
		"K)L",
		"K)YOU",
		"I)SAN",
	])
	yield (part_two, (part_two_input, ), 4, )

for test in generate_tests():
	result = test[0](*test[1])
	message = f"{test[0].__name__}{test[1]!r} should be {test[2]}, got {result}"
	assert result == test[2], message

from pathlib import Path
with open(Path(__file__).with_suffix(".txt")) as file:
	orbits = parse_input(file)
	print(f"{part_one(orbits)=}")
	print(f"{part_two(orbits)=}")
