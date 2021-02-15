from fitread import read_data
from style import get_colors, get_markers2, get_linestyles, plot_style
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy import optimize
import numpy as np


lw=1

def plot_compare(
    names,
    csv_names, 
    xaxis, 
    probs, 
    latts, 
    feature, 
    plot_error=False, 
    dim=1,
    xm=1, 
    ms=5,
    normy=None,
    xname=None,
    yname="",
    output="", 
    fitname="",
    folder="/home/watermarkhu/mep/mep-thesis/pgfplots/",
    show_legend=True,
    markers=None,
    colors=None,
    linestyles=None,
    gridcolor="k",
    **kwargs
    ):

    if fitname == "":
        fit = None
    else:
        if fitname in globals():
            fit = globals()[fitname]()
        else:
            print("fit does not exist")
            fit = None

    if not markers:
        markers = get_markers2()
    if not colors:
        colors = get_colors()
    if not linestyles:
        linestyles = get_linestyles()

    xchoice = dict(p="p", P="p", l="L", L="L")
    ychoice = dict(p="L", P="L", l="p", L="p")
    xchoice, ychoice = xchoice[xaxis], ychoice[xaxis]
    xlabels, ylabels = (probs, latts) if xaxis == "p" else (latts, probs)
    if xlabels:
        xlabels = sorted(xlabels)
    if xname is None:
        xname = xchoice


    data, leg1, leg2 = [], [], []
    for i, (name, x) in enumerate(zip(csv_names, names)):
        ls = linestyles[x]
        leg1.append(Line2D([0], [0], ls=ls,  color=colors[x], label=x, lw=lw))
        data.append(read_data(name))

    if not ylabels:
        ylabels = set()
        for df in data:
            for item in df.index.get_level_values(ychoice):
                ylabels.add(round(item, 6))
        ylabels = sorted(list(ylabels))

    xset = set()

    for i, (df,name) in enumerate(zip(data,names)):

        indices = [round(x, 6) for x in df.index.get_level_values(ychoice)]
        ls = linestyles[name]

        for j, ylabel in enumerate(ylabels):

            marker = markers[name]
            # color = colors[ylabel]
            color = colors[name]

            if name == "MWPM" and normy is not None:
                ylabel = normy

            d = df.loc[[x == ylabel for x in indices]]
            index = [round(v, 6) for v in d.index.get_level_values(xchoice)]
            d = d.reset_index(drop=True)
            d["index"] = index
            d = d.set_index("index")

            if not xlabels:
                X = index
                xset = xset.union(set(X))
            else:
                X = [x for x in xlabels if x in d.index.values]

            column = feature if feature in df else f"{feature}_m"
            Y = [d.loc[x, column] for x in X]

            if dim != 1:
                X = [x**dim for x in X]

            # print(ylabel, X, Y)
            #
            if fit is not None:
                guess, min, max = fit.guesses()
                res = optimize.curve_fit(
                    fit.func, X, Y, guess, bounds=[min, max])
                step = abs(int((X[-1] - X[0])/100))
                pn = np.array(range(X[0], X[-1] + step, step))
                ft = fit.func(pn, *res[0])
                plt.plot(pn, ft, ls=ls, c=color, lw=lw)
                plt.plot(X, Y, lw=0, c=color, marker=marker,
                         ms=ms, fillstyle="none")
                print(f"{ychoice} = {ylabel}", fit.show(*res[0]))
            else:
                plt.plot(X, Y, ls=ls, c=color, marker=marker,
                         ms=ms, fillstyle="none", lw=lw)

            if i == 0:
                leg2.append(Line2D([0], [0], ls=ls, c=color, marker=marker, lw=lw,
                                   ms=ms, fillstyle="none", label=f"{ychoice}={ylabel}"))

            if plot_error and f"{feature}_v" in d:
                E = list(d.loc[:, f"{feature}_v"])
                ym = [y - e for y, e in zip(Y, E)]
                yp = [y + e for y, e in zip(Y, E)]
                plt.fill_between(X, ym, yp, alpha=0.1,
                                 facecolor=color, edgecolor=color, ls=ls, lw=2)

    xnames = sorted(list(xset)) if not xlabels else xlabels
    xticks = [x**dim for x in xnames]
    xnames = [round(x*xm, 3) for x in xnames]

    plt.xticks(xticks, xnames)

    if show_legend:
        L1 = plt.legend(handles=leg1, loc="upper left")
        plt.gca().add_artist(L1)
        if len(probs) > 1:
            L2 = plt.legend(handles=leg2, loc="upper left", ncol=3)
            plt.gca().add_artist(L2)

    plot_style(plt.gca(), "", xname, yname, gridcolor=gridcolor)
    # plt.title("Comparison of matching weight")
    plt.tight_layout()

    if output:
        plt.savefig(folder + "{}.pgf".format(output))


