import matplotlib.pyplot as plt
import numpy as np
import glob
from matplotlib.widgets import Slider
import astropy.constants as u
from scipy.interpolate import interp2d

au = u.au.cgs.value

# read in hydro data

hydro_r = np.loadtxt('data_evolving/domain_y.dat')
files = sorted(glob.glob('data_evolving/*.txt'))
hydro_data = np.array([np.loadtxt(file) for file in files])
times = np.array([float(file[-11:-4]) for file in files])
times /= times[-1]

# define hydro interpolation function

f2d = interp2d(np.log10(hydro_r), times, np.log10(hydro_data))


def get_hydro(r, t):
    """
    Get hydro profile by interpolating the data.

    r : array
        radial array to interpolate onto

    t : float
        time at which the profile is interpolated

    Output
    ------

    array: gas surface density on hydro grid
    """
    return 10**f2d(np.log10(r), t)


def get_fit(r, sig0, t, masses, radii):
    """
    HERE YOU HAVE TO WRITE YOUR OWN KANAGAWA FUNCTION
    """
    # start with the initial profile
    sig = sig0.copy()

    # for each planet: multiply a factor to represent the gap shape

    for mp, rp in zip(masses, radii):
        sig *= 1 - t * mp * np.exp(-(r - rp)**2 / (2 * (5 * au)**2))

    return sig


# arbitrary initial condition

r = np.logspace(1, np.log10(300), 300) * au
sig_0 = get_hydro(r, 0)

# Make the figure

fig = plt.figure()
ax = fig.add_axes([0.1, 0.3, 0.8, 0.65])
l1, = ax.loglog(hydro_r / au, hydro_data[0], 'k-', label='hydro')
l2, = ax.loglog(r / au, sig_0, 'r', label='fit')
ax.legend(fontsize='small')
ax.set_xlim(r[[0, -1]] / au)
ax.set_ylim(1e-3, 1e3)

# to avoid garbage collection

ax._widgets = []

x0 = ax.get_position().x0
x1 = ax.get_position().x1
y0 = ax.get_position().y0
y1 = ax.get_position().y1
width = x1 - x0
height = y1 - y0

# CREATE SLIDERS

# time slider
axTime = plt.axes([x0 + 0.15 * width,
                   0.20,
                   0.75 * width,
                   0.05 * height], facecolor="lightgoldenrodyellow")

sliderTime = Slider(axTime, "Time", -1, 0, valinit=0, valfmt="%.2f")
title = axTime.set_title('time = ')
ax._widgets += [sliderTime]

# mass slider

axMass1 = plt.axes([x0 + 0.15 * width,
                    0.15,
                    0.25 * width,
                    0.05 * height], facecolor="lightgoldenrodyellow")

axMass2 = plt.axes([x0 + 0.15 * width,
                    0.10,
                    0.25 * width,
                    0.05 * height], facecolor="lightgoldenrodyellow")

axMass3 = plt.axes([x0 + 0.15 * width,
                    0.05,
                    0.25 * width,
                    0.05 * height], facecolor="lightgoldenrodyellow")

sliderMass1 = Slider(axMass1, "$M_1$", 0, 1, valinit=0, valfmt="%.2f")
sliderMass2 = Slider(axMass2, "$M_2$", 0, 1, valinit=0, valfmt="%.2f")
sliderMass3 = Slider(axMass3, "$M_3$", 0, 1, valinit=0, valfmt="%.2f")

ax._widgets += [sliderMass1]
ax._widgets += [sliderMass2]
ax._widgets += [sliderMass3]

# position slider

axRadius1 = plt.axes([x0 + 0.55 * width,
                      0.15,
                      0.25 * width,
                      0.05 * height], facecolor="lightgoldenrodyellow")

axRadius2 = plt.axes([x0 + 0.55 * width,
                      0.10,
                      0.25 * width,
                      0.05 * height], facecolor="lightgoldenrodyellow")

axRadius3 = plt.axes([x0 + 0.55 * width,
                      0.05,
                      0.25 * width,
                      0.05 * height], facecolor="lightgoldenrodyellow")

sliderRadius1 = Slider(axRadius1, "$R_1$", 1, 300, valinit=50, valfmt="%.2f")
sliderRadius2 = Slider(axRadius2, "$R_2$", 1, 300, valinit=100, valfmt="%.2f")
sliderRadius3 = Slider(axRadius3, "$R_3$", 1, 300, valinit=150, valfmt="%.2f")

ax._widgets += [sliderRadius1]
ax._widgets += [sliderRadius2]
ax._widgets += [sliderRadius3]


def callback(event):
    """
    The callback for updating the figure when the buttons are clicked
    """

    # get all values from the sliders

    time = 10**sliderTime.val
    M1 = sliderMass1.val
    M2 = sliderMass2.val
    M3 = sliderMass3.val
    R1 = sliderRadius1.val * au
    R2 = sliderRadius2.val * au
    R3 = sliderRadius3.val * au

    # update log sliders with a meaningful value

    title.set_text(f'time = {time:.2g}')

    # get the new profiles

    sig_hydro = get_hydro(hydro_r, time)
    sig_fit = get_fit(r, sig_0, time, [M1, M2, M3], [R1, R2, R3])

    # update the lines with the new profiles

    l1.set_ydata(sig_hydro)
    l2.set_ydata(sig_fit)


# connect all sliders to the callback function

sliderTime.on_changed(callback)
sliderMass1.on_changed(callback)
sliderMass2.on_changed(callback)
sliderMass3.on_changed(callback)
sliderRadius1.on_changed(callback)
sliderRadius2.on_changed(callback)
sliderRadius3.on_changed(callback)

# call the callback function once to make the plot agree with state of the buttons
callback(None)

plt.show()
