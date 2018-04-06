def test_labeling(docs):
    print(docs[0].sentences[1].text)
    print(docs[0].sentences[1].entities)


def test_iob_tagging(docs):
    for iob in docs[0].sentences[1].to_iobs():
        print(iob)
