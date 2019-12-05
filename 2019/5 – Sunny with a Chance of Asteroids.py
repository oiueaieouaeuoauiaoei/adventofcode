def run_intcode(arg_memory, arg_inputs):
	done = False
	
	# padded to make the eager instruction decoder happy
	memory = arg_memory.copy() + [None, None, None]
	instruction_pointer = 0
	
	inputs = (input for input in arg_inputs)
	outputs = list()
	
	def resolve_parameter(mode, parameter):
		if 0 == mode: # position
			return memory[instruction_pointer +parameter]
		elif 1 == mode: # immediate
			return instruction_pointer +parameter
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
		99: 0,
	}
	
	def decode_instruction(instruction_pointer):
		instruction = memory[instruction_pointer]
		
		(instruction, opcode) = divmod(instruction, 100)
		
		parameters = [None]
		for parameter_index in range(instruction_lengths[opcode]):
			(instruction, mode) = divmod(instruction, 10)
			parameters.append(resolve_parameter(mode, parameter_index +1))
		
		return (opcode, parameters)
	
	while not done:
		(opcode, parameters) = decode_instruction(instruction_pointer)
		
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
			write(1, next(inputs))
			instruction_pointer += 2
		elif 4 == opcode: # outputs
			outputs.append(read(1))
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
		elif 99 == opcode: # halt
			done = True
		else:
			raise Exception(f"unknown opcode, {opcode=}, {instruction_pointer=}")
	
	return outputs

def part_one(memory):
	*test_values, diagnostic_code = run_intcode(memory, [1])
	assert all(map(lambda test_value: 0 == test_value, test_values))
	return diagnostic_code

def part_two(memory):
	return run_intcode(memory, [5])[0]


def parse_input(input_file):
	import csv
	parsed = list()
	for row in csv.reader(input_file):
		for cell in row:
			parsed.append(int(cell, base=10))
	return parsed

def generate_tests():
	memory = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
	for i in range(-99, 99):
		if 0 == i:
			yield (run_intcode, (memory, [i], ), [0])
		else:
			yield (run_intcode, (memory, [i], ), [1])
	
	memory = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
	for i in range(-99, 99):
		if 0 == i:
			yield (run_intcode, (memory, [i], ), [0])
		else:
			yield (run_intcode, (memory, [i], ), [1])
	
	memory = [
		3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
		1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
		999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
	]
	for i in range(-99, 99):
		if i < 8:
			yield (run_intcode, (memory, [i], ), [999])
		elif 8 < i:
			yield (run_intcode, (memory, [i], ), [1001])
		else:
			yield (run_intcode, (memory, [i], ), [1000])

for test in generate_tests():
	result = test[0](*test[1])
	message = f"{test[0].__name__}{test[1]!r} should be {test[2]}, got {result}"
	assert result == test[2], message

from pathlib import Path
with open(Path(__file__).with_suffix(".txt")) as file:
	memory = parse_input(file)
	print(f"{part_one(memory)=}")
	print(f"{part_two(memory)=}")
