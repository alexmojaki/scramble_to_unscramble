import json
import random

import itertools


def get_path():
    with open("/tmp/word_data.json") as f:
        all_data = json.load(f)

    data = all_data["6"]

    while True:
        seen = set()
        path = []
        node = random.choice(list(data))
        while True:
            seen.add(node)
            words, neighbors = data[node]
            path.append(random.choice(words))
            options = set(neighbors) - seen
            if not options:
                if len(seen) > 40:
                    return path
                break
            node = random.choice(list(options))


def main():
    path = get_path()

    num_actual_options = 7
    options = path[:num_actual_options] + [""] * 3
    random.shuffle(options)

    letters = "".join(random.sample(path[0], len(path[0])))
    message = ""

    for path_index, current_word in enumerate(path):
        letters = "".join(
            max(
                itertools.permutations(current_word),
                key=lambda w: sum(map(str.__eq__, w, letters)),
            )
        )
        answer_index = options.index(current_word)
        empty_indices = [i for i, option in enumerate(options) if not option]
        new_word = path[path_index + num_actual_options]
        new_index = random.choice(empty_indices)

        while True:
            print("\n" * 100)

            for i, word in enumerate(options):
                print(f"{i}. {word}")

            print()
            print(letters)
            print()
            print(message)
            print()

            num = input("Number? ")
            if num == str(answer_index):
                message = "Correct!"
                options[new_index] = new_word
                options[answer_index] = ""
                break
            else:
                message = "Wrong!"


main()
