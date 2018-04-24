from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

with open('DrugBank.csv', encoding="utf8") as f:
    names = f.read().splitlines()
names = set(names)


def common_tokens(text, type, n=10):  # Maybe treat these as separte feature and try if each of them improves the model?
    '''
        Check if the word contains any of the most common 2-gram and 3-gram, as done in 
        "UMCC_DLSI: Semantic and Lexical features for detection and classification Drugs in biomedical texts"
        Param:
            ::text: the string from which to extract the features
            ::type: whether it is the word itself (iob), the preceeding one (iob_p) or the following one (iob_n)
            ::n: the number of n-grams to consider (max = 10). The 10 most common n-grams are extracted from the paper and hardly encoded
    '''
    if n > 10:
        n = 10
    ngrams = ["in", "ne", "ine", "ti", "id", "an", "ro", "nt", "et", "en"]
    features = []
    for i in range(n):
        ng = ngrams[i]
        c = text.count(ng)
        features.append(
            type + "." + ng + "=" + str(c))  # Not sure if the algo is able to understand that this is a number
    return features


def issingular(text):
    ''' Return if a word is singular or plural - note, should be better evaluated to see if it works well with drugs 
        Note that it also returns singular if the word is unknown
    '''
    wnl = WordNetLemmatizer()
    lemma = wnl.lemmatize(text, 'n')
    return False if text is not lemma else True


def isInDrugDictionary(text):
    ''' Return if a drug is present in the WordBank dictionary (common names and synonyms are considered)
        Also, partial match should be implemented
    '''
    # r =  re.compile('.*'+text+'.*')
    if text in names:
        return "Match"
    # elif  any(r.match(line) for line in names):
    #    return "Match"
    else:
        return "NoMatch"


def iob_to_features(iob_index, sentence_as_iobs, sentence_id):
    iob = sentence_as_iobs[iob_index]

    ps = PorterStemmer()

    features = [
        'bias',
        'iob.lower=' + iob.text.lower(),
        'word.stem=' + ps.stem(iob.text),  # Used by Greg (=a) #
        'iob[:3]=' + iob.text[:3],  # Greg (-a) #
        'iob[:2]=' + iob.text[:2],  # Greg (-a) #
        'iob[-3:]=' + iob.text[-3:],
        'iob[-2:]=' + iob.text[-2:],
        'iob.isupper=%s' % iob.text.isupper(),
        'iob.istitle=%s' % iob.text.istitle(),
        'iob.isdigit=%s' % iob.text.isdigit(),
        'iob.singular=%s' % issingular(iob.text),  #
        'iob.isInDictionary=%s' % isInDrugDictionary(iob.text),  # (=a but diff numbers)
        'pos_tag=' + iob.pos_label,
        'pos_tag[:2]=' + iob.pos_label[:2],
    ]
    features.extend(common_tokens(iob.text, "iob", n=5))  # 5
    if iob_index > 0:
        iob_p = sentence_as_iobs[iob_index - 1]
        features.extend([
            '-1:iob.lower=' + iob_p.text.lower(),
            '-1:iob.stem=' + ps.stem(iob_p.text),  # (-a) #
            '-1:iob[-3:]=' + iob_p.text[-3:],  # (=a, !=c) #
            '-1:iob[-2:]=' + iob_p.text[-2:],  # (-a) #
            '-1:iob[:3]=' + iob_p.text[:3],  # Greg (-a) #
            '-1:iob[:2]=' + iob_p.text[:2],  # Greg (-a) #
            '-1:iob.istitle=%s' % iob_p.text.istitle(),
            '-1:iob.isupper=%s' % iob_p.text.isupper(),
            '-1:iob.singular=%s' % issingular(iob_p.text),  #
            '-1:iob.isInDictionary=%s' % isInDrugDictionary(iob_p.text),  # (-a) #
            '-1:pos_tag=' + iob_p.pos_label,
            '-1:pos_tag[:2]=' + iob_p.pos_label[:2],
        ])
        features.extend(common_tokens(iob_p.text, "-1:iob", n=10))  # (-a) #
    else:
        features.append('BOS')

    if iob_index < len(sentence_as_iobs) - 1:
        iob_n = sentence_as_iobs[iob_index + 1]
        features.extend([
            '+1:iob.lower=' + iob_n.text.lower(),
            '+1:iob.stem=' + ps.stem(iob_n.text),  # (-a)  #
            '+1:iob[-3:]=' + iob_n.text[-3:],  # (-a) #
            '+1:iob[-2:]=' + iob_n.text[-2:],  # (+a) !
            '+1:iob[:3]=' + iob_n.text[:3],  # Greg (-a) #
            '+1:iob[:2]=' + iob_n.text[:2],  # Greg (-a) #
            '+1:iob.istitle=%s' % iob_n.text.istitle(),
            '+1:iob.isupper=%s' % iob_n.text.isupper(),
            '+1:iob.singular=%s' % issingular(iob_n.text),  #
            '+1:iob.isInDictionary=%s' % isInDrugDictionary(iob_n.text),
            '+1:pos_tag=' + iob_n.pos_label,
            '+1:pos_tag[:2]=' + iob_n.pos_label[:2],
        ])
        features.extend(common_tokens(iob_n.text, "+1:iob", n=10))  # (-a) #
    else:
        features.append('EOS')

    return features, iob.get_label(), sentence_id, iob.offset, iob.text


def sentence_to_features(sentence):
    sentence_as_iobs = sentence.to_iobs()
    return [iob_to_features(i, sentence_as_iobs, sentence.id_) for i in range(len(sentence_as_iobs))]
