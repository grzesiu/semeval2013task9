import argparse
import xml.etree.ElementTree

from structures.document import Document


def read(filename):
    tree = xml.etree.ElementTree.parse(filename)
    doc = Document.parse(tree.getroot())
    print(doc.sentences[0].entities[0].id_)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_dir', default='Train/DrugBank/', help='Train directory')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    print(args.train_dir)
