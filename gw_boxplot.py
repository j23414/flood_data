# coding: utf-8

from db_scripts.get_server_data import get_table_for_variable
from matplotlib import rcParams
import matplotlib.pyplot as plt

fig_dir = '../Manuscript/pres/11.18.mtg/'
gwdf = get_table_for_variable(6)
gwdf.Value.plot.box()
ax = gwdf.Value.plot.box()
ax.set_xticklabels([''])
rcParams.update({'font.size': 15})
fig = plt.gcf()
fig.set_size_inches([4, 6.])
plt.figtext(
    0.04,
    0.5,
    'Shallow Well Depth [ft]',
    fontsize=15,
    rotation=90,
    ha='center',
    va='center')
fig.tight_layout()
plt.savefig('{}boxplot_shallow_well.png'.format(fig_dir), dpi=300)
