""" The ``dyson_equalizer.plots`` module provides functions to create useful plots
"""

import numpy as np
from matplotlib import pyplot as plt

from dyson_equalizer.algorithm import marchenko_pastur


def plot_mp_eigenvalues(
        eigs: np.ndarray, gamma: float,
        eigenvalues_to_show: int = 100,
        log_y: bool = True,
        matrix_label: str = 'X',
        ax: plt.Axes | None = None,
) -> None:
    """Plots the eigenvalues of the covariance matrix and compares to the Marchenko-Pastur threshold

    This function assumes the input are the eigenvalues of a covariance matrix of a random matrix
    whose entries have variance 1. These eigenvalues follow the Marchenko-Pastur distribution.

    Parameters
    ----------
    eigs: (n) numpy.array
        The array of eigenvalues (e.g. of a covariance matrix) to plot
    gamma: float
        The ratio between the dimensions of the matrix (between 0 and 1)
    eigenvalues_to_show: int, optional
        The number of eigenvalues to show in the plot (defaults to 100)
    log_y: bool, optional
        Whether the y-axis should be logarithmic (defaults to True)
    matrix_label: str, optional
        The name of the matrix that will be used as label (defaults to ``X``)
    ax: plt.Axes, optional
        A matplotlib Axes object. If none is provided, a new figure is created.

    See Also
    --------

    dyson_equalizer.algorithm.marchenko_pastur

    Examples
    --------

    We generate a random matrix X of size (100, 1000) and show that the eigenvalues of
    the covariance matrix Y = ¹⁄ₙXXᵀ follow a Marchenko-Pastur distribution.


    .. plot::
        :context: close-figs
        :caption: Eigenvalues plot of a random matrix

        import numpy as np
        from dyson_equalizer.plots import plot_mp_eigenvalues

        m, n = 100, 1000
        X = np.random.normal(size=(m, n))
        Y = X @ X.T / n
        eigs = sorted(np.linalg.eigvals(Y), reverse=True)

        plot_mp_eigenvalues(eigs, gamma=m/n)
    """
    if ax is None:
        _, ax = plt.subplots()

    beta_p = (1 + gamma ** 0.5) ** 2
    nx = min(eigenvalues_to_show, len(eigs))
    ax.bar(x=range(nx), height=eigs[:nx], label=f'Eigenvalues of {matrix_label}')
    ax.axhline(y=beta_p, linestyle='--', color='green', label='MP upper edge β₊')
    if log_y:
        ax.set_yscale('log')
    ax.legend()


def plot_mp_density(
        eigs: np.ndarray,
        gamma: float,
        show_only_significant: int = None,
        matrix_label: str = 'X',
        ax: plt.Axes | None = None,
) -> None:
    """Plots the density of eigenvalues of the covariance matrix and compares to the Marchenko-Pastur distribution

    This function assumes the input are the eigenvalues of a covariance matrix of a random matrix
    whose entries have variance 1. These eigenvalues follow the Marchenko-Pastur distribution.

    Parameters
    ----------
    eigs: (n) numpy.array
        The array of eigenvalues (e.g. of a covariance matrix) to plot
    gamma: float
        The ratio between the dimensions of the matrix (between 0 and 1)
    show_only_significant: int, optional
        Set this value to show only a small number of significant eigenvalues (defaults to None)
        This option is useful is some of the signal eigenvalues are much bigger than the noise.
    matrix_label: str, optional
        The name of the matrix that will be used as label (defaults to ``X``)
    ax: plt.Axes, optional
        A matplotlib Axes object. If none is provided, a new figure is created.

    See Also
    --------

    dyson_equalizer.algorithm.marchenko_pastur


    Examples
    --------

    We generate a random matrix X of size (100, 1000) and show that the eigenvalues of
    the covariance matrix Y = ¹⁄ₙXXᵀ follow a Marchenko-Pastur distribution.


    .. plot::
        :context: close-figs
        :caption: Eigenvalues plot of a random matrix

        import numpy as np
        from dyson_equalizer.plots import plot_mp_density

        m, n = 100, 1000
        X = np.random.normal(size=(m, n))
        Y = X @ X.T / n
        eigs = sorted(np.linalg.eigvals(Y), reverse=True)

        plot_mp_density(eigs, gamma=m/n)

    """
    if ax is None:
        _, ax = plt.subplots()

    eigs = np.asarray(eigs)
    beta_p = (1 + gamma ** 0.5) ** 2
    rank = np.sum(eigs > beta_p)

    if show_only_significant is not None:
        eigs = eigs[rank - show_only_significant:]

    ax.hist(eigs, bins='auto', density=True, label=f'Eigenvalues of {matrix_label}')
    x = np.linspace(start=0, stop=eigs[0] * 1.05, num=1000)
    mp = marchenko_pastur(x, gamma)
    ax.plot(x, mp, color='red', label='MP density')
    ax.axvline(beta_p, linestyle='--',  color='green', label='MP upper edge β₊')
    ax.legend()
