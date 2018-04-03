import argparse
import os
import xml.etree.ElementTree

from structures.document import Document
from util import text2iob


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
    print(docs[0].sentences[0].features)
    print(docs[0].sentences[0].labels)


def test_converting():
    text = "1.2Na' Na+ Na(+) 1,2-(carboxyalkyl)hydroxypyridinones, (carboxyalkyl)hydroxypyridinone [2-(acetylamino)-2-carbomethoxyethyl]sulfenyl"
    print(text2iob(text))


def main():
    test_converting()


if __name__ == '__main__':
    main()
