import sys
import xml.etree.ElementTree

from structures.document import Document


def read(filename):
    tree = xml.etree.ElementTree.parse(filename)
    doc = Document.parse(tree.getroot())
    print(doc.sentences[0].entities[0].id_)


if __name__ == '__main__':
    read(sys.argv[1])
