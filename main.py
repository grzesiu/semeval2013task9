import argparse
import os
import xml.etree.ElementTree

from structures.document import Document


def read(filename):
    tree = xml.etree.ElementTree.parse(filename)
    return Document.parse(tree.getroot())


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_dir', default='Train/SmallDrugBank/', help='Train directory')
    return parser.parse_args()


def test_labeling():
    args = parse_args()
    docs = [read(os.path.join(args.train_dir, filename)) for filename in os.listdir(args.train_dir)]
    print(docs[0].sentences[1].text.get_split())


def main():
    test_labeling()


if __name__ == '__main__':
    main()
