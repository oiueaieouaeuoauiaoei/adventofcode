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
			while len(arg_inputs) <= inputs_pointer:
				yield None
			memory[parameter_a] = arg_inputs[inputs_pointer]
			inputs_pointer += 1
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
	
	return arg_outputs

def run_painting_robot(memory, base_inputs):
	robot = complex(0, 0)
	white_panels = set()
	painted_panels = set()
	direction = complex(0, -1)
	
	inputs = list(base_inputs)
	outputs = list()
	outputs_pointer = 0
	
	for _ in run_intcode(memory, inputs, outputs):
		assert len(outputs) == outputs_pointer +2
		
		if 0 == outputs[outputs_pointer]:
			white_panels -= {robot, }
		else:
			white_panels |= {robot, }
		painted_panels |= {robot, }
		outputs_pointer += 1
		
		if 0 == outputs[outputs_pointer]:
			direction *= complex(0, -1)
		else:
			direction *= complex(0, 1)
		robot += direction
		outputs_pointer += 1
		
		if robot in white_panels:
			inputs.append(1)
		else:
			inputs.append(0)
	
	return (white_panels, painted_panels, )

def part_one(memory):
	(white_panels, painted_panels, ) = run_painting_robot(memory, [0, ])
	return len(painted_panels)

def part_two(memory):
	(white_panels, painted_panels, ) = run_painting_robot(memory, [1, ])
	return white_panels


def pretty_print(coordinates):
	minimum_imag = int(min(coordinate.imag for coordinate in coordinates))
	maximum_imag = int(max(coordinate.imag for coordinate in coordinates))
	minimum_real = int(min(coordinate.real for coordinate in coordinates))
	maximum_real = int(max(coordinate.real for coordinate in coordinates))
	
	for imag in range(minimum_imag -1, maximum_imag +2):
		for real in range(minimum_real -1, maximum_real +2):
			if complex(real, imag) in coordinates:
				print("\N{DARK SHADE}", end="")
			else:
				print("\N{LIGHT SHADE}", end="")
		print("")

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
	
	print("pretty_print(part_two(parsed))")
	pretty_print(part_two(parsed))
