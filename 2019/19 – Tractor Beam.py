import collections
class DefaultList(collections.UserList):
	# not checking for negative indices
	def __getitem__(self, index):
		if index < len(self.data):
			return self.data[index]
		else:
			return 0
	
	def __setitem__(self, index, item):
		if index < len(self.data):
			self.data[index] = item
		elif 0 == item:
			pass
		else:
			while len(self.data) < index:
				self.data.append(0)
			self.data.append(item)

def run_intcode(arg_memory, arg_inputs, arg_outputs):
	memory = DefaultList(arg_memory)
	instruction_pointer = 0
	relative_base = 0
	
	def resolve_parameter(mode, parameter):
		if 0 == mode: # position
			return memory[instruction_pointer + parameter]
		elif 1 == mode: # immediate
			return instruction_pointer + parameter
		elif 2 == mode: # relative
			return memory[instruction_pointer + parameter] + relative_base
		else:
			raise Exception("unknown parameter mode")
	
	halted = False
	while not halted:
		instruction = memory[instruction_pointer]
		
		(instruction, opcode, ) = divmod(instruction, 100)
		
		if opcode in {1, 2, 7, 8, }:
			(instruction, mode_a, ) = divmod(instruction, 10)
			(instruction, mode_b, ) = divmod(instruction, 10)
			(instruction, mode_c, ) = divmod(instruction, 10)
			
			parameter_a = resolve_parameter(mode_a, 1)
			parameter_b = resolve_parameter(mode_b, 2)
			parameter_c = resolve_parameter(mode_c, 3)
		elif opcode in {5, 6, }:
			(instruction, mode_a, ) = divmod(instruction, 10)
			(instruction, mode_b, ) = divmod(instruction, 10)
			
			parameter_a = resolve_parameter(mode_a, 1)
			parameter_b = resolve_parameter(mode_b, 2)
			parameter_c = 0
		elif opcode in {3, 4, 9, }:
			(instruction, mode_a, ) = divmod(instruction, 10)
			
			parameter_a = resolve_parameter(mode_a, 1)
			parameter_b = 0
			parameter_c = 0
		elif opcode in {99, }:
			parameter_a = 0
			parameter_b = 0
			parameter_c = 0
		else:
			raise Exception("unknown opcode")
		
		if 1 == opcode: # adds
			memory[parameter_c] = memory[parameter_a] + memory[parameter_b]
			instruction_pointer += 4
		elif 2 == opcode: # multiplies
			memory[parameter_c] = memory[parameter_a] * memory[parameter_b]
			instruction_pointer += 4
		elif 3 == opcode: # input
			while 0 == len(arg_inputs):
				yield (arg_inputs, arg_outputs, )
			memory[parameter_a] = arg_inputs.popleft()
			instruction_pointer += 2
		elif 4 == opcode: # outputs
			arg_outputs.append(memory[parameter_a])
			instruction_pointer += 2
		elif 5 == opcode: # jump-if-true
			if 0 == memory[parameter_a]:
				instruction_pointer += 3
			else:
				instruction_pointer = memory[parameter_b]
		elif 6 == opcode: # jump-if-false
			if 0 == memory[parameter_a]:
				instruction_pointer = memory[parameter_b]
			else:
				instruction_pointer += 3
		elif 7 == opcode: # less than
			if memory[parameter_a] < memory[parameter_b]:
				memory[parameter_c] = 1
			else:
				memory[parameter_c] = 0
			instruction_pointer += 4
		elif 8 == opcode: # equals
			if memory[parameter_a] == memory[parameter_b]:
				memory[parameter_c] = 1
			else:
				memory[parameter_c] = 0
			instruction_pointer += 4
		elif 9 == opcode: # adjusts the relative base
			relative_base += memory[parameter_a]
			instruction_pointer += 2
		# bad opcodes are caught in the paramater phase
		# thus the final case can only be opcode 99
		else: # halt
			halted = True
	
	return (arg_inputs, arg_outputs, )

def is_drone_pulled(memory, drone_x, drone_y):
	inputs = collections.deque((drone_x, drone_y, ))
	outputs = collections.deque()
	
	for _ in run_intcode(memory, inputs, outputs):
		pass
	
	return 1 == outputs[0]

def part_one(memory):
	s = 50
	return sum(
		1
		for y in range(s)
		for x in range(s)
		if is_drone_pulled(memory, x, y)
	)

def part_two(memory):
	# search for the closest pulled drone that is not at (0, 0, )
	(x, y, ) = (0, 1, )
	while not is_drone_pulled(memory, x, y):
		if x == y:
			(x, y, ) = (0, x +1, )
		elif x < y:
			(x, y, ) = (y, x, )
		else:
			(x, y, ) = (y +1, x, )
	
	s = 99
	while not is_drone_pulled(memory, x, y +s):
		# riding the upper edge of the beam
		x += 1
		while not is_drone_pulled(memory, x +s, y):
			y += 1
	
	return 10000 *x +y


def parse_input(input_file):
	parsed = list()
	
	import csv
	for row in csv.reader(input_file):
		for cell in row:
			parsed.append(int(cell, base=10))
	
	return parsed

from pathlib import Path
with open(Path(__file__).with_suffix(".txt")) as file:
	parsed = parse_input(file)
	print(f"{part_one(parsed)=}")
	print(f"{part_two(parsed)=}")
