def run_intcode(arg_memory, arg_inputs, arg_outputs):
	done = False
	
	import collections
	memory = collections.defaultdict(int)
	for (index, cell, ) in enumerate(arg_memory):
		memory[index] = cell
	instruction_pointer = 0
	inputs_pointer = 0
	relative_base = 0
	
	def resolve_parameter(mode, parameter):
		if 0 == mode: # position
			return memory[instruction_pointer + parameter]
		elif 1 == mode: # immediate
			return instruction_pointer + parameter
		elif 2 == mode: # relative
			return memory[instruction_pointer + parameter] + relative_base
		else:
			raise Exception(f"unknown parameter mode, {mode=}, {parameter=}")
	
	instruction_lengths = {
		1: 4,
		2: 4,
		3: 2,
		4: 2,
		5: 3,
		6: 3,
		7: 4,
		8: 4,
		9: 2,
		99: 0,
	}
	
	def decode_instruction(instruction_pointer):
		instruction = memory[instruction_pointer]
		
		(instruction, opcode, ) = divmod(instruction, 100)
		
		parameters = [None]
		for parameter_index in range(instruction_lengths[opcode]):
			(instruction, mode, ) = divmod(instruction, 10)
			parameters.append(resolve_parameter(mode, parameter_index +1))
		
		return (opcode, parameters, )
	
	while not done:
		(opcode, parameters, ) = decode_instruction(instruction_pointer)
		
		def read(parameter):
			return memory[parameters[parameter]]
		
		def write(parameter, value):
			memory[parameters[parameter]] = value
		
		if 1 == opcode: # adds
			write(3, read(1) + read(2))
			instruction_pointer += 4
		elif 2 == opcode: # multiplies
			write(3, read(1) * read(2))
			instruction_pointer += 4
		elif 3 == opcode: # input
			write(1, arg_inputs[inputs_pointer])
			inputs_pointer += 1
			instruction_pointer += 2
		elif 4 == opcode: # outputs
			arg_outputs.append(read(1))
			instruction_pointer += 2
		elif 5 == opcode: # jump-if-true
			if 0 == read(1):
				instruction_pointer += 3
			else:
				instruction_pointer = read(2)
		elif 6 == opcode: # jump-if-false
			if 0 == read(1):
				instruction_pointer = read(2)
			else:
				instruction_pointer += 3
		elif 7 == opcode: # less than
			if read(1) < read(2):
				write(3, 1)
			else:
				write(3, 0)
			instruction_pointer += 4
		elif 8 == opcode: # equals
			if read(1) == read(2):
				write(3, 1)
			else:
				write(3, 0)
			instruction_pointer += 4
		elif 9 == opcode: # adjusts the relative base
			relative_base += read(1)
			instruction_pointer += 2
		elif 99 == opcode: # halt
			done = True
		else:
			raise Exception(f"unknown opcode, {opcode=}, {instruction_pointer=}")
	
	return arg_outputs

def part_one(memory):
	return run_intcode(memory, [1], list())[0]

def part_two(memory):
	return run_intcode(memory, [2], list())[0]


def parse_input(input_file):
	parsed = list()
	
	import csv
	for row in csv.reader(input_file):
		for cell in row:
			parsed.append(int(cell, base=10))
	
	return parsed

def generate_tests():
	test_input = parse_input(["109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"])
	yield (run_intcode, (test_input, list(), list(), ), test_input, )
	
	test_input = parse_input(["1102,34915192,34915192,7,4,7,99,0"])
	yield (run_intcode, (test_input, list(), list(), ), [test_input[1]*test_input[2]], )
	
	test_input = parse_input(["104,1125899906842624,99"])
	yield (run_intcode, (test_input, list(), list(), ), [test_input[1]], )

for test in generate_tests():
	result = test[0](*test[1])
	message = f"{test[0].__name__}{test[1]!r} should be {test[2]}, got {result}"
	assert result == test[2], message

from pathlib import Path
with open(Path(__file__).with_suffix(".txt")) as file:
	parsed = parse_input(file)
	print(f"{part_one(parsed)=}")
	print(f"{part_two(parsed)=}")
