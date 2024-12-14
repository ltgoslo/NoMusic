import myutils
import pprint
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('rob.mplstyle')
import sys


dialects = False
results = {}
teamname = ''
run_path = ''
for line in open('../participants/detailed_results.txt'):
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

 
all_scores = []
team_names = []
for teamname in results:
    submissions = results[teamname]['slot']['f1:']['all']
    # remove "extra" submissions from LTG
    submissions = {x: submissions[x] for x in submissions if "mas" not in x}
    best_submission = sorted(submissions.items(), key=lambda item: item[1])[-1][0]
    
    teamscores = []
    for metric in ['f1:', 'precision:', 'recall:', 'unlabeled-f1:', 'loose-f1:']:
        teamscores.append(results[teamname]['slot'][metric]['all'][best_submission])
    if set(teamscores) == {0.0}:
        continue

    all_scores.append(teamscores)
    if teamname == "HITZ":
        team_names.append("HiTZ 1")
    elif teamname == "MaiNLP":
        team_names.append("MaiNLP 2")
    elif teamname == "LTG":
        team_names.append("LTG 3")
    else:
        team_names.append(teamname)

ax, fig = myutils.makeGraph(all_scores, team_names, ['F1', 'Precision', 'Recall', 'Unlabeled-F1', 'Loose-F1'], loc='lower right')
#ax.set_ylabel('Metric performance')
fig.savefig('slots-analysis.pdf', bbox_inches='tight')

def read_gold(path, task):
    labels = []
    for line in open(path):
        if line.startswith('# ' + task + ' ='):
            labels.append(line[11:].strip())
        if line.startswith('# ' + task + ': '):
            labels.append(line[10:].strip())
    return labels


for task, metric in zip(['intent', 'dialect'], ['accuracy:', 'f1-score']):
    print(task)
    print('Most common errors per team (gold-pred)')
    gold_labels = read_gold('../norsid_test.conll', task)
    all_labels = list(sorted(set(gold_labels)))
    err_counts = [0] * len(gold_labels)
    dialect_teams = []

    if task == 'dialect':
        plt.rcParams["axes.grid"] = False
        figs, axs = plt.subplots(1, 4, figsize=(8,5), dpi=300)
    for teamname in results:
        if teamname == 'Baseline' and task == 'intent':
            continue
        if task not in results[teamname]:
            continue
        errors = {}
        print(teamname)
        scores = [[0] * len(all_labels) for _ in range(len(all_labels))]
        submissions = results[teamname][task][metric]['all']
        best_submission = sorted(submissions.items(), key=lambda item: item[1])[-1][0]
        team_labels = read_gold('../participants/' + best_submission, task)
        idx = 0
        for gold, pred in zip(gold_labels, team_labels):
            if pred in all_labels:
                scores[all_labels.index(gold)][all_labels.index(pred)] += 1
                if gold != pred:
                    error = gold.split('/')[-1] + '-' + pred.split('/')[-1]
                    if error not in errors:
                        errors[error] = 0
                    errors[error] += 1
                    err_counts[idx] += 1
            idx += 1

        for item in sorted(errors.items(), key=lambda item: item[1], reverse=True)[:3]:
            print(item)
        if task == 'dialect':
            ax = axs[len(dialect_teams)]

            if teamname == "HITZ":
                teamname = "HiTZ 2"
            elif teamname == "CUFE":
                teamname = "CUFE 1"

            dialect_teams.append(teamname)
            print(scores)
            ax.set_title(teamname)
            im = ax.imshow(scores, vmin=0, vmax=1000)
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                rotation_mode="anchor")
            plt.setp(ax.get_yticklabels(), rotation=45, ha="right",
                rotation_mode="anchor")
    
            ax.set_xticks(range(4))
            ax.set_yticks(range(4))
            ax.set_xticklabels(all_labels)
            ax.set_yticklabels(all_labels)

            for i in range(len(scores)):
                for j in range(len(scores[i])):
                    if scores[i][j] < 1000:
                        text = ax.text(j, i, str(scores[i][j]),
                            ha="center", va="center", fontsize=7, color='white')
                    else:
                        text = ax.text(j, i, str(scores[i][j]),
                            ha="center", va="center", fontsize=7, color='black')


            #pprint.pprint(scores)
        print()
    #print(err_counts.count(0))
    #print(err_counts.count(1))
    #print(err_counts.count(2))
    #print(err_counts.count(3))
    #print(err_counts.count(4))


    if task == 'intent':
        print('Instances classified wrong by every team')
        sent_idx = 0
        test_lines = open('../norsid_test.conll').readlines()
        for line_idx, line in enumerate(test_lines):
            if line.startswith('# text = '):
                if err_counts[sent_idx] == 4:
                    print(line.strip())
                    print(test_lines[line_idx+1].strip())
                    print()
                sent_idx += 1

    if task == 'dialect':
        figs.colorbar(im, ax=axs[-1], aspect=5)
        axs[-1].remove()
        figs.tight_layout(pad=1.9)

        # Somehow it breaks with pdf
        figs.savefig('dialect-confusions.png', bbox_inches='tight')


