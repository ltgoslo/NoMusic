import sys, collections

def readNlu(path):
    slots = []
    intents = []
    dialects = []
    curSlots = []
    for line in open(path):
        line = line.strip()
        if line.startswith('# intent: '):
            intents.append(line.split(":", 1)[1].strip())
        elif line.startswith('# intent ='):
            intents.append(line.split("=", 1)[1].strip())
        if line.startswith('# dialect: '):
            dialects.append(line.split(":", 1)[1].strip())
        elif line.startswith('# dialect ='):
            dialects.append(line.split("=", 1)[1].strip())
        if line == '':
            slots.append(curSlots)
            curSlots = []
        elif line[0] == '#' and len(line.split('\t')) == 1:
            continue
        else:
            curSlots.append(line.split('\t')[-1])
    return slots, intents, dialects

def toSpans(tags):
    spans = set()
    for beg in range(len(tags)):
        if tags[beg][0] == 'B':
            end = beg
            for end in range(beg+1, len(tags)):
                if tags[end][0] != 'I':
                    break
            spans.add(str(beg) + '-' + str(end) + ':' + tags[beg][2:])
    return spans

def getBegEnd(span):
    return [int(x) for x in span.split(':')[0].split('-')]

def getLooseOverlap(spans1, spans2):
    found = 0
    for spanIdx, span in enumerate(spans1):
        spanBeg, spanEnd = getBegEnd(span)
        label = span.split(':')[1]
        match = False
        for span2idx, span2 in enumerate(spans2):
            span2Beg, span2End = getBegEnd(span2)
            label2 = span2.split(':')[1]
            if label == label2:
                if span2Beg >= spanBeg and span2Beg <= spanEnd:
                    match = True
                if span2End <= spanEnd and span2End >= spanBeg:
                    match = True
        if match:
            found += 1
    return found

def getUnlabeled(spans1, spans2):
    return len(set([x.split('-')[0] for x in spans1]).intersection([x.split('-')[0] for x in spans2]))

