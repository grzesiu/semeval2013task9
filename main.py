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
    parser.add_argument('--train', type=str, help='Train directory')
    parser.add_argument('--test', type=str, help='Test directory')
    parser.add_argument('--tune', help='Should tune the parameters', action='store_true')
    parser.add_argument('--save', help='Should save the output', action='store_true')
    return parser.parse_args()


def extract_data(directory):
    docs = [Document.from_file(os.path.join(directory, filename))
            for filename in os.listdir(directory)]
    data = [util.sentence_to_features(sentence) for doc in docs for sentence in doc.sentences]
    x, y, ids, offsets, texts = zip(*[zip(*i) for i in data])
    return x, y


def train(x_train, y_train, c1=1.0, c2=1e-3, max_iterations=100, possible_transitions=True):
    trainer = pycrfsuite.Trainer(verbose=False)

    for x_seq, y_seq in zip(x_train, y_train):
        trainer.append(x_seq, y_seq)

    trainer.set_params({
        'c1': c1,  # coefficient for L1 penalty
        'c2': c2,  # coefficient for L2 penalty
        'max_iterations': max_iterations,  # stop earlier
        'feature.possible_transitions': possible_transitions  # include transitions that are possible, but not observed
    })
    trainer.train('model_0.crfsuite')


# def predict(tagger, test_sentence):
#     print(test_sentence)
#     iobs = test_sentence.to_iobs()
#     print("Predicted:", ' '.join(tagger.tag(util.sentence_to_features(iobs))))
#     print("Correct:  ", ' '.join(util.sentence_to_labels(iobs)))


def evaluate(x_test, y_test):
    tagger = pycrfsuite.Tagger()
    tagger.open('model_0.crfsuite')
    y_pred = [tagger.tag(i) for i in x_test]
    print(bio_classification_report(y_test, y_pred))


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


def tune(x_train, y_train, x_test, y_test):
    for c2 in [1e-3, 1e-2, 1e-1, 1, 10, 100]:
        for possible_transitions in [True, False]:
            print("c1=" + str(0) + ", c2=" + str(c2) + ", trans=" + str(possible_transitions))
            train(x_train, y_train, c1=0, c2=c2, max_iterations=1000, possible_transitions=possible_transitions)
            evaluate(x_test, y_test)


def save():
    pass


def main():
    args = parse_args()
    x_train, y_train, x_test, y_test = None, None, None, None

    if args.train:
        x_train, y_train = extract_data(args.train)
        train(x_train, y_train, c1=0.001, c2=1, max_iterations=1000, possible_transitions=True)

    if args.test and not args.tune:
        x_test, y_test = extract_data(args.test)
        evaluate(x_test, y_test)

        if args.save:
            save()

    elif args.tune and args.train and args.test:
        tune(x_train, y_train, x_test, y_test)

        if args.save:
            save()


if __name__ == '__main__':
    main()
