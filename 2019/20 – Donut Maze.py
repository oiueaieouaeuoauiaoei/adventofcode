def part_one(donut):
	(maze, start, end, portals, portals_outside, ) = donut
	
	def step_through_portals(portals, current):
		for coord in current:
			if coord not in portals:
				yield coord
			else:
				yield portals[coord]
		
	
	current = {start, }
	touched = set()
	depth = 0
	while current and (end not in current):
		depth += 1
		touched.update(current)
		
		current = {
			coord - delta
			for coord in current
			for delta in {-1J, 1J, -1, 1, }
		}
		current = set(step_through_portals(portals, current))
		current &= maze
		current -= touched
	
	return depth

def part_two(donut):
	(maze, start, end, portals, portals_outside, ) = donut
	
	def step_through_portals(portals, current):
		for (coord, level, ) in current:
			if coord not in portals:
				yield (coord, level, )
			elif coord not in portals_outside:
				yield (portals[coord], level +1, )
			elif level < 0:
				pass
			else:
				yield (portals[coord], level -1, )
		
	
	current = {(start, 0, ), }
	touched = set()
	depth = 0
	while current and ((end, 0, ) not in current):
		depth += 1
		touched.update(current)
		
		current = {
			(coord - delta, level, )
			for (coord, level, ) in current
			for delta in {-1J, 1J, -1, 1, }
		}
		current = set(step_through_portals(portals, current))
		current = {
			(coord, level, )
			for (coord, level, ) in current
			if coord in maze
		}
		current -= touched
	
	return depth


def parse_input(input_file):
	lines = list()
	import csv
	for row in csv.reader(input_file, delimiter="\xFF"):
		for cell in row:
			lines.append(cell)
	
	maze = set()
	portal_cells = dict()
	for (imag, line) in enumerate(lines):
		for (real, cell) in enumerate(line):
			if cell in " #":
				pass
			elif "." == cell:
				maze.add(complex(real, imag))
			elif cell in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
				portal_cells[complex(real, imag)] = cell
	
	start = None
	end = None
	raw_portals_inside = dict()
	raw_portals_outside = dict()
	for (coord, portal_cell, ) in portal_cells.items():
		inside = (
			0 < coord.real -2 and coord.real +2 < len(lines[0])
			and
			0 < coord.imag -2 and coord.imag +2 < len(lines)
		)
		
		if coord +1J in maze:
			name = portal_cells[coord -1J] + portal_cell
			direction = 1J
		elif coord -1J in maze:
			name = portal_cell + portal_cells[coord +1J]
			direction = -1J
		elif coord +1 in maze:
			name = portal_cells[coord -1] + portal_cell
			direction = 1
		elif coord -1 in maze:
			name = portal_cell + portal_cells[coord +1]
			direction = -1
		else:
			name = "!!"
			direction = 0
		
		if "AA" == name:
			start = coord +direction
		elif "ZZ" == name:
			end = coord +direction
		elif "!!" == name:
			pass
		else:
			if inside:
				raw_portals_inside[name] = (coord, direction, )
			else:
				raw_portals_outside[name] = (coord, direction, )
	
	portals = dict()
	portals_outside = set()
	for (name, (coord_inside, in_dir, ), ) in raw_portals_outside.items():
		portals_outside.add(coord_inside)
		(coord_outside, out_dir, ) = raw_portals_inside[name]
		portals[coord_inside] = coord_outside +out_dir
		portals[coord_outside] = coord_inside +in_dir
	
	maze.update(portals.values())
	
	return (maze, start, end, portals, portals_outside, )

