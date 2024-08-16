# Author: Firas Moosvi, Jake Bobowski, others
# Date: 2023-10-31

from __future__ import annotations

from typing import Any, Literal

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from scipy import stats


def shaded_normal_density(
    q: float | tuple[float, float],
    /,
    mean: float = 0,
    sd: float = 1,
    rsd: float = 4,
    lower_tail: bool = True,
    add_prob: bool = True,
    add_q: bool = True,
    add_legend: bool = False,
    figsize: tuple[float, float] | None = (8, 6),
    color: Any = "xkcd:sky blue",
    x_label: str = "x",
    y_label: str = "f(x; \u03BC,\u03C3)",
    legend_text: str | None = None,
    **kwargs,
) -> Figure:
    """Generate a normal distribution plot with optional listed probability calculation.

    Parameters
    ----------
    q : float or tuple[float, float]
        If a float, the upper or lower bound of the shaded area. If a tuple of floats, the lower and upper bounds of the shaded area.
    mean : float
        The mean of the normal distribution. Defaults to ``0``
    sd : float
        The standard deviation of the normal distribution. Defaults to ``1``
    rsd : float
        The number of standard deviations to plot on either side of the mean.  Defaults to ``4``
    lower_tail : bool
        Whether the shaded area should represent the lower tail probability :math:`\\operatorname{P}(X \\le x)`,
        or the upper tail probability :math:`\\operatorname{P}(X \\ge x)`. Defaults to ``True``
    add_prob : bool
        Whether to show the probability of the shaded area will be displayed on the plot. Defaults to ``True``
    add_q : bool
        Whether the value(s) of ``q`` should be displayed on the x-axis of the plot. Defaults to ``True``
    add_legend : bool
        Whether a legend with the mean and standard deviation values will be displayed on the plot. Defaults to ``False``
    figsize : tuple or tuple[float, float] or None
        The size of the plot in inches. If None, the default matplotlib figure size
        will be used as this is passed to :func:`matplotlib.pyplot.figure`. Defaults to ``(8, 6)``
    color : Any
        The color of the shaded area as a valid :doc:`matplotlib color <mpl:users/explain/colors/colors>`. Defaults to ``xkcd:sky blue``
    x_label : str
        The label for the x-axis. Defaults to ``x``
    y_label : str
        The label for the y-axis. Defaults to ``f(x; \u03BC,\u03C3)``
    legend_text : str or None, Optional
        The text to display in the legend if add_legend is set to true. By default (None), the legend will display the mean and standard deviation values.
    **kwargs
        Additional keyword arguments to pass to :func:`matplotlib.pyplot.figure`.

    Returns
    -------
    matplotlib.figure.Figure
        The generated matplotlib Figure object.

    Raises
    ------
    TypeError
        If the input parameters are not of the expected type.
    ValueError
        If the input values are out of the expected range.

    Examples
    --------

    Shading the region :math:`P(Z \\le z)` where :math:`Z\\sim N(0,1)` is the standard normal ``N(0,1)``
    
    .. plot::
        :context: reset

        pbh.stats.shaded_normal_density(-0.2533)

    Shading the region :math:`P(Z \\ge z)` where :math:`Z\\sim N(\u03BC,\u03C3)` is a normal distribution with mean \u03BC and standard deviation \u03C3.
    
    .. plot::
        :context: reset

        pbh.stats.shaded_normal_density(7.1, 7, 0.1, lower_tail=False, add_legend=True)
    
    Shading the region :math:`P(a \\le Z \\le b)` where :math:`Z\\sim N(0,1)` is the standard normal ``N(0,1)``
    
    .. plot::
        :context: reset

        pbh.stats.shaded_normal_density((-1.1, 2))

    References
    ----------
    Based off of an R function written by Dr. Irene Vrbick for making `shaded normal density curves <https://irene.vrbik.ok.ubc.ca/blog/2021-11-04-shading-under-the-normal-curve/>`__.

    The R function by Dr. Irene Vrbick was adapted from `here <http://rstudio-pubs-static.s3.amazonaws.com/78857_86c2403ca9c146ba8fcdcda79c3f4738.html>`__.
    """
    if not isinstance(mean, (float, int)):
        msg = f"mean must be a number, not a {mean.__class__.__name__!r}"
        raise TypeError(msg)
    if not isinstance(sd, (float, int)):
        msg = f"sd must be a number, not a {sd.__class__.__name__!r}"
        raise TypeError(msg)
    if not isinstance(rsd, (float, int)):
        msg = f"rsd must be a number, not a {rsd.__class__.__name__!r}"
        raise TypeError(msg)
    if (
        isinstance(q, tuple)
        and len(q) == 2
        and isinstance(q[0], (float, int))
        and isinstance(q[1], (float, int))
    ):
        q_lower, q_upper = sorted(q)
        xx = np.linspace(mean - rsd * sd, mean + rsd * sd, 200)
        yy = stats.norm.pdf(xx, mean, sd)
        fig = plt.figure(figsize=figsize, **kwargs)
        ax = fig.gca()
        ax.plot(xx, yy)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        x = np.linspace(q_lower, q_upper, 200)
        y = stats.norm.pdf(x, mean, sd)
        # fmt: off
        filled, *_ = ax.fill(  # Fill returns a list of polygons, but we're  only making one
            np.concatenate([[q_lower], x, [q_upper]]),
            np.concatenate([[0], y, [0]]),
            color,
        )
        # fmt: on
        if add_prob:
            height = max(y) / 4
            rv = stats.norm(mean, sd)
            prob: float = rv.cdf(q_upper) - rv.cdf(q_lower)
            ax.text((sum(q) / 2), height, f"{prob:.3f}", ha="center")
        if add_q:
            ax.set_xticks(
                [q_lower, q_upper],
                labels=[
                    str(round(q_lower, 4)),
                    str(round(q_upper, 4)),
                ],
                minor=True,
                color=color,
                y=-0.05,
            )
            if q_lower in ax.get_xticks():
                ax.get_xticklabels()[
                    np.where(ax.get_xticks() == q_lower)[0][0]
                ].set_color(color)
            if q_upper in ax.get_xticks():
                ax.get_xticklabels()[
                    np.where(ax.get_xticks() == q_upper)[0][0]
                ].set_color(color)

    elif isinstance(q, (float, int)):
        if not isinstance(lower_tail, bool):
            msg = f"lower_tail must be a bool, not a {lower_tail.__class__.__name__!r}"
            raise TypeError(msg)

        xx = np.linspace(mean - rsd * sd, mean + rsd * sd, 200)
        yy = stats.norm.pdf(xx, mean, sd)
        fig = plt.figure(figsize=figsize, **kwargs)
        ax = fig.gca()
        ax.plot(xx, yy)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        if lower_tail is True:
            x = np.linspace(xx[0], q, 100)
            y = stats.norm.pdf(x, mean, sd)
            # fmt: off
            filled, *_ = ax.fill(  # Fill returns a list of polygons, but we're  only making one
                np.concatenate([[xx[0]], x, [q]]),
                np.concatenate([[0], y, [0]]),
                color,
            )
            # fmt: on
            if add_prob:
                height: float = stats.norm.pdf(q, mean, sd) / 4  # type: ignore
                prob: float = stats.norm.cdf(q, mean, sd)  # type: ignore
                ax.text((q - 0.5 * sd), height, f"{prob:.3f}", ha="center")
        else:
            x = np.linspace(q, xx[-1], 100)
            y = stats.norm.pdf(x, mean, sd)
            # fmt: off
            filled, *_ = ax.fill(  # Fill returns a list of polygons, but we're  only making one
                np.concatenate([[q], x, [xx[-1]]]),
                np.concatenate([[0], y, [0]]),
                color,
            )
            # fmt: on
            if add_prob:
                height: float = stats.norm.pdf(q, mean, sd) / 4  # type: ignore
                prob: float = stats.norm.sf(q, mean, sd)  # type: ignore
                ax.text((q + 0.5 * sd), height, f"{prob:.3f}", ha="center")

        if add_q:
            if q in ax.get_xticks():
                ax.get_xticklabels()[np.where(ax.get_xticks() == q)[0][0]].set_color(
                    color
                )
            else:
                ax.set_xticks(
                    [q],
                    labels=[
                        str(round(q, 4)),
                    ],
                    minor=True,
                    color=color,
                    y=-0.05,
                )

    else:
        error_base = "q must be a tuple of two numbers, or a single number"
        if isinstance(q, tuple):
            if len(q) != 2:
                msg = f"{error_base}, not a {len(q)}-tuple"
                raise ValueError(msg)
            msg = f"{error_base}, not a 2-tuple containing a {q[0].__class__.__name__!r} and a {q[1].__class__.__name__!r}"
            raise TypeError(msg)
        else:
            msg = f"{error_base}, not a {q.__class__.__name__!r}"
            raise TypeError(msg)

    if add_legend:
        ax.set_title(legend_text or f"\u03BC = {mean}, \u03C3 = {sd}")

    return fig


