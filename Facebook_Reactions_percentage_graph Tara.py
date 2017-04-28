# coding: utf-8
get_ipython().magic(u'pylab inline')
# Read data from CSV file

data = pd.read_csv("/Users/Tara/leaveEU.csv", parse_dates=[0], encoding = 'utf-8')
#data = pd.read_csv("/Users/Tara/uk.csv", parse_dates=[0], encoding = 'utf-8')
data


# Filter rows with no reactions at all
data = data[(data.T[2:] != 0).any()]
data.shape

# ### Group data by weeks
data = data.groupby(data['status_published'].map(lambda x: str(x.year) + ' - ' + "%02i" % x.isocalendar()[1])).sum()

# ### Start at a specific calendar week
data = data[[week >= '2016 - 07' for week in data.index.tolist()]]
data.shape

# ### Make relative numbers
relative_data = OrderedDict()
relative_data['love'] = data['num_loves'] / data['num_reactions']
relative_data['wow'] = data['num_wows'] / data['num_reactions']
relative_data['haha'] = data['num_hahas'] / data['num_reactions']
relative_data['sad'] = data['num_sads'] / data['num_reactions']
relative_data['angry'] = data['num_angrys'] / data['num_reactions']
relative_data['like'] = data['num_likes'] / data['num_reactions']


# ### Plot stacked barchart

# set a colormap, names see here: http://matplotlib.org/examples/color/colormaps_reference.html
cmap = cm.Set3

figure(figsize=(20,10))
ind = arange(len(data))
prev = None
for i, (k, v) in enumerate(relative_data.items()):
    v *= 100
    bar(ind, v, label=k, bottom=prev, color=cmap(1.*i/len(relative_data)))
    if prev is None:
        prev = v
    else:
        prev += v
ylabel("Relative reactions %"), legend()
xticks(ind, data.index, rotation='vertical'), xlabel("Calendar week")
ax1 = plt.gca()
ax2 = ax1.twinx()
ind_smooth = linspace(0, len(ind), 500)
ax2.plot(ind_smooth, spline(ind, data['num_reactions'], ind_smooth))
ylabel("Total reactions")
tight_layout;
savefig("trend.pdf");


from IPython.core.display import display, HTML
display(HTML('<h1>Hello, world!</h1>'))

from weasyprint import HTML
HTML(string=html_out).write_pdf("report.pdf")