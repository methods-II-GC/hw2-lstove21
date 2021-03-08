#!/usr/bin/env python
"""Splits the data into four paths: input, train, dev, and test."""

import argparse
import random
from typing import Iterator, List


def main(args: argparse.Namespace) -> None:
    def read_tags(path: str) -> Iterator[List[List[str]]]:
        with open(path, "r") as source:
            lines = []
            for line in source:
                line = line.rstrip()
                if line:  # Line is contentful.
                    lines.append(line.split())
                else:  # Line is blank.
                    yield lines.copy()
                    lines.clear()
        # Just in case someone forgets to put a blank line at the end...
        if lines:
            yield lines

    def write_tags(a_list, a_file):
        for i in a_list:
            for word in i:
                my_str = " ".join(word)
                with open(a_file, "a") as sink:
                    print(my_str, file=sink)

    corpus = list(read_tags(args.input))
    corpus.sort()
    random.seed(args.seed)
    random.shuffle(corpus)
    
    split_1 = int(0.8 * len(corpus))
    split_2 = int(0.9 * len(corpus))
    train_corpus = corpus[:split_1]
    dev_corpus = corpus[split_1:split_2]
    test_corpus = corpus[split_2:]

    write_tags(train_corpus, args.train)
    write_tags(dev_corpus, args.dev)
    write_tags(test_corpus, args.test)

     

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input data")
    parser.add_argument("train", help="training data")
    parser.add_argument("dev", help="dev set")
    parser.add_argument("test", help="test set")
    parser.add_argument("--seed", type=int, required=True)
    main(parser.parse_args())
