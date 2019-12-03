def run_intcode(input_memory, noun, verb):
	done, memory, index = False, input_memory.copy(), 0
	
	memory[1] = noun
	memory[2] = verb
	
	while not done:
		if 1 == memory[index]:
			memory[memory[index +3]] = (
				memory[memory[index +1]] +
				memory[memory[index +2]]
			)
			index += 4
		elif 2 == memory[index]:
			memory[memory[index +3]] = (
				memory[memory[index +1]] *
				memory[memory[index +2]]
			)
			index += 4
		elif 99 == memory[index]:
			done = True
		else:
			raise Exception("Encountering an unknown opcode means something went wrong.")
	
	return memory[0]

def part_one(memory):
	return run_intcode(memory, noun=12, verb=2)

def part_two(memory):
	from itertools import product
	for noun, verb in product(range(100), range(100)):
		if 19690720 == run_intcode(memory, noun, verb):
			return 100*noun + verb

# some assumptions are required, but they seem to hold true
def part_two_bis(memory):
	base = run_intcode(memory, noun=0, verb=0)
	base_plus_noun = run_intcode(memory, noun=1, verb=0)
	base_plus_verb = run_intcode(memory, noun=0, verb=1)
	
	noun = base_plus_noun - base
	verb = base_plus_verb - base
	assert 0 < verb < noun
	
	goal = 19690720
	base_remain = goal - base
	
	noun_quotient, noun_remain = divmod(base_remain, noun)
	verb_quotient, verb_remain = divmod(noun_remain, verb)
	assert 0 == verb_remain
	
	return 100*noun_quotient + verb_quotient

def parse_input(input_file):
	import csv
	parsed = list()
	for row in csv.reader(input_file):
		for cell in row:
			parsed.append(int(cell, base=10))
	return parsed

from pathlib import Path
with open(Path(__file__).with_suffix(".txt")) as file:
	memory = parse_input(file)
	print(f"{part_one(memory)=}")
	print(f"{part_two(memory)=}")
	print(f"{part_two_bis(memory)=}")
