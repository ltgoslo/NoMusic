

dialects = False
results = {}
teamname = ''
run_path = ''
for line in open('participants/detailed_results.txt'):
    if line.startswith('---------------'):
        dialects = True
        continue

    if line[0].isupper():
        teamname = line.strip().split()[0]
        continue

    tok = line.strip().split()
    if len(tok) == 0:
        continue
    if '/' in tok[0]:
        run_path = tok[0]
        continue
    if tok[0] == 'class:':
        continue
    if tok[0] == 'B':
        continue
    
    if not dialects:
        if len(tok) == 8:
            tok = [tok[1], tok[0] + '-' + tok[2]] + tok[3:] 
        task = tok[0]
        metric = tok[1]
        scores = tok[2:]
    else:
        if len(tok) == 2:
            continue
        task = 'dialect'
        metric = tok[0]
        scores = tok[1:5] + [tok[-1]]
        print(scores)

    if teamname not in results:
        results[teamname] = {}
    if task not in results[teamname]:
        results[teamname][task] = {}
    if metric not in results[teamname][task]:
        results[teamname][task][metric] = {}

    for setting_idx, setting in enumerate(['B', 'N', 'T', 'V', 'all']):
        if setting not in results[teamname][task][metric]:
            results[teamname][task][metric][setting] = {}
        results[teamname][task][metric][setting][run_path] = float(scores[setting_idx])
        
print( 'Team & Slots (f1) & Intents (acc.) & Dialect (w-f1) \\\\')
for teamname in results:
    row = []
    for task, metric in zip(['slot', 'intent', 'dialect'], ['f1:', 'accuracy:', 'f1-score']):
        if task in results[teamname]:
            scores = results[teamname][task][metric]['all']
        else:
            scores = {'':0.0}
        row.append(max(scores.values()))
    print(' & '.join ([teamname] + ['{:.2f}'.format(100*x) for x in row]) + ' \\\\')
print()

for task, metric in zip(['slot', 'intent', 'dialect'], ['f1:', 'accuracy:', 'f1-score']):
    print(task)
    data = []
    for teamname in results:
        if task in results[teamname]:
            for path in results[teamname][task][metric]['all']:
                submission_name = teamname + '-' + path.split('/')[-1].replace('mainlp_', '').replace('_', '\\_').replace('.conll', '')
                scores = [results[teamname][task][metric][setting][path] for setting in ['B', 'N', 'T', 'V', 'all']]
                data.append([submission_name] + scores)

                #print(' & '.join ([submission_name] + ['{:.2f}'.format(100*x) for x in scores]) + ' \\\\')

    print(' & '.join(['Submission', 'B', 'N', 'T', 'V', 'all']) + ' \\\\')
    for row in sorted(data,key=lambda x: x[-1], reverse=True):
        print(' & '.join ([row[0]] + ['{:.2f}'.format(100*x) for x in row[1:]]) + ' \\\\')
    print()

    
