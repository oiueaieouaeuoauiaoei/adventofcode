def find_reachable_keys(passages, keys, doors, entrance, found_keys):
	missing_keys = {
		key_key
		for (key_key, key_value) in keys.items()
		if key_value not in found_keys
	}
	
	locked_doors = {
		door_key
		for (door_key, door_value) in doors.items()
		if door_value not in found_keys
	}
	
	reachable_keys = set()
	
	current_passages = {entrance, }
	touched = set()
	depth = 0
	while current_passages:
		depth += 1
		touched.update(current_passages)
		current_passages = {
			current - delta
			for current in current_passages
			for delta in {-1J, 1J, -1, 1, }
		}
		current_passages &= passages
		current_passages -= touched
		
		reachable_keys |= {
			(depth, key, )
			for key in (missing_keys & current_passages)
		}
		current_passages -= missing_keys
		current_passages -= locked_doors
	
	return reachable_keys

def part_one(tunnels):
	(passages, keys, doors, entrance, ) = tunnels
	
	def inner(entrance, found_keys):
		reachable_keys = find_reachable_keys(passages, keys, doors, entrance, found_keys)
		for (depth, key, ) in reachable_keys:
			deeper_entrance = key
			
			deeper_found_keys = set(found_keys)
			deeper_found_keys.add(keys[key])
			deeper_found_keys = frozenset(deeper_found_keys)
			
			yield depth + memoized_breadth_first_search(deeper_entrance, deeper_found_keys)
	
	memory = dict()
	def memoized_breadth_first_search(entrance, found_keys):
		memory_key = (entrance, found_keys, )
		if memory_key not in memory:
			memory[memory_key] = min(
				inner(entrance, found_keys),
				default=0,
			)
		return memory[memory_key]
	
	return memoized_breadth_first_search(entrance, frozenset())

def part_two(tunnels):
	(passages, keys, doors, entrance, ) = tunnels
	
	passages -= {
		entrance -1J,
		entrance -1,
		entrance,
		entrance +1,
		entrance +1J,
	}
	passages |= {
		entrance -1 -1J,
		entrance +1 -1J,
		entrance -1 +1J,
		entrance +1 +1J,
	}
	
	entrances = (
		entrance -1 -1J,
		entrance +1 -1J,
		entrance -1 +1J,
		entrance +1 +1J,
	)
	
	def inner(entrances, found_keys):
		for (index, entrance, ) in enumerate(entrances):
			reachable_keys = find_reachable_keys(passages, keys, doors, entrance, found_keys)
			for (depth, key, ) in reachable_keys:
				deeper_entrances = list(entrances)
				deeper_entrances[index] = key
				deeper_entrances = tuple(deeper_entrances)
				
				deeper_found_keys = set(found_keys)
				deeper_found_keys.add(keys[key])
				deeper_found_keys = frozenset(deeper_found_keys)
				
				yield depth + memoized_breadth_first_search(deeper_entrances, deeper_found_keys)
	
	memory = dict()
	def memoized_breadth_first_search(entrances, found_keys):
		memory_key = (entrances, found_keys, )
		if memory_key not in memory:
			memory[memory_key] = min(
				inner(entrances, found_keys),
				default=0,
			)
		return memory[memory_key]
	
	return memoized_breadth_first_search(entrances, frozenset())


def parse_input(input_file):
	lines = list()
	import csv
	for row in csv.reader(input_file, delimiter="\xFF"):
		assert 1 == len(row)
		lines.append(row[0])
	
	passages = set()
	entrance = None
	keys = dict()
	doors = dict()
	for (imag, line, ) in enumerate(lines):
		for (real, tile, ) in enumerate(line):
			coord = complex(real, imag)
			if "#" == tile:
				pass
			elif "." == tile:
				passages.add(coord)
			elif "@" == tile:
				passages.add(coord)
				entrance = coord
			elif tile in "abcdefghijklmnopqrstuvwxyz":
				passages.add(coord)
				keys[coord] = tile.lower()
			elif tile in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
				passages.add(coord)
				doors[coord] = tile.lower()
			else:
				raise Exception("unknown character in input")
	
	assert entrance is not None
	assert set(doors.values()) <= set(keys.values())
	
	return (passages, keys, doors, entrance, )

def generate_tests():
	yield (part_one, (parse_input([
		"#########",
		"#b.A.@.a#",
		"#########",
	]), ), 8, )
	yield (part_one, (parse_input([
		"########################",
		"#f.D.E.e.C.b.A.@.a.B.c.#",
		"######################.#",
		"#d.....................#",
		"########################",
	]), ), 86, )
	yield (part_one, (parse_input([
		"########################",
		"#...............b.C.D.f#",
		"#.######################",
		"#.....@.a.B.c.d.A.e.F.g#",
		"########################",
	]), ), 132, )
	yield (part_one, (parse_input([
		"#################",
		"#i.G..c...e..H.p#",
		"########.########",
		"#j.A..b...f..D.o#",
		"########@########",
		"#k.E..a...g..B.n#",
		"########.########",
		"#l.F..d...h..C.m#",
		"#################",
	]), ), 136, )
	yield (part_one, (parse_input([
		"########################",
		"#@..............ac.GI.b#",
		"###d#e#f################",
		"###A#B#C################",
		"###g#h#i################",
		"########################",
	]), ), 81, )
	
	yield (part_two, (parse_input([
		"#######",
		"#a.#Cd#",
		"##...##",
		"##.@.##",
		"##...##",
		"#cB#Ab#",
		"#######",
	]), ), 8, )
	yield (part_two, (parse_input([
		"#############",
		"#DcBa.#.GhKl#",
		"#.###...#I###",
		"#e#d#.@.#j#k#",
		"###C#...###J#",
		"#fEbA.#.FgHi#",
		"#############",
	]), ), 32, )
	yield (part_two, (parse_input([
		"#############",
		"#g#f.D#..h#l#",
		"#F###e#E###.#",
		"#dCba...BcIJ#",
		"#####.@.#####",
		"#nK.L...G...#",
		"#M###N#H###.#",
		"#o#m..#i#jk.#",
		"#############",
	]), ), 72, )

for test in generate_tests():
	result = test[0](*test[1])
	message = f"{test[0].__name__}{test[1]!r} should be {test[2]}, got {result}"
	assert result == test[2], message

from pathlib import Path
with open(Path(__file__).with_suffix(".txt")) as file:
	parsed = parse_input(file)
	print(f"{part_one(parsed)=}")
	print(f"{part_two(parsed)=}")
