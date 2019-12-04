from re import compile
increasing_digits_pattern = compile("0*1*2*3*4*5*6*7*8*9*")

def part_one(password_limits):
	from collections import Counter
	return len(set(
		filter(
		lambda password: 1 < len({1}.union(Counter(password).values())),
		filter(
		lambda password: increasing_digits_pattern.fullmatch(password) is not None,
		map(
		str,
		range(password_limits[0], password_limits[1])
		)))
	))

def part_two(password_limits):
	from collections import Counter
	return len(set(
		filter(
		lambda password: 1 == len({2}.intersection(Counter(password).values())),
		filter(
		lambda password: increasing_digits_pattern.fullmatch(password) is not None,
		map(
		str,
		range(password_limits[0], password_limits[1])
		)))
	))

def parse_input(input_file):
	import csv
	parsed = list()
	for row in csv.reader(input_file, delimiter="-"):
		for cell in row:
			parsed.append(int(cell, base=10))
	return parsed

from pathlib import Path
with open(Path(__file__).with_suffix(".txt")) as file:
	password_limits = parse_input(file)
	print(f"{part_one(password_limits)=}")
	print(f"{part_two(password_limits)=}")
