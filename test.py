import nltk

text = nltk.word_tokenize(
    "The majority of patients in RA clinical studies received one or more of the following concomitant medications with ORENCIA: MTX, NSAIDs, corticosteroids, TNF blocking agents, azathioprine, chloroquine, gold, hydroxychloroquine, leflunomide, sulfasalazine, and anakinra.")
print(nltk.pos_tag(text))
