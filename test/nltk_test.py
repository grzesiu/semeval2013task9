from nltk import word_tokenize, pos_tag, ne_chunk
from nltk import conlltags2tree, tree2conlltags


tree = ne_chunk(pos_tag(word_tokenize("4-ethyl-1-(2'-hydroxyethyl)-3-hydroxypyridin-4-one")))
print(tree)
# (S (GPE New/NNP York/NNP) is/VBZ my/PRP$ favorite/JJ city/NN)

iob_tags = tree2conlltags(tree)
print(iob_tags)
# [('New', 'NNP', u'B-GPE'), ('York', 'NNP', u'I-GPE'), ('is', 'VBZ', u'O'), ('my', 'PRP$', u'O'), ('favorite', 'JJ', u'O'), ('city', 'NN', u'O')]

tree = conlltags2tree(iob_tags)
print(tree)
# (S (GPE New/NNP York/NNP) is/VBZ my/PRP$ favorite/JJ city/NN)
