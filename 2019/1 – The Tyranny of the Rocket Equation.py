def mass_to_fuel(mass):
	return mass //3 -2

def part_one(modules_masses):
	total = 0
	for modules_mass in modules_masses:
		total += mass_to_fuel(modules_mass)
	return total

def part_two(modules_masses):
	total = 0
	for modules_mass in modules_masses:
		sub_total = 0
		fuel = mass_to_fuel(modules_mass)
		while 0 < fuel:
			sub_total += fuel
			fuel = mass_to_fuel(fuel)
		total += sub_total
	return total

def parse_input(input_file):
	import csv
	parsed = list()
	for row in csv.reader(input_file):
		for cell in row:
			parsed.append(int(cell, base=10))
	return parsed

from pathlib import Path
with open(Path(__file__).with_suffix(".txt")) as file:
	modules_masses = parse_input(file)
	print(f"{part_one(modules_masses)=}")
	print(f"{part_two(modules_masses)=}")
