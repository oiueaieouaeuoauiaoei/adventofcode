def parse_input():
	def parse_line(line):
		return int(line, base=10)
	
	from pathlib import Path
	with open(Path(__file__).with_suffix(".txt")) as file:
		# blindly strip the line feed at the end of inputs
		data = file.read()[:-1]
	return [parse_line(line) for line in data.split("\N{LINE FEED}")]
modules_masses = parse_input()

def mass_to_fuel(mass):
	return mass //3 -2

def part_one():
	total = 0
	for modules_mass in modules_masses:
		total += mass_to_fuel(modules_mass)
	return total

def part_two():
	total = 0
	for modules_mass in modules_masses:
		sub_total = 0
		fuel = mass_to_fuel(modules_mass)
		while 0 < fuel:
			sub_total += fuel
			fuel = mass_to_fuel(fuel)
		total += sub_total
	return total

print(f"{part_one()=}")
print(f"{part_two()=}")
