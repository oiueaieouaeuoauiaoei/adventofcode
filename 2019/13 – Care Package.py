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
				yield None
			memory[parameter_a] = arg_inputs.popleft()
			instruction_pointer += 2
		elif 4 == opcode: # outputs
			arg_outputs.appendleft(memory[parameter_a])
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

def update_screen(outputs, screen):
	score = None
	
	while len(outputs):
		x = outputs.pop()
		y = outputs.pop()
		tile_id = outputs.pop()
		
		screen[(x, y, )] = tile_id
	
	assert screen.get((-1, 0, ), 0) not in {2, 3, 4, }, "score is a block/horizontal paddle/ball tile"
	
	return screen

def part_one(memory):
	inputs = collections.deque()
	outputs = collections.deque()
	
	for _ in run_intcode(memory, inputs, outputs):
		pass
	
	screen = update_screen(outputs, dict())
	
	return len(list(
		None
		for tile_id in screen.values()
		if 2 == tile_id
	))

def part_two(memory):
	memory = memory.copy()
	memory[0] = 2
	inputs = collections.deque()
	outputs = collections.deque()
	outputs_pointer = 0
	
	screen = dict()
	for _ in run_intcode(memory, inputs, outputs):
		screen = update_screen(outputs, screen)
		
		has_blocks = any(
			2 == tile_id
			for tile_id in screen.values()
		)
		
		if has_blocks:
			paddle_x = next(
				position
				for (position, tile_id, ) in screen.items()
				if 3 == tile_id
			)[0]
			
			ball_x = next(
				position
				for (position, tile_id, ) in screen.items()
				if 4 == tile_id
			)[0]
			
			if paddle_x < ball_x:
				inputs.append(1)
			elif ball_x < paddle_x:
				inputs.append(-1)
			else:
				inputs.append(0)
		else:
			inputs.append(-1)
	
	screen = update_screen(outputs, screen)
	
	return screen[(-1, 0, )]


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
