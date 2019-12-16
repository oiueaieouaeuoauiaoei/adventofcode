def part_one(phases):
	for _ in range(100):
		phases = [
			abs(sum(
				(
					(0, 1, 0, -1, )[((j +1) //(i +1)) %4]
					* phases[j]
				)
				for (j, phase, ) in enumerate(phases)
			)) %10
			for i in range(len(phases))
		]
	return "".join(map(str, phases[:8]))

def part_two(phases):
	# the pattern past the middle looks like
	# ０…０１１…１１１
	# ０…００１…１１１
	# ︙…︙︙︙⋱︙︙︙
	# ０…０００…０１１
	# ０…０００…００１
	
	# so we can ignore everything before the message offset
	message_offset = int("".join(map(str, phases[:7])), base=10)
	assert len(phases) * 10_000 <= message_offset * 2
	phases = (phases * 10_000)[message_offset:]
	
	# if we reverse it we can keep a simple tally
	# rather than summing a slice for every row
	phases.reverse()
	for _ in range(100):
		tally = 0
		for (index, phase, ) in enumerate(phases):
			tally += phase
			tally %= 10
			phases[index] = tally
	phases.reverse()
	
	return "".join(map(str, phases[:8]))


def parse_input(input_file):
	parsed = list()
	
	import csv
	for row in csv.reader(input_file):
		for cell in row:
			for digit in cell:
				parsed.append(int(digit, base=10))
	
	return parsed

def generate_tests():
	test_input = parse_input([
		"80871224585914546619083218645595",
	])
	yield (part_one, (test_input, ), "24176176", )
	
	test_input = parse_input([
		"19617804207202209144916044189917",
	])
	yield (part_one, (test_input, ), "73745418", )
	
	test_input = parse_input([
		"69317163492948606335995924319873",
	])
	yield (part_one, (test_input, ), "52432133", )
	
	test_input = parse_input([
		"03036732577212944063491565474664",
	])
	yield (part_two, (test_input, ), "84462026", )
	
	test_input = parse_input([
		"02935109699940807407585447034323",
	])
	yield (part_two, (test_input, ), "78725270", )
	
	test_input = parse_input([
		"03081770884921959731165446850517",
	])
	yield (part_two, (test_input, ), "53553731", )

for test in generate_tests():
	result = test[0](*test[1])
	message = f"{test[0].__name__}{test[1]!r} should be {test[2]}, got {result}"
	assert result == test[2], message

from pathlib import Path
with open(Path(__file__).with_suffix(".txt")) as file:
	parsed = parse_input(file)
	print(f"{part_one(parsed)=}")
	print(f"{part_two(parsed)=}")
