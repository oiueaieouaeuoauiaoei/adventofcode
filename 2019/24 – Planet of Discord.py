def part_one(bugs):
	first_time = set()
	second_time = set()
	
	while not second_time:
		neighbor_count = {
			(x, y, ): sum(
				1
				for neighbor in list_neighbors((x, y, ))
				if neighbor in bugs
			)
			for y in range(5)
			for x in range(5)
		}
		
		bugs = {
			bug
			for (bug, count, ) in neighbor_count.items()
			if (
				count in {1, }
				if bug in bugs else
				count in {1, 2, }
			)
		}
		
		snapshot = frozenset(bugs)
		if snapshot not in first_time:
			first_time.add(snapshot)
		elif snapshot not in second_time:
			second_time.add(snapshot)
		else:
			raise Exception("should have exited the loop already")
	
	return sum(
		2 **(5 *y +x)
		for y in range(5)
		for x in range(5)
		if (x, y, ) in bugs
	)

def part_two(bugs, time=200):
	bugs = {
		(x, y, 0, )
		for (x, y, ) in bugs
	}
	
	for _ in range(time):
		minimum_z = min(z for (x, y, z, ) in bugs)
		maximum_z = max(z for (x, y, z, ) in bugs)
		
		neighbor_count = {
			(x, y, z, ): sum(
				1
				for neighbor in list_plutonian_neighbors((x, y, z, ))
				if neighbor in bugs
			)
			for z in range(minimum_z -1, maximum_z +2)
			for y in range(5)
			for x in range(5)
		}
		
		bugs = {
			bug
			for (bug, count, ) in neighbor_count.items()
			if (
				count in {1, }
				if bug in bugs else
				count in {1, 2, }
			)
		}
		
		bugs = {
			(x, y, z, )
			for (x, y, z, ) in bugs
			if not (2 == x and 2 == y)
		}
	
	return len(bugs)

def list_neighbors(bug):
	(x, y, ) = bug
	for (n_x, n_y, ) in ((x+1, y, ), (x, y+1, ), (x-1, y, ), (x, y-1, ), ):
		if n_x < 0:
			pass
		elif 4 < n_x:
			pass
		elif n_y < 0:
			pass
		elif 4 < n_y:
			pass
		else:
			yield (n_x, n_y, )

def list_plutonian_neighbors(bug):
	(x, y, z, ) = bug
	for (n_x, n_y, ) in ((x+1, y, ), (x, y+1, ), (x-1, y, ), (x, y-1, ), ):
		if 2 == n_x and 2 == n_y:
			if 1 == x and 2 == y:
				for y in range(5):
					yield (0, y, z+1, )
			elif 3 == x and 2 == y:
				for y in range(5):
					yield (4, y, z+1, )
			elif 2 == x and 1 == y:
				for x in range(5):
					yield (x, 0, z+1, )
			elif 2 == x and 3 == y:
				for x in range(5):
					yield (x, 4, z+1, )
			else:
				raise
		elif n_x < 0:
			yield (1, 2, z-1, )
		elif 4 < n_x:
			yield (3, 2, z-1, )
		elif n_y < 0:
			yield (2, 1, z-1, )
		elif 4 < n_y:
			yield (2, 3, z-1, )
		else:
			yield (n_x, n_y, z, )


def parse_input(lines):
	bugs = set()
	
	for (y, line, ) in enumerate(lines):
		for (x, char, ) in enumerate(line):
			if "\x23" == char: # NUMBER SIGN
				bugs.add((x, y, ))
			elif "\x2E" == char: # PERCENT SIGN
				pass
			elif "\x3F" == char: # QUESTION MARK
				pass
			else:
				raise AssertionError("unknown character in input")
	
	return bugs

def generate_tests():
	test_input = parse_input([
		"....#",
		"#..#.",
		"#..##",
		"..#..",
		"#....",
	])
	yield (part_one, (test_input, ), 2129920, )
	yield (part_two, (test_input, 10, ), 99, )

for test in generate_tests():
	result = test[0](*test[1])
	message = f"{test[0].__name__}{test[1]!r} should be {test[2]}, got {result}"
	assert result == test[2], message

from pathlib import Path
with open(Path(__file__).with_suffix(".txt")) as file:
	parsed = parse_input(file.read().splitlines(keepends=False))
	print(f"{part_one(parsed)=}")
	print(f"{part_two(parsed)=}")