def getInstanceScores(predPath, goldPath):
    goldSlots, goldIntents = readNlu(goldPath)
    predSlots, predIntents = readNlu(predPath)
    intentScores = []
    slotScores = []
    for goldSlot, goldIntent, predSlot, predIntent in zip(goldSlots, goldIntents, predSlots, predIntents):
        if goldIntent == predIntent:
            intentScores.append(100.0)
        else:
            intentScores.append(0.0)
        
        goldSpans = toSpans(goldSlot)
        predSpans = toSpans(predSlot)
        overlap = len(goldSpans.intersection(predSpans))
        tp = overlap
        fp = len(predSpans) - overlap
        fn = len(goldSpans) - overlap
        
        prec = 0.0 if tp+fp == 0 else tp/(tp+fp)
        rec = 0.0 if tp+fn == 0 else tp/(tp+fn)
        f1 = 0.0 if prec+rec == 0.0 else 2 * (prec * rec) / (prec + rec)
        slotScores.append(f1)
    return slotScores, intentScores
    

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('please provide paths to gold and predicted data')
    goldSlots, goldIntents, goldDialects = readNlu(sys.argv[1])
    predSlots, predIntents, _ = readNlu(sys.argv[2])
    
    tp = collections.defaultdict(int)
    fp = collections.defaultdict(int)
    fn = collections.defaultdict(int)
    fullyCor = collections.defaultdict(int)
    corIntents = collections.defaultdict(int)
    slotCounts = collections.defaultdict(int)
    
    recall_loose_tp = collections.defaultdict(int)
    recall_loose_fn = collections.defaultdict(int)
    precision_loose_tp = collections.defaultdict(int)
    precision_loose_fp = collections.defaultdict(int)
    
    tp_ul = collections.defaultdict(int)
    fp_ul = collections.defaultdict(int)
    fn_ul = collections.defaultdict(int) 
    
    for goldSlot, goldIntent, predSlot, predIntent, dialect in zip(goldSlots, goldIntents, predSlots, predIntents, goldDialects):
        #print(goldSlot, goldIntent, predSlot, predIntent, dialect)
        # intents
        if goldIntent == predIntent:
            corIntents[dialect] += 1
    
        # slots
        slotCounts[dialect] += 1

        goldSpans = toSpans(goldSlot)
        predSpans = toSpans(predSlot)
        overlap = len(goldSpans.intersection(predSpans))
        tp[dialect] += overlap
        fp[dialect] += len(predSpans) - overlap
        fn[dialect] += len(goldSpans) - overlap
        
        overlap_ul = getUnlabeled(goldSpans, predSpans)
        tp_ul[dialect] += overlap_ul
        fp_ul[dialect] += len(predSpans) - overlap_ul
        fn_ul[dialect] += len(goldSpans) - overlap_ul
    
        overlapLoose = getLooseOverlap(goldSpans, predSpans)
        recall_loose_tp[dialect] += overlapLoose
        recall_loose_fn[dialect] += len(goldSpans) - overlapLoose
    
        overlapLoose = getLooseOverlap(predSpans, goldSpans)
        precision_loose_tp[dialect] += overlapLoose
        precision_loose_fp[dialect] += len(predSpans) - overlapLoose
    
        # fully correct sentences
        if overlap == len(goldSpans) and len(goldSpans) == len(predSpans) and goldIntent == predIntent:
            fullyCor[dialect] += 1
    
    corIntents["all"] = sum(corIntents.values())
    fullyCor["all"] = sum(fullyCor.values())
    slotCounts["all"] = sum(slotCounts.values())
    tp["all"] = sum(tp.values())
    fp["all"] = sum(fp.values())
    fn["all"] = sum(fn.values())
    tp_ul["all"] = sum(tp_ul.values())
    fp_ul["all"] = sum(fp_ul.values())
    fn_ul["all"] = sum(fn_ul.values())
    recall_loose_tp["all"] = sum(recall_loose_tp.values())
    recall_loose_fn["all"] = sum(recall_loose_fn.values())
    precision_loose_tp["all"] = sum(precision_loose_tp.values())
    precision_loose_fp["all"] = sum(precision_loose_fp.values())

    prec = {}
    rec = {}
    f1 = {}
    prec_ul = {}
    rec_ul = {}
    f1_ul = {}
    prec_loose = {}
    rec_loose = {}
    f1_loose = {}

    for d in corIntents.keys():
        prec[d] = 0.0 if tp[d]+fp[d] == 0 else tp[d]/(tp[d]+fp[d])
        rec[d] = 0.0 if tp[d]+fn[d] == 0 else tp[d]/(tp[d]+fn[d])
        f1[d] = 0.0 if prec[d]+rec[d] == 0.0 else 2 * (prec[d] * rec[d]) / (prec[d] + rec[d])

        prec_ul[d] = 0.0 if tp_ul[d]+fp_ul[d] == 0 else tp_ul[d]/(tp_ul[d]+fp_ul[d])
        rec_ul[d] = 0.0 if tp_ul[d]+fn_ul[d] == 0 else tp_ul[d]/(tp_ul[d]+fn_ul[d])
        f1_ul[d] = 0.0 if prec_ul[d]+rec_ul[d] == 0.0 else 2 * (prec_ul[d] * rec_ul[d]) / (prec_ul[d] + rec_ul[d])

        prec_loose[d] = 0.0 if precision_loose_tp[d] + precision_loose_fp[d] == 0 else precision_loose_tp[d]/(precision_loose_tp[d]+precision_loose_fp[d])
        rec_loose[d] = 0.0 if recall_loose_tp[d]+recall_loose_fn[d] == 0 else recall_loose_tp[d]/(recall_loose_tp[d]+recall_loose_fn[d])
        f1_loose[d] = 0.0 if prec_loose[d]+rec_loose[d] == 0.0 else 2 * (prec_loose[d] * rec_loose[d]) / (prec_loose[d] + rec_loose[d])

    dialects = sorted(corIntents.keys())
    print('class:                   ', '       '.join([d for d in dialects]))
    print()
    print('slot recall:             ', '  '.join([f'{rec[d]:.4f}' for d in dialects]))
    print('slot precision:          ', '  '.join([f'{prec[d]:.4f}' for d in dialects]))
    print('slot f1:                 ', '  '.join([f'{f1[d]:.4f}' for d in dialects]))
    print()
    print('intent accuracy:         ', '  '.join(['{:.4f}'.format(corIntents[d]/slotCounts[d]) for d in dialects]))
    print('fully correct:           ', '  '.join(['{:.4f}'.format(fullyCor[d]/slotCounts[d]) for d in dialects]))
    print()
    print('unlabeled slot recall:   ', '  '.join([f'{rec_ul[d]:.4f}' for d in dialects]))
    print('unlabeled slot precision:', '  '.join([f'{prec_ul[d]:.4f}' for d in dialects]))
    print('unlabeled slot f1:       ', '  '.join([f'{f1_ul[d]:.4f}' for d in dialects]))
    print()
    # loose = partial overlap with same label
    print('loose slot recall:       ', '  '.join([f'{rec_loose[d]:.4f}' for d in dialects]))
    print('loose slot precision:    ', '  '.join([f'{prec_loose[d]:.4f}' for d in dialects]))
    print('loose slot f1:           ', '  '.join([f'{f1_loose[d]:.4f}' for d in dialects]))
    print()
