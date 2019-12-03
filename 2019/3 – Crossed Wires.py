def distance_from_origin(coord):
	return sum(map(abs, coord))

def part_one(wires):
	first_wire, *other_wires = wires
	intersections = set(first_wire).intersection(*other_wires)
	return min(map(distance_from_origin, intersections))

def part_two(wires):
	first_wire, *other_wires = wires
	intersections = set(first_wire).intersection(*other_wires)
	return min(
		1 + steps + sum(map(lambda wire: 1 + wire.index(coord), other_wires))
		for steps, coord in enumerate(first_wire)
		if coord in intersections
	)

def parse_input(input_file):
	import csv
	parsed = list()
	for row in csv.reader(input_file):
		wire = list()
		head = (0, 0)
		for cell in row:
			if "D" == cell[0]:
				direction = (0, 1)
			elif "L" == cell[0]:
				direction = (-1, 0)
			elif "R" == cell[0]:
				direction = (1, 0)
			elif "U" == cell[0]:
				direction = (0, -1)
			else:
				raise AssertionError("unknown direction")
			
			for _ in range(int(cell[1:], base=10)):
				head = (head[0] + direction[0], head[1] + direction[1])
				wire.append(head)
		parsed.append(wire)
	return parsed

from pathlib import Path
with open(Path(__file__).with_suffix(".txt")) as file:
	wires = parse_input(file)
	print(f"{part_one(wires)=}")
	print(f"{part_two(wires)=}")

from io import StringIO
tests = [
	(part_one, ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"], 159),
	(part_one, ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"], 135),
	
	(part_two, ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"], 610),
	(part_two, ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"], 410),
]
for index, test in enumerate(tests):
	result = test[0](parse_input(test[1]))
	assert result == test[2], f"test case {index} failed, want {test[2]}, got {result}"
