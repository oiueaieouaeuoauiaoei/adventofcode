def part_one(layers):
	return min(
		(
			layer.count(0),
			layer.count(1) * layer.count(2),
		)
		for layer in layers
	)[1]

def part_two(layers):
	from functools import reduce
	return list(reduce(
		lambda under, above: (
			(
				digit
				if 2 == above[index] else
				above[index]
			)
			for (index, digit, ) in enumerate(under)
		),
		reversed(layers)
	))


def pretty_print(coordinates):
	from functools import reduce
	minima = list(reduce(lambda minima, coordinate: map(min, zip(minima, coordinate)), coordinates))
	maxima = list(reduce(lambda maxima, coordinate: map(max, zip(maxima, coordinate)), coordinates))
	ranges = list(list(range(minimum, maximum +1)) for (minimum, maximum, ) in zip(minima, maxima))
	
	# could stay generic but even at 3D it start to be unreadable
	# and probably do not want to pretty print 1D coordinates
	assert 2 == len(ranges), "2D only"
	
	# product iterate its iterators last to first
	# here that would mean y then x, while we want x then y
	from itertools import product
	for (y, x, ) in product(*reversed(ranges)):
		if minima[0] == x:
			print("")
		if (x, y, ) in coordinates:
			print("\N{DARK SHADE}", end="")
		else:
			print("\N{LIGHT SHADE}", end="")
	print("")

def parse_input(input_file, layer_size):
	layers = list()
	layer = list()
	layers.append(layer)
	
	import csv
	for row in csv.reader(input_file):
		for cell in row:
			for digit in cell:
				if len(layer) < layer_size:
					pass
				else:
					layer = list()
					layers.append(layer)
				
				layer.append(int(digit, base=10))
	
	return layers

def generate_tests():
	test = parse_input([
		"123456",
		"789012",
	], 3*2)
	
	yield (part_one, (test, ), 1, )
	yield (part_two, (test, ), [1, 8, 3, 4, 5, 6], )

for test in generate_tests():
	result = test[0](*test[1])
	message = f"{test[0].__name__}{test[1]!r} should be {test[2]}, got {result}"
	assert result == test[2], message

from pathlib import Path
with open(Path(__file__).with_suffix(".txt")) as file:
	layers = parse_input(file, 25*6)
	print(f"{part_one(layers)=}")
	print(f"{part_two(layers)=}")
	
	print(f"pretty_print of part_two(layers)")
	image = part_two(layers)
	assert not set(image).difference((0, 1, ))
	pretty_print(
		set(
			(x, y, )
			for x in range(25)
			for y in range(6)
			if 1 == image[25 *y +x]
		)
	)
