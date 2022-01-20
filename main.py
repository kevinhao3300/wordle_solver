import re
from collections import Counter, defaultdict
from string import ascii_lowercase


with open('words.txt') as f:
    words = f.read().split()


# all known letters, min amount and max amount
letter_min_max = defaultdict(lambda: [0, float('inf')])
# pattern of known letters
pattern = None
# letter to banned positions for that letter
banned_pos = defaultdict(set)
print("result should be a string of 0 (incorrect), 1 (wrong position), and 2 (correct position)")
while True:
    guess = input("Enter the word you guessed: ")
    # start
    if pattern is None:
        pattern = ['.'] * len(guess)
        # match length
        words = list(filter(lambda word: len(word) == len(guess), words))

    # next line is labels, 0 for wrong, 1 for wrong pos, 2 for correct pos
    labels = input("Enter the result: ")
    if not (len(labels) == len(guess) == len(pattern)):
        raise Exception("length mismatch")
    # store letter plus all labels
    label_counts = defaultdict(lambda: [0, 0, 0])
    for index, (letter, label) in enumerate(zip(guess, labels)):
        label = int(label)
        label_counts[letter][label] += 1

        if label == 1:
            banned_pos[letter].add(index)
        elif label == 2:
            pattern[index] = letter

    for letter, (zeros, ones, twos) in label_counts.items():
        cur_min = ones + twos
        letter_min_max[letter][0] = cur_min
        if zeros and cur_min:
            letter_min_max[letter][1] = cur_min
    new_words = []
    for word in words:
        # match pattern
        if not re.match(''.join(pattern), word):
            continue
        # make sure haven't ruled out this letter in this position
        if any(idx in banned_pos[letter] for idx, letter in enumerate(word)):
            continue
        # make sure letter counts line up
        letter_count = Counter(word)
        if not all(minimum <= letter_count[letter] <= maximum for letter, (minimum, maximum) in letter_min_max.items()):
            continue

        new_words.append(word)
    if not new_words:
        raise Exception("no matches")

    words = new_words
    print(words)
