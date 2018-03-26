import argparse
import os
import xml.etree.ElementTree

from structures.document import Document


def read(filename):
    tree = xml.etree.ElementTree.parse(filename)
    return Document.parse(tree.getroot())


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_dir', default='Train/DrugBank/', help='Train directory')
    return parser.parse_args()


def main():
    args = parse_args()
    for filename in os.listdir(args.train_dir):
        print(filename)
        read(os.path.join(args.train_dir, filename))


if __name__ == '__main__':
    main()
