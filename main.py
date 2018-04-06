import argparse
import os
from itertools import chain

import pycrfsuite
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelBinarizer

import util
from structures.document import Document


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_dir', default='Train/DrugBank/', help='Train directory')
    parser.add_argument('--test_dir', default='Test/Test for DrugNER task/DrugBank', help='Test directory')
    return parser.parse_args()


def read_docs(directory):
    train_docs = [Document.from_file(os.path.join(directory, filename))
                  for filename in os.listdir(directory)]
    return train_docs


def extract_data(docs):
    sentences_as_iobs = [sentence.to_iobs() for doc in docs for sentence in doc.sentences]
    x = [util.sentence_to_features(sentence_as_iobs) for sentence_as_iobs in sentences_as_iobs]
    y = [util.sentence_to_labels(sentence_as_iobs) for sentence_as_iobs in sentences_as_iobs]
    return x, y


def train(x_train, y_train):
    trainer = pycrfsuite.Trainer(verbose=False)

    for x_seq, y_seq in zip(x_train, y_train):
        trainer.append(x_seq, y_seq)

    trainer.set_params({
        'c1': 1.0,  # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty
        'max_iterations': 50,  # stop earlier
        'feature.possible_transitions': True  # include transitions that are possible, but not observed
    })
    trainer.train('model_0.crfsuite')


def predict(tagger, test_sentence):
    print(test_sentence)
    iobs = test_sentence.to_iobs()
    print("Predicted:", ' '.join(tagger.tag(util.sentence_to_features(iobs))))
    print("Correct:  ", ' '.join(util.sentence_to_labels(iobs)))


def bio_classification_report(y_true, y_pred):
    lb = LabelBinarizer()
    y_true_combined = lb.fit_transform(list(chain.from_iterable(y_true)))
    y_pred_combined = lb.transform(list(chain.from_iterable(y_pred)))

    tag_set = set(lb.classes_) - {'O'}
    tag_set = sorted(tag_set, key=lambda tag: tag.split('-', 1)[::-1])
    class_indices = {cls: idx for idx, cls in enumerate(lb.classes_)}

    return classification_report(
        y_true_combined,
        y_pred_combined,
        labels=[class_indices[cls] for cls in tag_set],
        target_names=tag_set,
    )


def evaluate(x_test, y_test):
    tagger = pycrfsuite.Tagger()
    tagger.open('model_0.crfsuite')
    y_pred = [tagger.tag(i) for i in x_test]
    print(bio_classification_report(y_test, y_pred))


def main():
    args = parse_args()
    train_docs = read_docs(args.train_dir)
    test_docs = read_docs(args.test_dir)
    x_train, y_train = extract_data(train_docs)
    x_test, y_test = extract_data(test_docs)

    train(x_train, y_train)
    evaluate(x_test, y_test)


if __name__ == '__main__':
    main()
