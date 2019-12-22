def compute_ab(techniques, length):
	# in search of the function f such that
	# f(card_index) = card_index *a +b = card_number
	# in the ring of integers modulo length
	
	# we start with an identity function (the deck in factory order)
	(a, b, ) = (1, 0, )
	
	for (technique, amount, ) in techniques:
		if "into" == technique:
			a *= -1
			b += a
		elif "with" == technique:
			# while you could get a “ValueError: base is not invertible for the given modulus”
			# today’s puzzle tells you to assume an inverse element always exist, so let’s
			a *= pow(amount, -1, length)
		elif "cut" == technique:
			b += a *amount
		else:
			raise Exception((technique, amount, ))
		
		a %= length
		b %= length
	
	return (a, b, )

def apply_shuffle(techniques, length):
	(a, b, ) = compute_ab(techniques, length)
	
	return tuple(
		(i *a +b) %length
		for i in range(length)
	)

def part_one(techniques):
	return apply_shuffle(techniques, 10007).index(2019)

def part_one_bis(techniques):
	length = 10007
	(a, b, ) = compute_ab(techniques, length)
	
	result = 2019
	result -= b
	result *= pow(a, -1, length)
	result %= length
	return result

def part_two(techniques):
	length = 119315717514047
	repeats = 101741582076661
	
	(a, b, ) = compute_ab(techniques, length)
	
	# from the closed form of ([[a, b, ], [0, 1, ], ] **repeats)
	# combined with being in a finite field (length is prime)
	(a, b, ) = (
		pow(a, repeats, length),
		b * (pow(a, repeats, length) -1) * pow((a -1), -1, length),
	)
	
	return (2020 *a +b) %length


def parse_input(lines):
	parsed = list()
	
	import re
	into_regex = re.compile(r"""deal\x20into\x20new\x20stack""")
	with_regex = re.compile(r"""deal\x20with\x20increment\x20(?P<amount>[0-9]+)""")
	cut_regex = re.compile(r"""cut\x20(?P<amount>\x2D?[0-9]+)""")
	
	for line in lines:
		if (match := into_regex.fullmatch(line)):
			parsed.append(("into", None, ))
		elif (match := with_regex.fullmatch(line)):
			parsed.append(("with", int(match["amount"], base=10), ))
		elif (match := cut_regex.fullmatch(line)):
			parsed.append(("cut", int(match["amount"], base=10), ))
		else:
			raise Exception(line)
	
	return parsed

def generate_tests():
	test_input = parse_input([
		"deal with increment 7",
		"deal into new stack",
		"deal into new stack",
	])
	yield (apply_shuffle, (test_input, 10, ), (0, 3, 6, 9, 2, 5, 8, 1, 4, 7, ), )
	
	test_input = parse_input([
		"cut 6",
		"deal with increment 7",
		"deal into new stack",
	])
	yield (apply_shuffle, (test_input, 10, ), (3, 0, 7, 4, 1, 8, 5, 2, 9, 6, ), )
	
	test_input = parse_input([
		"deal with increment 7",
		"deal with increment 9",
		"cut -2",
	])
	yield (apply_shuffle, (test_input, 10, ), (6, 3, 0, 7, 4, 1, 8, 5, 2, 9, ), )
	
	test_input = parse_input([
		"deal into new stack",
		"cut -2",
		"deal with increment 7",
		"cut 8",
		"cut -4",
		"deal with increment 7",
		"cut 3",
		"deal with increment 9",
		"deal with increment 3",
		"cut -1",
	])
	yield (apply_shuffle, (test_input, 10, ), (9, 2, 5, 8, 1, 4, 7, 0, 3, 6, ), )

for test in generate_tests():
	result = test[0](*test[1])
	message = f"{test[0].__name__}{test[1]!r} should be {test[2]}, got {result}"
	assert result == test[2], message

from pathlib import Path
with open(Path(__file__).with_suffix(".txt")) as file:
	parsed = parse_input(file.read().splitlines(keepends=False))
	print(f"{part_one(parsed)=}")
	print(f"{part_one_bis(parsed)=}")
	print(f"{part_two(parsed)=}")
