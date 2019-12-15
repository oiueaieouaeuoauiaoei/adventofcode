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

def a_star(maze, start, goal):
	def h(node):
		distance = node - goal
		return abs(distance.real) + abs(distance.imag)
	
	open_set = {start, }
	came_from = dict()
	g_score = dict()
	g_score[start] = 0
	f_score = dict()
	f_score[start] = h(start)
	
	while open_set:
		current = min(open_set, key=lambda node: f_score[node])
		if current == goal:
			total_path = [current, ]
			while current in came_from:
				current = came_from[current]
				total_path.append(current)
			return total_path
		
		open_set.remove(current)
		
		for neighbor in {
			current - delta
			for delta in {-1J, 1J, -1, 1, }
			if (current - delta) in maze
		}:
			tentative_gScore = g_score[current] + 1
			if neighbor not in g_score or tentative_gScore < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = tentative_gScore
				f_score[neighbor] = g_score[neighbor] + h(neighbor)
				if neighbor not in open_set:
					open_set.add(neighbor)
	
	raise Exception("could not solve maze")

def generate_maze(memory):
	maze = set()
	position = complex(0, 0)
	direction = 1J
	oxygen_system = None
	direction_to_command = {
		-1J: 1,
		1J: 2,
		-1: 3,
		1: 4,
	}
	
	for (inputs, outputs, ) in run_intcode(
		memory,
		collections.deque((direction_to_command[direction], )),
		collections.deque(),
	):
		reply = outputs.popleft()
		if 0 == reply:
			direction *= -1J
		elif 1 == reply:
			maze.add(position + direction)
			position += direction
			direction *= 1J
		elif 2 == reply:
			maze.add(position + direction)
			position += direction
			direction *= 1J
			oxygen_system = position
		else:
			raise Exception("unknown status")
		
		# send a movement command
		inputs.append(direction_to_command[direction])
		
		# break out if we found the oxygen system
		# and the repair droid is back home
		if oxygen_system is not None and 0 == position:
			break
	
	return (maze, oxygen_system, )

def part_one(memory):
	(maze, oxygen_system, ) = generate_maze(memory)
	
	solved = a_star(
		maze,
		0,
		oxygen_system,
	)
	
	return len(solved) - 1

def part_two(memory):
	(maze, oxygen_system, ) = generate_maze(memory)
	
	depth = 0
	touched = set()
	current_set = {oxygen_system, }
	
	while current_set:
		depth += 1
		touched.update(current_set)
		current_set = {
			current - delta
			for current in current_set
			for delta in {-1J, 1J, -1, 1, }
			if (current - delta) in maze and (current - delta) not in touched
		}
	
	return depth - 1


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
