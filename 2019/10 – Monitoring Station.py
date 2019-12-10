import cmath
def part_one(asteroids):
	return max(
		len(set(
			cmath.phase(station - asteroid)
			for asteroid in asteroids - {station}
		))
		for station in asteroids
	)

def part_two(asteroids):
	station = max(
		asteroids,
		key=lambda station: len(set(
			cmath.phase(station - asteroid)
			for asteroid in asteroids - {station}
		))
	)
	
	almost_sorted_asteroids = sorted(
		(
			cmath.phase((asteroid - station) * complex(0, -1)),
			abs(asteroid - station),
			asteroid,
		)
		for asteroid in asteroids - {station}
	)
	
	last_phase = None
	index = None
	transposed = list()
	for (t, r, asteroid, ) in almost_sorted_asteroids:
		if last_phase != t:
			last_phase = t
			index = 0
		
		if len(transposed) <= index:
			transposed.append(list())
		
		transposed[index].append(asteroid)
		index += 1
	
	sorted_asteroids = list(
		asteroid
		for asteroids in transposed
		for asteroid in asteroids
	)
	
	return int(sorted_asteroids[199].real*100 + sorted_asteroids[199].imag)

# some assumptions are required, but they seem to hold true
def part_two_bis(asteroids):
	station = max(
		asteroids,
		key=lambda station: len(set(
			cmath.phase(station - asteroid)
			for asteroid in asteroids - {station}
		))
	)
	
	asteroid_cache = dict()
	for asteroid in asteroids - {station}:
		(r, t, ) = cmath.polar((asteroid - station) * complex(0, -1))
		if t not in asteroid_cache or asteroid_cache[t][0] < r:
			asteroid_cache[t] = (r, asteroid, )
	
	sorted_asteroids = list(
		asteroid_cache[key][1]
		for key in sorted(asteroid_cache.keys())
	)
	
	return int(sorted_asteroids[199].real*100 + sorted_asteroids[199].imag)


def parse_input(input_file):
	parsed = set()
	
	import csv
	for (y, row, ) in enumerate(csv.reader(input_file, delimiter="\xFF")):
		assert 1 == len(row)
		for cell in row:
			for (x, spot, ) in enumerate(cell):
				assert spot in {"\x23", "\x2E", }, repr(spot)
				if "\x23" == spot:
					parsed.add(complex(x, y, ))
	
	return parsed

def generate_tests():
	test_input = parse_input([
		".#..#",
		".....",
		"#####",
		"....#",
		"...##",
	])
	yield (part_one, (test_input, ), 8, )
	
	test_input = parse_input([
		"......#.#.",
		"#..#.#....",
		"..#######.",
		".#.#.###..",
		".#..#.....",
		"..#....#.#",
		"#..#....#.",
		".##.#..###",
		"##...#..#.",
		".#....####",
	])
	yield (part_one, (test_input, ), 33, )
	
	test_input = parse_input([
		"#.#...#.#.",
		".###....#.",
		".#....#...",
		"##.#.#.#.#",
		"....#.#.#.",
		".##..###.#",
		"..#...##..",
		"..##....##",
		"......#...",
		".####.###.",
	])
	yield (part_one, (test_input, ), 35, )
	
	test_input = parse_input([
		".#..#..###",
		"####.###.#",
		"....###.#.",
		"..###.##.#",
		"##.##.#.#.",
		"....###..#",
		"..#.#..#.#",
		"#..#.#.###",
		".##...##.#",
		".....#.#..",
	])
	yield (part_one, (test_input, ), 41, )
	
	test_input = parse_input([
		".#..##.###...#######",
		"##.############..##.",
		".#.######.########.#",
		".###.#######.####.#.",
		"#####.##.#.##.###.##",
		"..#####..#.#########",
		"####################",
		"#.####....###.#.#.##",
		"##.#################",
		"#####.##.###..####..",
		"..######..##.#######",
		"####.##.####...##..#",
		".#####..#.######.###",
		"##...#.##########...",
		"#.##########.#######",
		".####.#.###.###.#.##",
		"....##.##.###..#####",
		".#.#.###########.###",
		"#.#.#.#####.####.###",
		"###.##.####.##.#..##",
	])
	yield (part_one, (test_input, ), 210, )
	yield (part_two, (test_input, ), 802, )

for test in generate_tests():
	result = test[0](*test[1])
	message = f"{test[0].__name__}{test[1]!r} should be {test[2]}, got {result}"
	assert result == test[2], message

from pathlib import Path
with open(Path(__file__).with_suffix(".txt")) as file:
	parsed = parse_input(file)
	print(f"{part_one(parsed)=}")
	print(f"{part_two(parsed)=}")
	print(f"{part_two_bis(parsed)=}")
