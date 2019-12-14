def fuel_to_ore(fuel, reactions):
	inventory = {
		key: 0
		for key in reactions.keys()
	}
	
	inventory["FUEL"] = fuel
	# the only chemical present in inputs that is not the output to any reaction
	# or at least should be
	inventory["ORE"] = 0
	
	while not all(
		"ORE" == chemical or quantity <= 0
		for (chemical, quantity, ) in inventory.items()
	):
		for chemical in inventory.keys() - {"ORE", }:
			(reaction_quantity, reaction_inputs, ) = reactions[chemical]
			
			# the inventory can hold negative quantities of chemicals
			# that could induce negative reactions (where we consume inputs)
			# in cases of (-1) reactions the 0<leftover branch rectify to (0)
			# we never deplete the inventory enough to cause cases of (-2)
			
			(reactions_needed, leftover, ) = divmod(inventory[chemical], reaction_quantity)
			if 0 < leftover:
				reactions_needed += 1
			
			inventory[chemical] -= reaction_quantity * reactions_needed
			for (input_quantity, input_chemical, ) in reaction_inputs:
				inventory[input_chemical] += input_quantity * reactions_needed
	
	return inventory["ORE"]

def part_one(reactions):
	return fuel_to_ore(1, reactions)

def part_two(reactions):
	R = 1
	while fuel_to_ore(R, reactions) < 1000000000000:
		R *= 2
	L = R // 2
	
	while L < R:
		m = (L + R) // 2
		if 1000000000000 < fuel_to_ore(m, reactions):
			R = m
		else:
			L = m + 1
	
	return L - 1


def parse_input(input_file):
	parsed = dict()
	
	import re
	reaction_regex = re.compile(r"""(?x)
		(?P<inputs>
			[0-9]+\x20[A-Z]+
			(\x2C\x20[0-9]+\x20[A-Z]+)*
		)
		\x20\x3D\x3E\x20
		(?P<output_quantity>[0-9]+)
		\x20
		(?P<output_chemical>[A-Z]+)
	""")
	input_regex = re.compile(r"""(?x)
		(?P<input_quantity>[0-9]+)
		\x20
		(?P<input_chemical>[A-Z]+)
	""")
	
	import csv
	for row in csv.reader(input_file, delimiter="\xFF"):
		for cell in row:
			reaction_match = reaction_regex.fullmatch(cell)
			
			assert reaction_match["output_chemical"] not in parsed
			parsed[reaction_match["output_chemical"]] = (
				int(reaction_match["output_quantity"], base=10),
				tuple(
					(
						int(input_match["input_quantity"], base=10),
						input_match["input_chemical"],
					)
					for input_match in input_regex.finditer(reaction_match["inputs"])
				),
			)
	
	return parsed

def generate_tests():
	test_input = parse_input([
		"10 ORE => 10 A",
		"1 ORE => 1 B",
		"7 A, 1 B => 1 C",
		"7 A, 1 C => 1 D",
		"7 A, 1 D => 1 E",
		"7 A, 1 E => 1 FUEL",
	])
	yield (part_one, (test_input, ), 31, )
	
	test_input = parse_input([
		"9 ORE => 2 A",
		"8 ORE => 3 B",
		"7 ORE => 5 C",
		"3 A, 4 B => 1 AB",
		"5 B, 7 C => 1 BC",
		"4 C, 1 A => 1 CA",
		"2 AB, 3 BC, 4 CA => 1 FUEL",
	])
	yield (part_one, (test_input, ), 165, )
	
	test_input = parse_input([
		"157 ORE => 5 NZVS",
		"165 ORE => 6 DCFZ",
		"44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL",
		"12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ",
		"179 ORE => 7 PSHF",
		"177 ORE => 5 HKGWZ",
		"7 DCFZ, 7 PSHF => 2 XJWVT",
		"165 ORE => 2 GPVTF",
		"3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT",
	])
	yield (part_one, (test_input, ), 13312, )
	yield (part_two, (test_input, ), 82892753, )
	
	test_input = parse_input([
		"2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG",
		"17 NVRVD, 3 JNWZP => 8 VPVL",
		"53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL",
		"22 VJHF, 37 MNCFX => 5 FWMGM",
		"139 ORE => 4 NVRVD",
		"144 ORE => 7 JNWZP",
		"5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC",
		"5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV",
		"145 ORE => 6 MNCFX",
		"1 NVRVD => 8 CXFTF",
		"1 VJHF, 6 MNCFX => 4 RFSQX",
		"176 ORE => 6 VJHF",
	])
	yield (part_one, (test_input, ), 180697, )
	yield (part_two, (test_input, ), 5586022, )
	
	test_input = parse_input([
		"171 ORE => 8 CNZTR",
		"7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL",
		"114 ORE => 4 BHXH",
		"14 VRPVC => 6 BMBT",
		"6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL",
		"6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT",
		"15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW",
		"13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW",
		"5 BMBT => 4 WPTQ",
		"189 ORE => 9 KTJDG",
		"1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP",
		"12 VRPVC, 27 CNZTR => 2 XDBXC",
		"15 KTJDG, 12 BHXH => 5 XCVML",
		"3 BHXH, 2 VRPVC => 7 MZWV",
		"121 ORE => 7 VRPVC",
		"7 XCVML => 6 RJRHP",
		"5 BHXH, 4 VRPVC => 5 LTCX",
	])
	yield (part_one, (test_input, ), 2210736, )
	yield (part_two, (test_input, ), 460664, )

for test in generate_tests():
	result = test[0](*test[1])
	message = f"{test[0].__name__}{test[1]!r} should be {test[2]}, got {result}"
	assert result == test[2], message

from pathlib import Path
with open(Path(__file__).with_suffix(".txt")) as file:
	parsed = parse_input(file)
	print(f"{part_one(parsed)=}")
	print(f"{part_two(parsed)=}")
