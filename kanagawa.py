import numpy as np


def get_fit(r, sig_ini, t, masses, radii, alpha, hp, M_star):
    """Return kanagawa-multiplanet fit.

    Parameters
    ----------
    r : array
        radial grid

    sig_ini : array
        initial gas surface density

    t : float
        normalized time

    masses : list of floats
        planet masses [g]

    radii : list of floats
        list of planet radii [au]

    alpha : array | float
        value or array of alpha turbulence parameters

    hp : array | float
        value or array of scale heights

    M_star : float
        stellar mass in g

    Returns
    -------
    array
        surface density array

    """

    """
    HERE YOU HAVE TO WRITE YOUR OWN KANAGAWA FUNCTION
    """
    factor = np.ones_like(r)

    # for each planet: multiply a factor to represent the gap shape

    for mp, rp in zip(masses, radii):
        factor *= get_kanagawa_factor(r, hp, mp, rp, M_star, alpha, smooth=None)

    return sig_ini * (factor * t**.2 + (1 - t**.2))


def get_kanagawa_factor(r, hp, m_planet, a_planet, mstar, alpha, smooth=None):
    """Short summary.

    Parameters
    ----------
    r : array
        radial grid

    hp : float | array
        pressure scale height (float or array)

    m_planet : float
        planet mass

    a_planet : float
        planet semimajor axis

    mstar : float
        stellar mass

    alpha : float | array
        turbulence parameter

    Keywords
    --------

    smooth : None | float
        if float, smooth the profile over that many hill radii

    Returns
    -------
    array
        surface density reduction factor

    """
    hp = np.interp(a_planet, r, np.ones_like(r) * hp)
    alpha = np.interp(a_planet, r, alpha * np.ones_like(r))

    K = (m_planet / mstar)**2 * (hp / a_planet)**-5 / alpha
    Kp = (m_planet / mstar)**2 * (hp / a_planet)**-3 / alpha

    factor_min = 1. / (1. + 0.04 * K)  # Eq. 11

    delta_R_1 = (factor_min / 4. + 0.08) * Kp**0.25 * a_planet  # Eq. 8
    delta_R_2 = 0.33 * Kp**0.25 * a_planet  # Eq. 9

    factor_gap = 4 * Kp**-0.25 * np.abs(r - a_planet) / a_planet - 0.32  # Eq. 7

    # Eqn. 6

    factor = np.ones_like(r)

    mask1 = np.abs(r - a_planet) < delta_R_1
    mask2 = (delta_R_1 <= np.abs(r - a_planet)) & (np.abs(r - a_planet) <= delta_R_2)

    factor[mask1] = factor_min
    factor[mask2] = factor_gap[mask2]

    if smooth is not None:
        r_H = a_planet * (m_planet / (mstar * 3.))**(1. / 3.)
        drsmooth = smooth * r_H
        factor = np.exp(np.log(factor) * np.exp(-0.5 * (r - a_planet)**4 / drsmooth**4))

    return factor