def shaded_hypothesis_test(
    critical_value: float,
    tail: Literal["left", "right", "both"],
    /,
    mean: float = 0,
    sd: float = 1,
    rsd: float = 4,
    figsize: tuple[float, float] | None = (8, 6),
    color: Any = "xkcd:sky blue",
    x_label: str = "x",
    y_label: str = "Probability Density",
    legend: str | None = None,
    **kwargs
) -> Figure:
    """Generate a normal distribution plot with appropriate tails for a hypothesis test.

    Parameters
    ----------
    critical_value : float
        The critical value to plot. If ``tail`` is ``both``, :code:`-abs(critical_value)` is used for the left tail
        and :code:`abs(critical_value)` is used for the right tail.
    tail : ``left`` or ``right`` or ``both``
        The type of hypothesis test to plot.
    mean : float
        The mean of the normal distribution. Defaults to ``0``
    sd : float
        The standard deviation of the normal distribution. Defaults to ``1``
    rsd : float
        The number of standard deviations to plot on either side of the mean.  Defaults to ``4``
    figsize : tuple or tuple[float, float] or None
        The size of the plot in inches. If None, the default matplotlib figure size
        will be used as this is passed to :func:`matplotlib.pyplot.figure`. Defaults to ``(8, 6)``
    color : Any
        The color of the shaded area as a valid :doc:`matplotlib color <mpl:users/explain/colors/colors>`. Defaults to ``xkcd:sky blue``
    x_label : str
        The label for the x-axis. Defaults to ``x``
    y_label : str
        The label for the y-axis. Defaults to ``Probability Density``
    legend : str or None, Optional
        The text to display in the legend (title) of the plot.
    **kwargs
        Additional keyword arguments to pass to :func:`matplotlib.pyplot.figure`.

    Returns
    -------
    matplotlib.figure.Figure
        The generated matplotlib Figure object.

    Raises
    ------
    TypeError
        If the input parameters are not of the expected type.
    ValueError
        If the input values are out of the expected range.

    Examples
    --------

    Left-tailed hypothesis test with a critical value of ``-1.645`` for the standard normal ``N(0,1)``
    
    .. plot::
        :context: reset

        pbh.stats.shaded_hypothesis_test(-1.645, "left")

    Right-tailed hypothesis test with a critical value of ``1.645`` for the standard normal ``N(0,1)``
    
    .. plot::
        :context: reset

        pbh.stats.shaded_hypothesis_test(1.645, "right")
    
    Two-tailed hypothesis test with a critical value of ``±1.96`` for the standard normal ``N(0,1)``
    
    .. plot::
        :context: reset

        pbh.stats.shaded_hypothesis_test(1.96, "both")
    """
    if not isinstance(mean, (float, int)):
        msg = f"mean must be a number, not a {mean.__class__.__name__!r}!"
        raise TypeError(msg)
    if not isinstance(sd, (float, int)):
        msg = f"sd must be a number, not a {sd.__class__.__name__!r}!"
        raise TypeError(msg)
    if not isinstance(rsd, (float, int)):
        msg = f"rsd must be a number, not a {rsd.__class__.__name__!r}!"
        raise TypeError(msg)
    if not isinstance(critical_value, (float, int)):
        msg = f"critical_value must be a number, not a {critical_value.__class__.__name__!r}!"
        raise TypeError(msg)
    if tail not in {"left", "right", "both"}:
        msg = f"tail must be one of 'left', 'right', or 'both', not {tail!r}!"
        raise ValueError(msg)
    
    # Define the normal distribution
    plot_to = rsd * sd
    xx = np.linspace(mean - plot_to, mean + plot_to, 100)
    yy = stats.norm.pdf(xx, mean, sd)
    
    fig = plt.figure(figsize=figsize, **kwargs)
    ax = fig.gca()
    ax.plot(xx, yy)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    match tail:
        case "left":
            x = np.linspace(xx[0], critical_value, 100)
            y = stats.norm.pdf(x, mean, sd)
            # fmt: off
            ax.fill(
                np.concatenate([[xx[0]], x, [critical_value]]),
                np.concatenate([[0], y, [0]]),
                color,
            )
        case "right":
            x = np.linspace(critical_value, xx[-1], 100)
            y = stats.norm.pdf(x, mean, sd)
            # fmt: off
            ax.fill(
                np.concatenate([[critical_value], x, [xx[-1]]]),
                np.concatenate([[0], y, [0]]),
                color,
            )
        case "both":
            right_crit = abs(critical_value)
            left_crit = -right_crit
            left_x = np.linspace(xx[0], left_crit, 100)
            left_y = stats.norm.pdf(left_x, mean, sd)
            right_x = np.linspace(critical_value, xx[-1], 100)
            right_y = stats.norm.pdf(right_x, mean, sd)
            # fmt: off
            ax.fill(
                np.concatenate([[xx[0]], left_x, [left_crit]]),
                np.concatenate([[0], left_y, [0]]),
                color,
                np.concatenate([[right_crit], right_x, [xx[-1]]]),
                np.concatenate([[0], right_y, [0]]),
                color,
            )
        case other:
            msg = f"tail must be one of 'left', 'right', or 'both', not {other!r}!"
            raise ValueError(msg)
    
    if legend is not None:
        ax.set_title(legend)

    return fig

