"""
    The ``dyson_equalizer.dyson_equalizer`` module contains the class DysonEqualizer that can be used
    to easily compute the Dyson Equalizer.

"""
from typing import Self

import numpy as np
from matplotlib import pyplot as plt

from dyson_equalizer.algorithm import compute_scaling_factors, compute_low_rank_approximation_mp, scale_matrix
from dyson_equalizer.plots import plot_mp_eigenvalues, plot_mp_density
from dyson_equalizer.validation import validate_matrix


class DysonEqualizer:
    """
    This class can be used to compute the Dyson Equalizer [1]_ and store all associated results.


    Attributes
    ----------
    Y: (m, n) numpy.ndarray
        The original data matrix

    x_hat: (m) numpy.ndarray
        The normalizing factors for the rows

    y_hat: (n) numpy.ndarray
        The normalizing factors for the columns

    Y_hat: (m, n) numpy.ndarray
        The normalized data matrix so that the variance of the error is 1

    X_bar: (m, n) numpy.ndarray
        The estimated signal matrix. It has rank `r_hat`

    r_hat: int
        The estimated rank of the signal matrix

    S: (m) numpy.ndarray
        The principal values of the data matrix `Y`

    S_hat: (m) numpy.ndarray
        The principal values of the normalized data matrix `Y_hat`

    See Also
    --------
    dyson_equalizer.algorithm.compute_scaling_factors
    dyson_equalizer.algorithm.compute_low_rank_approximation_mp

    """

    #:  The original data matrix
    Y: np.ndarray

    #:  The normalizing factors for the rows
    x_hat: np.ndarray = None

    #:  The normalizing factors for the columns
    y_hat: np.ndarray = None

    #:  The normalized data matrix so that the variance of the error is 1
    Y_hat: np.ndarray = None

    #:  The estimated signal matrix. It has rank `r_hat`
    X_bar: np.ndarray = None

    #:  The estimated rank of the signal matrix
    r_hat: int = None

    #:  The principal values of the data matrix `Y`
    S: np.ndarray = None

    #:  The principal values of the data matrix `Y_hat`
    S_hat: np.ndarray = None

    def __init__(self, Y: np.ndarray):
        """ Creates a Dyson Equalizer object.

        Parameters
        ----------
        Y: (m, n) array-like
            The original data matrix
        """
        self.Y = validate_matrix(Y)

    def compute(
            self,
            use_Y_hat: bool = False
    ) -> Self:
        """ Computes the Dyson Equalizer and stores the results.

        Parameters
        ----------
        use_Y_hat: bool, optional
            if ``True`` uses `Y_hat` instead of the original matrix as input.
            This option may be used iteratively to improve the low rank approximation in some cases

        Returns
        -------
        self : DysonEqualizer
            A reference to this instance
        """
        Y = self.Y_hat if use_Y_hat else self.Y
        svd = np.linalg.svd(Y, full_matrices=False)
        x_hat, y_hat = compute_scaling_factors(svd)
        Y_hat = scale_matrix(self.Y, 1 / np.sqrt(x_hat), 1 / np.sqrt(y_hat))

        svd_hat = np.linalg.svd(Y_hat, full_matrices=False)
        Y_tr, r_hat = compute_low_rank_approximation_mp(svd_hat)

        X_bar = scale_matrix(Y_tr, np.sqrt(x_hat), np.sqrt(y_hat))

        self.x_hat = x_hat
        self.y_hat = y_hat
        self.Y_hat = Y_hat
        self.X_bar = X_bar
        self.r_hat = r_hat
        self.S = svd.S
        self.S_hat = svd_hat.S

        return self

    def plot_mp_eigenvalues_and_densities(
            self,
            log_eigenvalues: bool = True,
            eigenvalues_to_show: int = 100,
            show_only_significant: int = 2,
            figsize: tuple[int, int] = (12, 8),
    ) -> None:
        """ Plots the eigenvalues of ¹⁄ₙYYᵀ  of ¹⁄ₙŶŶᵀ and their densities.

        and compares to the Marchenko-Pastur threshold

        Parameters
        ----------
        eigenvalues_to_show: int, optional
            The number of eigenvalues to show in the eigenvalue plots (defaults to 100)
        log_eigenvalues: bool, optional
            Whether the y-axis should be logarithmic  in the eigenvalue plots (defaults to True)
        show_only_significant: int = None,
            Set this value to show only a small number of significant eigenvalues in the density plots
            This option is useful is some of the signal eigenvalues are much bigger than the noise.
        figsize: int, int
            The figure size

        See Also
        --------

        plot_mp_eigenvalues_Y
        plot_mp_eigenvalues_Y_hat
        plot_mp_density_Y
        plot_mp_density_Y_hat
        """
        fig, ((ax_11, ax_12), (ax_21, ax_22)) = plt.subplots(nrows=2, ncols=2, figsize=figsize)

        self.plot_mp_eigenvalues_Y(ax=ax_11, log_y=log_eigenvalues, eigenvalues_to_show=eigenvalues_to_show)
        self.plot_mp_eigenvalues_Y_hat(ax=ax_12, log_y=log_eigenvalues, eigenvalues_to_show=eigenvalues_to_show)
        self.plot_mp_density_Y(ax=ax_21, show_only_significant=show_only_significant)
        self.plot_mp_density_Y_hat(ax=ax_22, show_only_significant=show_only_significant)


    def plot_mp_eigenvalues_Y(
            self,
            eigenvalues_to_show: int = 100,
            log_y: bool = True,
            ax: plt.Axes | None = None,
    ) -> None:
        """  Plots the eigenvalues of ¹⁄ₙYYᵀ and compares to the Marchenko-Pastur threshold

        Parameters
        ----------
        eigenvalues_to_show: int, optional
            The number of eigenvalues to show in the plot (defaults to 100)
        log_y: bool, optional
            Whether the y-axis should be logarithmic (defaults to True)
        ax: plt.Axes, optional
            A matplotlib Axes object. If none is provided, a new figure is created.

        Returns
        -------

        See Also
        --------
        dyson_equalizer.plots.plot_mp_eigenvalues

        """
        m, n = sorted(self.Y.shape)
        eigs = self.S ** 2 / n
        plot_mp_eigenvalues(
            eigs, gamma=m/n,
            eigenvalues_to_show=eigenvalues_to_show,
            log_y=log_y,
            matrix_label='¹⁄ₙYYᵀ',
            ax=ax,
        )

    def plot_mp_eigenvalues_Y_hat(
            self,
            eigenvalues_to_show: int = 100,
            log_y: bool = True,
            ax: plt.Axes | None = None,
    ) -> None:
        """  Plots the eigenvalues of ¹⁄ₙŶŶᵀ and compares to the Marchenko-Pastur threshold

        Parameters
        ----------
        eigenvalues_to_show: int, optional
            The number of eigenvalues to show in the plot (defaults to 100)
        log_y: bool, optional
            Whether the y-axis should be logarithmic (defaults to True)
        ax: plt.Axes, optional
            A matplotlib Axes object. If none is provided, a new figure is created.

        See Also
        --------
        dyson_equalizer.plots.plot_mp_eigenvalues

        """
        m, n = sorted(self.Y_hat.shape)
        eigs = self.S_hat ** 2 / n
        plot_mp_eigenvalues(
            eigs, gamma=m/n,
            eigenvalues_to_show=eigenvalues_to_show,
            log_y=log_y,
            matrix_label='¹⁄ₙŶŶᵀ',
            ax=ax,
        )

    def plot_mp_density_Y(
            self,
            show_only_significant: int = None,
            ax: plt.Axes | None = None,
    ) -> None:
        """Plots the density of eigenvalues of ¹⁄ₙYYᵀ and compares to the Marchenko-Pastur distribution

        This function assumes the input are the eigenvalues of a covariance matrix of a random matrix
        whose entries have variance 1. These eigenvalues follow the Marchenko-Pastur distribution.

        Parameters
        ----------
        show_only_significant: int, optional
            Set this value to show only a small number of significant eigenvalues (defaults to None)
            This option is useful is some of the signal eigenvalues are much bigger than the noise.
        ax: plt.Axes, optional
            A matplotlib Axes object. If none is provided, a new figure is created.

        See Also
        --------
        dyson_equalizer.plots.plot_mp_density

        """
        m, n = sorted(self.Y.shape)
        eigs = self.S ** 2 / n
        plot_mp_density(
            eigs, gamma=m/n,
            show_only_significant=show_only_significant,
            matrix_label='¹⁄ₙYYᵀ',
            ax=ax,
        )

    def plot_mp_density_Y_hat(
            self,
            show_only_significant: int = None,
            ax: plt.Axes | None = None,
    ) -> None:
        """Plots the density of eigenvalues of ¹⁄ₙŶŶᵀ and compares to the Marchenko-Pastur distribution

        This function assumes the input are the eigenvalues of a covariance matrix of a random matrix
        whose entries have variance 1. These eigenvalues follow the Marchenko-Pastur distribution.

        Parameters
        ----------
        show_only_significant: int, optional
            Set this value to show only a small number of significant eigenvalues (defaults to None)
            This option is useful is some of the signal eigenvalues are much bigger than the noise.
        ax: plt.Axes, optional
            A matplotlib Axes object. If none is provided, a new figure is created.

        See Also
        --------
        dyson_equalizer.plots.plot_mp_density

        """
        m, n = sorted(self.Y_hat.shape)
        eigs = self.S_hat ** 2 / n
        plot_mp_density(
            eigs, gamma=m/n,
            show_only_significant=show_only_significant,
            matrix_label='¹⁄ₙŶŶᵀ',
            ax=ax,
        )
