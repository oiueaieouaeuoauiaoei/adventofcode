def parse_input():
	def parse_line(line):
		return int(line, base=10)
	
	from pathlib import Path
	path = Path(__file__).with_suffix(".txt")
	with open(path, mode="rt", encoding="utf8") as file:
		return [parse_line(line) for line in file]
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