def plot_compare2(
    names,
    csv_names,
    xaxis,
    probs,
    latts,
    feature,
    plot_error=False,
    dim=1,
    xm=1,
    ms=5,
    normy=None,
    yname="",
    xname=None,
    output="",
    fitname="",
    folder="/home/watermarkhu/mep/mep-thesis/pgfplots/",
    show_legend=True,
    show_normline=True,
    markers=None,
    colors=None,
    linestyles=None,
    gridcolor="k",
    **kwargs
):

    if fitname == "":
        fit = None
    else:
        if fitname in globals():
            fit = globals()[fitname]()
        else:
            print("fit does not exist")
            fit = None

    if not markers:
        markers = get_markers2()
    if not colors:
        colors = get_colors()
    if not linestyles:
        linestyles = get_linestyles()


    xchoice = dict(p="p", P="p", l="L", L="L")
    ychoice = dict(p="L", P="L", l="p", L="p")
    xchoice, ychoice = xchoice[xaxis], ychoice[xaxis]
    xlabels, ylabels = (probs, latts) if xaxis == "p" else (latts, probs)
    if xlabels:
        xlabels = sorted(xlabels)
    if xname is None:
        xname = xchoice

    data, leg1, leg2 = [], [], []
    for i, (name, x) in enumerate(zip(csv_names, names)):
        data.append(read_data(name))
        if i != 0:
            ls = linestyles[x]
            leg1.append(Line2D([0], [0], ls=ls,  color=colors[x], label=x, lw=lw))

    if not ylabels:
        ylabels = set()
        for df in data:
            for item in df.index.get_level_values(ychoice):
                ylabels.add(round(item, 6))
        ylabels = sorted(list(ylabels))


    xset = set()
    for i, (df, name) in enumerate(zip(data, names)):

        indices = [round(x, 6) for x in df.index.get_level_values(ychoice)]
        ls = linestyles[name]

        print(i, name)

        for j, ylabel in enumerate(ylabels):

            marker = markers[name]
            # color = colors[ylabel]
            color = colors[name]

            if i == 0 and normy is not None:
                ylabel = normy

            d = df.loc[[x == ylabel for x in indices]]
            index = [round(v, 6) for v in d.index.get_level_values(xchoice)]
            d = d.reset_index(drop=True)
            d["index"] = index
            d = d.set_index("index")

            if not xlabels:
                X = index
                xset = xset.union(set(X))
            else:
                X = [x for x in xlabels if x in d.index.values]

            column = feature if feature in df else f"{feature}_m"
            Y = [d.loc[x, column] for x in X]

            if dim != 1:
                X = [x**dim for x in X]

            
            if i == 0:
                Ynorm = Y
                marker="None"
                if not show_normline:
                    continue

            Y = [y1/y2 for y1, y2 in zip(Y,Ynorm)]
            # print(ylabel, X, Y)
            #
            if fit is not None:
                guess, min, max = fit.guesses()
                res = optimize.curve_fit(
                    fit.func, X, Y, guess, bounds=[min, max])
                step = abs(int((X[-1] - X[0])/100))
                pn = np.array(range(X[0], X[-1] + step, step))
                ft = fit.func(pn, *res[0])
                plt.plot(pn, ft, ls=ls, c=color, lw=lw)
                plt.plot(X, Y, lw=0, c=color, marker=marker,
                         ms=ms, fillstyle="none")
                print(f"{ychoice} = {ylabel}", fit.show(*res[0]))
            else:
                plt.plot(X, Y, ls=ls, c=color, marker=marker, lw=lw,
                         ms=ms, fillstyle="none")

            if i == 0:
                leg2.append(Line2D([0], [0], ls=ls, c=color, marker=marker,
                                   ms=ms, fillstyle="none", label=f"{ychoice}={ylabel}", lw=lw))

            if plot_error and f"{feature}_v" in d:
                E = list(d.loc[:, f"{feature}_v"])
                ym = [y - e for y, e in zip(Y, E)]
                yp = [y + e for y, e in zip(Y, E)]
                plt.fill_between(X, ym, yp, alpha=0.1,
                                 facecolor=color, edgecolor=color, ls=ls, lw=2)

    xnames = sorted(list(xset)) if not xlabels else xlabels
    xticks = [x**dim for x in xnames]
    xnames = [round(x*xm, 3) for x in xnames]

    plt.xticks(xticks, xnames)
    if show_legend:
        L1 = plt.legend(handles=leg1, loc="center right", bbox_to_anchor=(1, 0.4))
        plt.gca().add_artist(L1)
        if len(probs) > 1:
            L2 = plt.legend(handles=leg2, ncol=3)
            plt.gca().add_artist(L2)

    plot_style(plt.gca(), "", xchoice, yname, gridcolor=gridcolor)
    # plt.title("Comparison of matching weight, normalized to MWPM")
    plt.tight_layout()
    if output:
        plt.savefig(folder + "{}.pgf".format(output))
