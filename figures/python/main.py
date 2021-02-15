from compare import plot_compare, plot_compare2
from style import latex_style,  legend_style
from plot import plot_sequential, comp_thresholds, threscompplot
from fitread import read_data
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

src = "~/documents/mep/tqe_paper_ufbb/figures/data/"
out = "~/documents/mep/tqe_paper_ufbb/figures/python/"
alpha=1
lw=1
pad = 0.02
LS = dict(UFPG="-", MWPM="dashdot", DBUF="--")
LS2 = dict(UFPG="-", MWPM="dashdot", bvUF="--")
markers = dict(UFPG=None, MWPM=None, bvUF=None)
def get_csvdir(names):
    return [src + "{}.csv".format(n) for n in names]

linestyles = {
    "MWPM": "dashdot",
    "fUF":  "--",
    "vUF":  "--",
    "bfUF": "--",
    "bvUF": "--",
    "UFPG": "-"
}

colors = {
    "MWPM": "C3",
    "fUF":  "C1",
    "vUF":  "C4",
    "bfUF": "C9",
    "bvUF": "C0",
    "UFPG": "C2"
}
#%%



latex_style(1.15,0.45)

f0, (ax0a, ax1) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [1, 2]}, sharey = True, tight_layout = True)

ax0b = plt.axes([0.11, 0.2, .2, .3])
ax0b.axes.xaxis.set_visible(False)
ax0b.axes.yaxis.set_visible(False)
plt.tight_layout()
th, colors1, = plot_sequential(src + "ufbb_toric_2d.csv", ax0a, ax0b,probs=[round(0.099 + i*0.0005, 4) for i in range(11)])

dataset = {
    "MWPM": read_data(src + "mwpm_toric_2d.csv"),
    "bvUF": read_data(src + "dbuf_toric_2d.csv")
}
comp_thresholds(dataset, ax1, [8+8*i for i in range(8)], colors1, linestyles, th, ylabel="")

leg1 = [Line2D([0], [0], lw=lw, ls="-", color=color, label=name) for name, color in colors1.items()]
leg2 = [Line2D([0], [0], lw=lw, ls=style, color="k", label=name) for name, style in LS2.items()]
plt.sca(ax1)
ax1.add_artist(plt.legend(handles=leg1, loc="lower left", ncol=3, **
    legend_style(handletextpad=0.2, handlelength=1, columnspacing=0.5), title=r"$L$", title_fontsize=8))
ax1.add_artist(plt.legend(handles=leg2, loc="upper right"))

ax0a.text(10.32, 81, r"\emph{(a)}")
ax0b.text(0.1017, 0.78, r"\emph{(b)}")
ax1.text(9.83, 81, r"\emph{(c)}")

"""
"""

D2 = [
    src + "delfosse_2d_uf.csv",
    src + "delfosse_2d_dbuf.csv",
    src + "delfosse_2d_ufbb.csv",
    src + "delfosse_2d_mwpm.csv",
]

D3 = [
    src + "delfosse_3d_uf.csv",
    src + "delfosse_3d_dbuf.csv",
    src + "delfosse_3d_ufbb.csv",
    src + "delfosse_3d_mwpm.csv",
]
ufstyle = (0, (3, 1, 1, 1, 1))
latex_style(1.15, 0.5)

(f4, axes4) = plt.subplots(2, 4, sharey="row", tight_layout=True, gridspec_kw={'wspace': 0.1, 'hspace': 0.5})

threscompplot(D2[0], "UF", ax=axes4[0][0])
threscompplot(D2[1], "bvUF",       ax=axes4[0][1])
threscompplot(D2[2], "UFPG",       ax=axes4[0][2])
threscompplot(D2[3], "MWPM",       ax=axes4[0][3], yb=1, leg=1, legloc="lower left")
threscompplot(D3[0], "", starti=6, ax=axes4[1][0])
threscompplot(D3[1], "", starti=6, ax=axes4[1][1])
threscompplot(D3[2], "", starti=6, ax=axes4[1][2])
threscompplot(D3[3], "", starti=6, ax=axes4[1][3], yb=1, leg=1, legloc="lower left")

axes4[0][0].set_ylabel(r"$d (\%)$")
axes4[0][3].set_ylabel("Independent\nnoise")
axes4[0][3].yaxis.set_label_coords(1.4, 0.5)
axes4[1][0].set_ylabel(r"$d (\%)$")
axes4[1][3].set_ylabel("Phenomenological\nnoise")
axes4[1][3].yaxis.set_label_coords(1.4, 0.5)


'''
Compare matching weight
'''
keys = ["MWPM", "fUF", "bfUF", "vUF", "bvUF", "UFPG"]
files = ["mwpm_toric_2d", "suf_toric_2d", "sbuf_toric_2d", 
        "duf_toric_2d", "dbuf_toric_2d", "ufbb_toric_2d"]
