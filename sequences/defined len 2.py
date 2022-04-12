from random import choice

"""
Instead of looking for sequences in an already defined "list", like pi's digits (see pi.py),
We could try to generate our own, and optimize it (meaning, make sure there are no duplicates).

Here, the goal is to generated a such optimized list for 2 hexadecimal chars long sequences (int between 0 and 255).

Note: I did not find any better solution yet, so the generate() function is not deterministic
(as it uses random.choice()) nor perfect (given results might need some manual corrections).

However, here is an example of a list I could produce thanks to this algorithm:

5a346940efae6c6864d7367cd15e8518daa1e103bca619a7ac223752a5b0a271ffb55f0d62e7dbb7e56eba0908c5741d8ab96bea8bdd0133de206
53a4cce3142f39dfed2d4a9c1af7704f16d599e4b305dc9f4ee0f8454792b893f6f9581c0078e9b1297b2cb63cf24498350c48826ad911b43217f
d3ec766028fc38725c80bf5

Sadly, this sequence is... 257 chars long. The index of every 2 chars sequences is therefore between 0 and 255.
No compression possible, and such an interesting result.

"""


def generate():
    """
    Generate a list of every 2 hexadecimal chars combinations possible, optimized as described above.
    Note: Code is far from optimized, to say the least.
    :return: The generated list.
    """
    combis = []
    base = list("0123456789abcdef")

    for i in base:
        for j in base:
            combis.append(i + j)

    out = combis.pop()

    while len(combis) != 0:

        added_one = False

        for i in range(len(combis)):  # so we can modify the list in the loop
            last_chr = out[-1]
            first_chr = out[0]

            if len(combis) == 0:
                return out

            # item = combis[-1]
            item = choice(combis)
            if item in out:  # double check that we don't get any duplicate
                combis.remove(item)
                added_one = True
                continue

            if (last_chr + item[0]) in combis and (last_chr + item[0]) != item:
                out += item
                combis.remove(item)
                combis.remove(last_chr + item[0])
                added_one = True
                continue

            if (item[1] + first_chr) in combis and (item[1] + first_chr) != item:
                out = item + out
                combis.remove(item)
                combis.remove(item[1] + first_chr)
                added_one = True
                continue

        if not added_one:
            out += combis[-1]

    return out


def test(seq):
    base = list("0123456789abcdef")
    """
    print("[*] Testing out following sequence of length {}: ".format(len(seq)))
    print(seq)
    print("[*] in base : \"{}\"...".format(''.join(base)))
    """

    for i in base:
        for k in base:

            c = seq.count(i + k)

            if c == 0:
                print("[!] sequence not complete : \"{}\" not in sequence".format(i + k))
                return False
            elif c > 1:
                print("[*] subsequence \"{}\" more than once in the sequence (count = {})".format(i + k, c))
                return False

    print("Sequence is complete, but may not be optimal")
    return True


while True:
    s = generate()

    if test(s) and len(s) < 257:
        print("SUCCESS")
        print(s)
        print("len : " + str(len(s)))
        break
