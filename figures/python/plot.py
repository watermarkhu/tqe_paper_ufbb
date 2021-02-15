#%%
from style import plot_style, get_markers
from fitread import read_data, fit_thresholds, get_fit_func
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from collections import defaultdict
import numpy as np

alpha=1
lw=1


def plot_sequential(
    file_name,
    ax0,
    ax1,
    latts=[],
    probs=[],
    lattices=None,
    ms=4,
    style="-",           # linestyles for data and fit
    plotn=1000,                  # number of points on x axis
    ylabel=True,
):

    fit_func = get_fit_func(False)
    data = read_data(file_name)

    if not latts:
        latts = sorted(list(set(data.index.get_level_values("L"))))
    '''
    apply fit and get parameter
    '''
    parlist = []
    for i in range(len(latts)-1):
        (fitL, fitp, fitN, fitt), par = fit_thresholds(
            data, False, latts[i:i+2], probs)
        parlist.append(par)
    print("\nFinal:")
    (fitL, fitp, fitN, fitt), par = fit_thresholds(
        data, False, latts, probs)

    '''
    Plot and fit thresholds for a given dataset. Data is inputted as four lists for L, P, N and t.
    '''

    LP = defaultdict(list)
    for L, P, N, T in zip(fitL, fitp, fitN, fitt):
        LP[L].append([P, N, T])

    if lattices is None:
        lattices = sorted(set(fitL))

    cmap = plt.get_cmap('tab20')
    colors = {lati: cmap(i) for i, lati in zip(np.linspace(0, 1, len(lattices)), lattices)}

    markerlist = get_markers()
    markers = {lati: markerlist[i % len(markerlist)]
               for i, lati in enumerate(lattices)}


    for i, lati in enumerate(lattices):
        fp, fN, fs = map(list, zip(*sorted(LP[lati], key=lambda k: k[0])))
        ft = [si / ni for si, ni in zip(fs, fN)]
        ax0.plot(
            [q*100 for q in fp], [y*100 for y in ft],
            color=colors[lati],
            ls="-",
            lw=lw,
            alpha=alpha,
            label="{}".format(lati),
        )

    DS = fit_func((par[0], 20), *par)
    print("DS = {}".format(DS))

    var = 0.0004
    for par, lati, laty in zip(parlist, latts[:-1], latts[1:]):

        X = np.linspace(par[0] - var, par[0] + var, plotn)
        ax1.plot(
            [x for x in X],
            [fit_func((x, lati), *par) for x in X],
            "-",
            lw=lw,
            color=colors[lati],
            alpha=alpha,
            ls=style,
        )
        ax1.plot(
            [x for x in X],
            [fit_func((x, laty), *par) for x in X],
            "-",
            lw=lw,
            color=colors[laty],
            alpha=alpha,
            ls=style,
        )

    thresholds = []
    for par, lati, laty in zip(parlist, latts[:-1], latts[1:]):
        pth = par[0]
        kc = fit_func((pth, 20), *par)
        thresholds.append([pth, kc, colors[lati], markers[laty]])
        ax1.plot(pth, kc, color=colors[lati], lw=lw,
                 marker=markers[laty], ms=ms, fillstyle="none")

    if ylabel:
        plot_style(ax0, "", r" $ p_X $", r"$d (\%)$")
    else:
        plot_style(ax0, "", r" $ p_X $")

    return thresholds, colors


def comp_thresholds(dataset, ax, lattices, colors, linestyles, thdata=[], ylabel=None):

    legend_elements = []


    for decoder, data in dataset.items():

        (fitL, fitp, fitN, fitt), par = fit_thresholds(
            data, False, latts=lattices)

        LP = defaultdict(list)
        for L, P, N, T in zip(fitL, fitp, fitN, fitt):
            LP[L].append([P, N, T])

        if lattices is None:
            lattices = sorted(set(fitL))

        for i, lati in enumerate(lattices):
            fp, fN, fs = map(list, zip(*sorted(LP[lati], key=lambda k: k[0])))
            ft = [si / ni for si, ni in zip(fs, fN)]
            ax.plot(
                [q*100 for q in fp], [y*100 for y in ft],
                color=colors[lati],
                ls=linestyles[decoder],
                lw=lw,
                alpha=alpha,
                label="{}".format(lati),
            )
    for i, (x, y, color, marker) in enumerate(thdata):
        ax.plot(x*100, y*100, "*", ms=5, color=color, marker=marker, lw=lw, fillstyle="none")

    if ylabel is None:
        ylabel = r"$d (\%)$"

    plot_style(ax, "", r" $ p_X (\%)$", ylabel)


def threscompplot(
    file_name,
    title="",
    latts=[],
    probs=[],
    modified_ansatz=False,
    ax=None,                   # axis object of error fit plot
    lw=1,
    style="-",           # linestyles for data and fit
    leg=False,
    legendname="",
    legloc="lower left",
    yb=False,
    starti=0,
    **kwargs
):

    data = read_data(file_name)
    '''
    apply fit and get parameter
    '''
    (fitL, fitp, fitN, fitt), par = fit_thresholds(
        data, modified_ansatz, latts, probs)

    fit_func = get_fit_func(modified_ansatz)

    '''
    Plot and fit thresholds for a given dataset. Data is inputted as four lists for L, P, N and t.
    '''

    LP = defaultdict(list)
    for L, P, N, T in zip(fitL, fitp, fitN, fitt):
        LP[L].append([P, N, T])

    lattices = sorted(set(fitL))

    colors = {lati: f"C{(i+starti)%10}" for i, lati in enumerate(lattices)}
    legend = []

    for i, lati in enumerate(lattices):
        fp, fN, fs = map(list, zip(*sorted(LP[lati], key=lambda k: k[0])))
        ft = [si / ni for si, ni in zip(fs, fN)]
        ax.plot(
            [q*100 for q in fp], [y*100 for y in ft],
            color=colors[lati],
            ls=style,
            lw=lw,
        )
        legend.append(Line2D(
            [0],
            [0],
            label="{}".format(lati),
            color=colors[lati],
            lw=lw,
        ))

    DS = fit_func((par[0], 20), *par)
    print("DS = {}".format(DS))


    if yb:
        plot_style(ax, title, r"$p_X (\%)$", r"Decoding rate $d$", **kwargs)
    else:
        plot_style(ax, title, r"$p_X (\%)$", "", **kwargs)

    if leg:
        legend = ax.legend(handles=legend, loc=legloc, ncol=2,
                           markerscale=1, fontsize="small", columnspacing=0.2, labelspacing=0.2, handletextpad=0.2, handlelength=0.5, numpoints=1, title=r"{}$L$".format(legendname), title_fontsize=8)
    return ax

