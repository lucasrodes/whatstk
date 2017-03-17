import seaborn as sns

# Visualize Response Matrix
def vis_response_matrix(response_matrix, ptype='absolute', title_size=20, xlabel_size=12, ylabel_size=12, tick_size=8, anot_size=8):

    title = 'Response Matrix: '
    fmt = '.2f'#'.1g'
    if(ptype == 'absolute'):
        title += 'Number of responses'
        #fmt = 'g'
    elif(ptype == 'joint'):
        title += 'P(replied, replier)'
        #fmt = '.1g'
    elif(ptype == 'conditional_replier'):
        title += 'P(replied | replier)'
    elif(ptype == 'conditional_replied'):
        title += 'P(replier | replied)'

    ax = sns.heatmap(response_matrix, annot=True, fmt=fmt, annot_kws={"size":anot_size})
    labels = [m.replace(' ', '\n')  if len(m.split(' '))>1 else m for m in response_matrix.columns]

    ax.axes.set_title(title,fontsize=title_size)
    ax.set_xlabel("Replied",fontsize=xlabel_size)
    ax.set_ylabel("Replier",fontsize=ylabel_size)
    ax.tick_params(labelsize=tick_size)

    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels[::-1])
    sns.plt.yticks(rotation=0)

    sns.plt.show()