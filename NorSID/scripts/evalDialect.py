#! /usr/bin/env python3

import sys, re, string, collections

def readData(path):
    sentences = []
    labels = []
    for line in open(path):
        line = line.strip()
        if line.startswith('# text ='):
            sentences.append(line.split("=", 1)[1].strip())
        elif line.startswith('# dialect ='):
            labels.append(line.split("=", 1)[1].strip())
    assert(len(sentences) == len(labels))
    return sentences, labels

def normalizeSentence(s):
    s = re.sub(r'\s+', ' ', s)
    s = s.translate(str.maketrans("","", string.punctuation))
    s = s.lower()
    s = s.strip()
    return s

def makeSets(sentences, labels):
    data = collections.defaultdict(set)
    for s, l in zip(sentences, labels):
        s = normalizeSentence(s)
        l = set([x.strip() for x in l.split(",")])
        data[s].update(l)
    return data

def evaluate(goldSets, predSets):
    allSentences = sorted(goldSets.keys())
    allLabels = ["B", "N", "T", "V"]
    tp = {l: 0 for l in allLabels}
    fp = {l: 0 for l in allLabels}   # pred but not gold
    fn = {l: 0 for l in allLabels}   # gold but not pred
    tn = {l: 0 for l in allLabels}
    support = {l: 0 for l in allLabels}
    jaccard = 0
    for s in sorted(allSentences):
        goldSet = goldSets[s]
        predSet = predSets[s] if s in predSets else set()
        jaccard += len(goldSet & predSet) / len(goldSet | predSet)
        for l in allLabels:
            if l in goldSet and l in predSet:
                tp[l] += 1
            elif l in goldSet:
                fn[l] += 1
            elif l in predSet:
                fp[l] += 1
            else:
                tn[l] += 1
            if l in goldSet:
                support[l] += 1
    jaccard = jaccard / len(allSentences)
    
    prec = {}
    rec = {}
    f1 = {}
    for d in allLabels:
        prec[d] = 0.0 if tp[d]+fp[d] == 0 else tp[d]/(tp[d]+fp[d])
        rec[d] = 0.0 if tp[d]+fn[d] == 0 else tp[d]/(tp[d]+fn[d])
        f1[d] = 0.0 if prec[d]+rec[d] == 0.0 else 2 * (prec[d] * rec[d]) / (prec[d] + rec[d])
    
    prec["micro"] = 0.0 if sum(tp.values())+sum(fp.values()) == 0 else sum(tp.values())/(sum(tp.values())+sum(fp.values()))
    prec["macro"] = sum([prec[d] for d in allLabels]) / len(allLabels)
    prec["weighted"] = sum([prec[d] * (support[d] / sum(support.values())) for d in allLabels])
    rec["micro"] = 0.0 if sum(tp.values())+sum(fn.values()) == 0 else sum(tp.values())/(sum(tp.values())+sum(fn.values()))
    rec["macro"] = sum([rec[d] for d in allLabels]) / len(allLabels)
    rec["weighted"] = sum([rec[d] * (support[d] / sum(support.values())) for d in allLabels])
    f1["micro"] = 0.0 if prec["micro"]+rec["micro"] == 0.0 else 2 * (prec["micro"] * rec["micro"]) / (prec["micro"] + rec["micro"])
    f1["macro"] = 0.0 if prec["macro"]+rec["macro"] == 0.0 else 2 * (prec["macro"] * rec["macro"]) / (prec["macro"] + rec["macro"])
    f1["weighted"] = 0.0 if prec["weighted"]+rec["weighted"] == 0.0 else 2 * (prec["weighted"] * rec["weighted"]) / (prec["weighted"] + rec["weighted"])

    labels = sorted(prec.keys())
    print("          ", "  ".join(["{: <6}".format(x) for x in labels]))
    print("precision ", "  ".join(["{:.4f}".format(prec[x]) for x in labels]))
    print("recall    ", "  ".join(["{:.4f}".format(rec[x]) for x in labels]))
    print("f1-score  ", "  ".join(["{:.4f}".format(f1[x]) for x in labels]))
    print("jaccard       {:.4f}".format(jaccard))
    print()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('please provide paths to gold and predicted data')
        sys.exit(1)
    goldSentences, goldLabels = readData(sys.argv[1])
    goldData = makeSets(goldSentences, goldLabels)
    predSentences, predLabels = readData(sys.argv[2])
    predData = makeSets(predSentences, predLabels)
    print(sys.argv[2])
    evaluate(goldData, predData)
