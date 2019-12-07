def run_intcode(arg_memory, arg_inputs, arg_outputs):
	done = False
	
	memory = arg_memory.copy()
	instruction_pointer = 0
	inputs_pointer = 0
	
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
		elif 99 == opcode: # halt
			done = True
		else:
			raise Exception(f"unknown opcode, {opcode=}, {instruction_pointer=}")
	
	return arg_outputs

def part_one(memory):
	from itertools import permutations
	
	results = list()
	for permutation in permutations([0, 1, 2, 3, 4], 5):
		input_signal = [0]
		for setting in permutation:
			input_signal = run_intcode(memory, [setting, *input_signal], list())
		results.extend(input_signal)
	return max(results)

def part_two(memory):
	from itertools import permutations
	
	results = list()
	for permutation in permutations([5, 6, 7, 8, 9], 5):
		amp_infos = [
			[1, False, [], [permutation[0], 0, ], ],
			[2, False, [], [permutation[1], ], ],
			[3, False, [], [permutation[2], ], ],
			[4, False, [], [permutation[3], ], ],
			[0, False, [], [permutation[4], ], ],
		]
		
		while not amp_infos[4][1]:
			for amp_info in amp_infos:
				outputs = list()
				try:
					amp_info[1] = run_intcode(
						memory,
						amp_info[3] + amp_info[2],
						outputs,
					)
				except IndexError:
					pass
				amp_infos[amp_info[0]][2] = outputs
		
		results.append(amp_infos[0][2][-1])
	return max(results)


def parse_input(input_file):
	import csv
	parsed = list()
	for row in csv.reader(input_file):
		for cell in row:
			parsed.append(int(cell, base=10))
	return parsed

def generate_tests():
	memory = [
		3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
	]
	yield (part_one, (memory, ), 43210)
	memory = [
		3,23,3,24,1002,24,10,24,1002,23,-1,23,
		101,5,23,23,1,24,23,23,4,23,99,0,0
	]
	yield (part_one, (memory, ), 54321)
	memory = [
		3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
		1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0
	]
	yield (part_one, (memory, ), 65210)
	
	memory = [
		3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
		27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
	]
	yield (part_two, (memory, ), 139629729)
	memory = [
		3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
		-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
		53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
	]
	yield (part_two, (memory, ), 18216)

for test in generate_tests():
	result = test[0](*test[1])
	message = f"{test[0].__name__}{test[1]!r} should be {test[2]}, got {result}"
	assert result == test[2], message

from pathlib import Path
with open(Path(__file__).with_suffix(".txt")) as file:
	memory = parse_input(file)
	print(f"{part_one(memory)=}")
	print(f"{part_two(memory)=}")