def generate_tests():
	test_input = parse_input([
		"         A           ",
		"         A           ",
		"  #######.#########  ",
		"  #######.........#  ",
		"  #######.#######.#  ",
		"  #######.#######.#  ",
		"  #######.#######.#  ",
		"  #####  B    ###.#  ",
		"BC...##  C    ###.#  ",
		"  ##.##       ###.#  ",
		"  ##...DE  F  ###.#  ",
		"  #####    G  ###.#  ",
		"  #########.#####.#  ",
		"DE..#######...###.#  ",
		"  #.#########.###.#  ",
		"FG..#########.....#  ",
		"  ###########.#####  ",
		"             Z       ",
		"             Z       ",
	])
	yield (part_one, (test_input, ), 23, )
	
	test_input = parse_input([
		"                   A               ",
		"                   A               ",
		"  #################.#############  ",
		"  #.#...#...................#.#.#  ",
		"  #.#.#.###.###.###.#########.#.#  ",
		"  #.#.#.......#...#.....#.#.#...#  ",
		"  #.#########.###.#####.#.#.###.#  ",
		"  #.............#.#.....#.......#  ",
		"  ###.###########.###.#####.#.#.#  ",
		"  #.....#        A   C    #.#.#.#  ",
		"  #######        S   P    #####.#  ",
		"  #.#...#                 #......VT",
		"  #.#.#.#                 #.#####  ",
		"  #...#.#               YN....#.#  ",
		"  #.###.#                 #####.#  ",
		"DI....#.#                 #.....#  ",
		"  #####.#                 #.###.#  ",
		"ZZ......#               QG....#..AS",
		"  ###.###                 #######  ",
		"JO..#.#.#                 #.....#  ",
		"  #.#.#.#                 ###.#.#  ",
		"  #...#..DI             BU....#..LF",
		"  #####.#                 #.#####  ",
		"YN......#               VT..#....QG",
		"  #.###.#                 #.###.#  ",
		"  #.#...#                 #.....#  ",
		"  ###.###    J L     J    #.#.###  ",
		"  #.....#    O F     P    #.#...#  ",
		"  #.###.#####.#.#####.#####.###.#  ",
		"  #...#.#.#...#.....#.....#.#...#  ",
		"  #.#####.###.###.#.#.#########.#  ",
		"  #...#.#.....#...#.#.#.#.....#.#  ",
		"  #.###.#####.###.###.#.#.#######  ",
		"  #.#.........#...#.............#  ",
		"  #########.###.###.#############  ",
		"           B   J   C               ",
		"           U   P   P               ",
	])
	yield (part_one, (test_input, ), 58, )
	
	test_input = parse_input([
		"             Z L X W       C                 ",
		"             Z P Q B       K                 ",
		"  ###########.#.#.#.#######.###############  ",
		"  #...#.......#.#.......#.#.......#.#.#...#  ",
		"  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  ",
		"  #.#...#.#.#...#.#.#...#...#...#.#.......#  ",
		"  #.###.#######.###.###.#.###.###.#.#######  ",
		"  #...#.......#.#...#...#.............#...#  ",
		"  #.#########.#######.#.#######.#######.###  ",
		"  #...#.#    F       R I       Z    #.#.#.#  ",
		"  #.###.#    D       E C       H    #.#.#.#  ",
		"  #.#...#                           #...#.#  ",
		"  #.###.#                           #.###.#  ",
		"  #.#....OA                       WB..#.#..ZH",
		"  #.###.#                           #.#.#.#  ",
		"CJ......#                           #.....#  ",
		"  #######                           #######  ",
		"  #.#....CK                         #......IC",
		"  #.###.#                           #.###.#  ",
		"  #.....#                           #...#.#  ",
		"  ###.###                           #.#.#.#  ",
		"XF....#.#                         RF..#.#.#  ",
		"  #####.#                           #######  ",
		"  #......CJ                       NM..#...#  ",
		"  ###.#.#                           #.###.#  ",
		"RE....#.#                           #......RF",
		"  ###.###        X   X       L      #.#.#.#  ",
		"  #.....#        F   Q       P      #.#.#.#  ",
		"  ###.###########.###.#######.#########.###  ",
		"  #.....#...#.....#.......#...#.....#.#...#  ",
		"  #####.#.###.#######.#######.###.###.#.#.#  ",
		"  #.......#.......#.#.#.#.#...#...#...#.#.#  ",
		"  #####.###.#####.#.#.#.#.###.###.#.###.###  ",
		"  #.......#.....#.#...#...............#...#  ",
		"  #############.#.#.###.###################  ",
		"               A O F   N                     ",
		"               A A D   M                     ",
	])
	yield (part_two, (test_input, ), 396, )

for test in generate_tests():
	result = test[0](*test[1])
	message = f"{test[0].__name__}{test[1]!r} should be {test[2]}, got {result}"
	assert result == test[2], message

from pathlib import Path
with open(Path(__file__).with_suffix(".txt")) as file:
	parsed = parse_input(file)
	print(f"{part_one(parsed)=}")
	print(f"{part_two(parsed)=}")