markers = {key: None for key in keys}

latex_style(scale=0.55, y=0.8)
f5, ax5 = plt.subplots(tight_layout=True)
l = [8+i*8 for i in range(8)]
names = get_csvdir(files)
latex_style(scale=0.55, y=0.9)
plot_compare2(keys, names, "l", [0.098], l, "weight", dim=2, yname=r"$ |\mathcal{C}|/ \min{|\mathcal{C}|} $", normy=0.1, markers=markers, colors=colors, linestyles=linestyles, show_normline=0)
legends = [c for c in ax5.get_children() if isinstance(c, mpl.legend.Legend)]
# shift = max([t.get_window_extent().width for t in legends[0].get_texts()])
# shift = input("old shift is {}, new shift: ".format(shift))
# for t in legends[0].get_texts():
#     t.set_ha('right') # ha is alias for horizontalalignment
#     t.set_position((shift,0))

# plt.show()

#%%



'''
Compare computation time
'''


latex_style(scale=0.55, y=0.6)
f6, ax6 = plt.subplots(tight_layout=True)
l = [8+i*8 for i in range(8)]
keys = ["UFPG", "MWPM", "bvUF"]
names = get_csvdir(["ufbb_toric_2d", "mwpm_toric_2d", "dbuf_toric_2d"])
plot_compare(keys,
             names, "l", [0.1], l, "time", dim=2, yname="Mean time (s)", normy=0.1, show_legend=False, colors=colors, linestyles=linestyles, markers=markers)
leg = [Line2D([0], [0], ls=linestyles[key], color=colors[key], label=key, lw=lw) for key in keys]
plt.legend(handles=leg, loc="upper left")


'''
lowerror time
'''
latex_style(scale=0.55, y=1)
f8, axes = plt.subplots(3, 1, tight_layout=True, sharex=True, gridspec_kw={'wspace': 0, 'hspace': 0.1})

keys = ["UFPG", "MWPM", "bvUF"]
names = get_csvdir(["ufns_lowerror", "mwpm_lowerror", "dbuf_lowerror"])

prange = [0.005, 0.012, 0.02]
xnames = ["", "", "L"]
for ax, p, x in zip(axes, prange, xnames):
    plt.sca(ax)
    plot_compare(keys,
                names, "l", [p], [6, 10, 14, 18], "time", dim=3, yname="", xname=x, show_legend=False, colors=colors, linestyles=linestyles, markers=markers)
    ax.annotate(r"$p_X$={:.1f}\%".format(p*100), xy=(0.5, 0.9), xycoords='axes fraction',
                horizontalalignment='center', verticalalignment='top')
axes[1].set_ylabel("Mean time (s)")
leg = [Line2D([0], [0], ls=linestyles[key], color=colors[key], label=key, lw=lw) for key in keys]
axes[2].legend(handles=leg, loc="upper left")
plt.tight_layout()

'''
lowerror decoding rate
'''
latex_style(scale=0.55, y=0.6)
f7, ax7 = plt.subplots(tight_layout=True)

dataset = {
    "UFPG": read_data(src + "ufns_lowerror.csv"),
    "MWPM": read_data(src + "mwpm_lowerror.csv"),
    "bvUF": read_data(src + "dbuf_lowerror.csv")
}
colors = {6:"C6", 10: "C7", 14:"C8", 18: "C9"}
comp_thresholds(dataset, ax7, [6, 10, 14, 18], colors, linestyles) #, 'AUF'])
leg1 = [Line2D([0], [0], ls=linestyles[key], color="k", label=key, lw=lw) for key in dataset]
leg2 = [Line2D([0], [0], ls="-", color=c, label=key, lw=lw) for key, c in colors.items()]
ax7.add_artist(plt.legend(handles=leg1, loc="lower center", columnspacing=0.2, handletextpad=0.2, handlelength=2))
ax7.add_artist(plt.legend(handles=leg2, loc="lower left", columnspacing=0.2, handletextpad=0.5, handlelength=2, title="L", title_fontsize=8))

# plt.show()


#%%
f0.savefig("threshold_ufpg.pdf", bbox_inches='tight', pad_inches=pad)
f4.savefig("threshold_comparison.pdf", bbox_inches='tight', pad_inches=pad)
f5.savefig("comp_matching_weight.pdf", bbox_inches='tight', pad_inches=pad)
f6.savefig("comp_time.pdf", bbox_inches='tight', pad_inches=pad)
f7.savefig("comp_lowerror.pdf", bbox_inches='tight', pad_inches=pad)
f8.savefig("comp_lowerror_time.pdf", bbox_inches='tight', pad_inches=pad)
