def parse_input():
	def parse_line(line):
		return int(line, base=10)
	
	from pathlib import Path
	with open(Path(__file__).with_suffix(".txt")) as file:
		# blindly strip the line feed at the end of inputs
		data = file.read()[:-1]
	return [parse_line(line) for line in data.split("\N{COMMA}")]
memory = parse_input()

def run_intcode(input_memory, noun=None, verb=None):
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

def part_one():
	return run_intcode(memory, 12, 2)

def part_two():
	from itertools import product
	for noun, verb in product(range(100), range(100)):
		if 19690720 == run_intcode(memory, noun, verb):
			return 100*noun + verb

print(f"{part_one()=}")
print(f"{part_two()=}")
