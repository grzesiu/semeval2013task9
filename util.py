def iob_to_features(iob_index, sentence_as_iobs):
    iob = sentence_as_iobs[iob_index]
    features = [
        'bias',
        'iob.lower=' + iob.text.lower(),
        'iob[-3:]=' + iob.text[-3:],
        'iob[-2:]=' + iob.text[-2:],
        'iob.isupper=%s' % iob.text.isupper(),
        'iob.istitle=%s' % iob.text.istitle(),
        'iob.isdigit=%s' % iob.text.isdigit(),
        'pos_tag=' + iob.pos_label,
        'pos_tag[:2]=' + iob.pos_label[:2],
    ]
    if iob_index > 0:
        iob_p = sentence_as_iobs[iob_index - 1]
        features.extend([
            '-1:iob.lower=' + iob_p.text.lower(),
            '-1:iob.istitle=%s' % iob_p.text.istitle(),
            '-1:iob.isupper=%s' % iob_p.text.isupper(),
            '-1:pos_tag=' + iob_p.pos_label,
            '-1:pos_tag[:2]=' + iob_p.pos_label[:2],
        ])
    else:
        features.append('BOS')

    if iob_index < len(sentence_as_iobs) - 1:
        iob_n = sentence_as_iobs[iob_index + 1]
        features.extend([
            '+1:iob.lower=' + iob_n.text.lower(),
            '+1:iob.istitle=%s' % iob_n.text.istitle(),
            '+1:iob.isupper=%s' % iob_n.text.isupper(),
            '+1:pos_tag=' + iob_n.pos_label,
            '+1:pos_tag[:2]=' + iob_n.pos_label[:2],
        ])
    else:
        features.append('EOS')

    return features


def sentence_to_features(sentence_as_iobs):
    return [iob_to_features(i, sentence_as_iobs) for i in range(len(sentence_as_iobs))]


def sentence_to_labels(sentence_as_iobs):
    return [iob.get_label() for iob in sentence_as_iobs]


def sentence_to_tokens(sentence_as_iobs):
    return [iob.text for iob in sentence_as_iobs]
