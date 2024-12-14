import matplotlib.pyplot as plt
plt.style.use('rob.mplstyle')


def makeGraph(data, names1, names2, transpose=False, loc=None):
    if transpose == True:
        tmp = names2
        names2 = names1
        names1 = tmp
        # transpose
        data = list(zip(*data))
    fig, ax = plt.subplots(figsize=(8,5), dpi=300)
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    colors = colors[1:] + colors + colors
    dim1 = len(data)
    dim2 = len(data[0])
    bar_width = 1/(dim2+1)
    for dim1_idx in range(dim1):
        for dim2_idx in range(dim2):
            x = dim1_idx + bar_width * dim2_idx + bar_width
            y = data[dim1_idx][dim2_idx]
            print(">>>", "x", x, "y", y, "dim1", dim1_idx, "dim2", dim2_idx)
            if dim1_idx == 0:
                ax.bar(x, y, bar_width, color = colors[dim2_idx], label = names2[dim2_idx])
                #plt.text(x, y, y, ha='center')
            else:
                ax.bar(x, y, bar_width, color = colors[dim2_idx])
                #plt.text(x, y, y, ha='center')
    for container in ax.containers:
        ax.bar_label(container, label_type='center', rotation=90)#, color='white')

    ax.set_xticks([x+.5 for x in range(dim1)])
    ax.set_xticklabels([name.replace('.40M', '') for name in names1], rotation=45, ha="right", rotation_mode="anchor")

    ax.set_xlim((0,dim1))
    #ax.set_ylim((0,.7))

    if loc != None:
        leg = ax.legend(loc=loc, ncol=2)
    else:
        leg = ax.legend(ncol=2)
    leg.get_frame().set_linewidth(1.5)
    return ax, fig

