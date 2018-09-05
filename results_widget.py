import matplotlib.pyplot as plt
import matplotlib.widgets as w
import numpy as np

# Get the data

data = []

with open('data.csv') as fid:
    while True:
        line = fid.readline()
        if line.strip().startswith('#'):
            continue

        if line.strip() == '':
            break

        line = line.strip().split(',')
        sim_nr = int(line.pop(0))
        alpha = float(line.pop(0))
        vf = float(line.pop(0))
        nr = int(line.pop(0))
        r = [float(line.pop(0)) for i in range(nr)]
        Inu = [float(line.pop(0)) for i in range(nr)]

        data += [[
            sim_nr,
            alpha,
            vf,
            nr,
            r,
            Inu
            ]]


# Make the figure

fig = plt.figure()

ax = fig.add_axes([0.1, 0.3, 0.5, 0.6])

# make up the isella profile

r_isella = [0.5, 3, 10, 15]
Inu_isella = [20, 10, 12, 8]

# plot the isella profile

ax.plot(r_isella, Inu_isella, 'k--')

# now we need to make a variable number of buttons

simnr_values = sorted(list(set([d[0] for d in data])))
alpha_values = sorted(list(set([d[1] for d in data])))
vf_values = sorted(list(set([d[2] for d in data])))

# to avoid garbage collection
ax._widgets = []

# CREATE BUTTONS

button_width = 0.1
button_lheigh = 0.07
button_x0 = 0.05
button_y0 = 0.05

# 1. ALPHA
n_buttons = len(alpha_values)
ax_alpha = fig.add_axes([button_x0, button_y0, button_width, n_buttons * button_lheigh])
alpha_buttons = w.CheckButtons(ax_alpha, [str(s) for s in alpha_values], [True] + (n_buttons - 1) * [False])
ax_alpha.set_title(r'$\alpha$')
ax._widgets += [alpha_buttons]  # avoids garbage collection

# 2. vf
n_buttons = len(vf_values)
ax_vf = fig.add_axes([button_x0 + button_width, button_y0, button_width, n_buttons * button_lheigh])
vf_buttons = w.CheckButtons(ax_vf, [str(s) for s in vf_values], [True] + (n_buttons - 1) * [False])
ax_vf.set_title(r'$v_\mathrm{frag}$')
ax._widgets += [vf_buttons]  # avoids garbage collection

info_dict = {}


def callback(event):
    """
    The callback for updating the figure when the buttons are clicked
    """
    # get masks for all the selected values

    alpha_states = alpha_buttons.get_status()
    alpha_selected = np.array(alpha_values)[alpha_states]

    vf_states = vf_buttons.get_status()
    vf_selected = np.array(vf_values)[vf_states]

    # delete all simulation lines (keeping the observational line)

    for _line in ax.get_lines()[1:]:
        _line.remove()

    # plot all lines that match the selected values
    # in info_dict, we store a information string with the parameter
    # values for every line
    info_dict.clear()
    for d in data:
        if d[1] in alpha_selected and d[2] in vf_selected:
            l, = ax.plot(d[-2], d[-1], '0.5', picker=True)
            info_dict[l] = r'$\alpha$' + ' = {}, $v_\mathrm{{frag}}$ = {}'.format(d[1], d[2])

    ax.set_title('click on a line to see its parameters!', fontsize='small')
    plt.draw()


def onpick(event):
    """
    Function that gets called if a line is clicked
    """
    if isinstance(event.artist, plt.Line2D):
        ax.set_title('parameters of this line: ' + info_dict[event.artist], fontsize='small')
        for line in ax.get_lines()[1:]:
            line.set_color('0.5')
        event.artist.set_color('r')
        plt.draw()


fig.canvas.mpl_connect('pick_event', onpick)

# now link the callback to the buttons

alpha_buttons.on_clicked(callback)
vf_buttons.on_clicked(callback)

# call the callback function once to make the plot agree with state of the buttons
callback(None)

plt.show()
